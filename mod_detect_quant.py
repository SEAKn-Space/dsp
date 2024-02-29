import os
import re
import sys
import argparse
import time
import pdb
import random
from pytorch_nndct.apis import torch_quantizer
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.models.resnet import resnet18

from tqdm import tqdm

from torch.utils.data import Dataset, DataLoader


device = torch.device("cpu")

parser = argparse.ArgumentParser()

parser.add_argument(
    "--data_dir",
    default="/path/to/imagenet/",
    help="Data set directory, when quant_mode=calib, it is for calibration, while quant_mode=test it is for evaluation",
)
parser.add_argument(
    "--model_dir",
    default="/path/to/trained_model/",
    help="Trained model file path. Download pretrained model from the following url and put it in model_dir specified path: https://download.pytorch.org/models/resnet18-5c106cde.pth",
)
parser.add_argument(
    "--config_file", default=None, help="quantization configuration file"
)
parser.add_argument(
    "--subset_len",
    default=None,
    type=int,
    help="subset_len to evaluate model, using the whole validation dataset if it is not set",
)
parser.add_argument(
    "--batch_size", default=32, type=int, help="input data batch size to evaluate model"
)
parser.add_argument(
    "--quant_mode",
    default="calib",
    choices=["float", "calib", "test"],
    help="quantization mode. 0: no quantization, evaluate float model, calib: quantize, test: evaluate quantized model",
)
parser.add_argument(
    "--fast_finetune",
    dest="fast_finetune",
    action="store_true",
    help="fast finetune model before calibration",
)
parser.add_argument(
    "--deploy", dest="deploy", action="store_true", help="export xmodel for deployment"
)
parser.add_argument(
    "--inspect", dest="inspect", action="store_true", help="inspect model"
)
args, _ = parser.parse_known_args()


def load_data(
    data_dir="dataset/imagenet",
):

    data = pd.read_pickle(data_dir, compression="infer")
    qpsk_2_data_all = data[("QPSK", 2)]
    bpsk_2_data_all = data[("BPSK", 2)]

    # labels
    qpsk_labels = [0] * 1000  # QPSK = 0
    bpsk_labels = [1] * 1000  # BPSK = 1

    # combine the data lables
    data_combined = np.concatenate((qpsk_2_data_all, bpsk_2_data_all), axis=0)
    labels_combined = qpsk_labels + bpsk_labels

    # convert labels to NumPy array and then to PyTorch tensor with Long data type
    labels_combined = np.array(labels_combined, dtype=np.int64)
    labels_combined = torch.from_numpy(labels_combined).long()

    # convert 2 PyTorch tensor
    data_combined = torch.from_numpy(data_combined).float()

    # convert labels 2 NumPy array and then 2 PyTorch tensor
    labels_combined = np.array(labels_combined)
    labels_combined = torch.from_numpy(labels_combined)

    # break into training + testing
    test_size = 0.2  # Adjust the test size as needed
    data_train, data_test, labels_train, labels_test = train_test_split(
        data_combined, labels_combined, test_size=test_size, random_state=42
    )

    class MyDataset(Dataset):
        def __init__(self, data, labels):
            self.data = data
            self.labels = labels

        def __len__(self):
            return len(self.data)

        def __getitem__(self, idx):
            # access a single data sample and label
            sample = self.data[idx]
            label = self.labels[idx]

            # Convert sample, min_vals, and max_vals to PyTorch tensors
            sample = torch.tensor(sample, dtype=torch.float32)
            min_vals = torch.tensor(sample.min(axis=1).values, dtype=torch.float32)
            max_vals = torch.tensor(sample.max(axis=1).values, dtype=torch.float32)

            # normalize
            epsilon = 1e-10
            normalized_sample = (
                2
                * (sample - min_vals.unsqueeze(1))
                / (max_vals.unsqueeze(1) - min_vals.unsqueeze(1) + epsilon)
                - 1
            )

            return normalized_sample, label

    train_dataset = MyDataset(data_train, labels_train)
    test_dataset = MyDataset(data_test, labels_test)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)

    return train_loader, test_loader


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self, name, fmt=":f"):
        self.name = name
        self.fmt = fmt
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


    def __str__(self):
        fmtstr = "{name} {val" + self.fmt + "} ({avg" + self.fmt + "})"
        return fmtstr.format(**self.__dict__)


def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions
    for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].flatten().float().sum(0, keepdim=True)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res


def evaluate(model, val_loader, loss_fn):

    model.eval()
    model = model.to(device)
    top1 = AverageMeter("Acc@1", ":6.2f")
    top5 = AverageMeter("Acc@5", ":6.2f")
    total = 0
    Loss = 0
    for iteraction, (images, labels) in tqdm(
        enumerate(val_loader), total=len(val_loader)
    ):
        images = images.to(device)
    labels = labels.to(device)
    # pdb.set_trace()
    outputs = model(images)
    loss = loss_fn(outputs, labels)
    Loss += loss.item()
    total += images.size(0)
    acc1, acc5 = accuracy(outputs, labels, topk=(1, 5))
    top1.update(acc1[0], images.size(0))
    top5.update(acc5[0], images.size(0))
    return top1.avg, top5.avg, Loss / total


def quantization(title="optimize", model_name="", file_path=""):

    data_dir = args.data_dir
    quant_mode = args.quant_mode
    finetune = args.fast_finetune
    deploy = args.deploy
    batch_size = args.batch_size
    subset_len = args.subset_len
    inspect = args.inspect
    config_file = args.config_file
    if quant_mode != "test" and deploy:
        deploy = False
    print(
        r"Warning: Exporting xmodel needs to be done in quantization test mode, turn off it in this running!"
    )
    if deploy and (batch_size != 1 or subset_len != 1):
        print(
            r"Warning: Exporting xmodel needs batch size to be 1 and only 1 iteration of inference, change them automatically!"
        )
    batch_size = 1
    subset_len = 1

    model = resnet18().cpu()
    model.load_state_dict(torch.load(file_path))

    input = torch.randn([batch_size, 3, 224, 224])
    if quant_mode == "float":
        quant_model = model
    if inspect:
        import sys
        from pytorch_nndct.apis import Inspector

        # create inspector
        # inspector = Inspector("0x603000b16013831") # by fingerprint
        inspector = Inspector("DPUCAHX8L_ISA0_SP")  # by name
        # start to inspect
        inspector.inspect(quant_model, (input,), device=device)
        sys.exit()
    else:
        ## new api
        ####################################################################################
        quantizer = torch_quantizer(
            quant_mode, model, (input), device=device, quant_config_file=config_file
        )

        quant_model = quantizer.quant_model
        #####################################################################################

    # to get loss value after evaluation
    loss_fn = torch.nn.CrossEntropyLoss().to(device)

    val_loader, _ = load_data(data_dir)

    # fast finetune model or load finetuned parameter before test
    if finetune == True:
        ft_loader, _ = load_data(
            subset_len=5120,
            train=False,
            batch_size=batch_size,
            sample_method="random",
            data_dir=data_dir,
            model_name=model_name,
        )
        if quant_mode == "calib":
            quantizer.fast_finetune(evaluate, (quant_model, ft_loader, loss_fn))
        elif quant_mode == "test":
            quantizer.load_ft_param()

    # record  modules float model accuracy
    # add modules float model accuracy here
    acc_org1 = 0.0
    acc_org5 = 0.0
    loss_org = 0.0

    # register_modification_hooks(model_gen, train=False)
    acc1_gen, acc5_gen, loss_gen = evaluate(quant_model, val_loader, loss_fn)

    # logging accuracy
    print("loss: %g" % (loss_gen))
    print("top-1 / top-5 accuracy: %g / %g" % (acc1_gen, acc5_gen))

    # handle quantization result
    if quant_mode == "calib":
        quantizer.export_quant_config()
    if deploy:
        quantizer.export_xmodel(deploy_check=False)
        quantizer.export_onnx_model()


if __name__ == "__main__":

    model_name = "mod_detect"
    file_path = os.path.join(args.model_dir, model_name + ".pth")

    feature_test = " float model evaluation"
    if args.quant_mode != "float":
        feature_test = " quantization"
        # force to merge BN with CONV for better quantization accuracy
        args.optimize = 1
        feature_test += " with optimization"
    else:
        feature_test = " float model evaluation"
        title = model_name + feature_test

    print("-------- Start {} test ".format(model_name))

    # calibration or evaluation
    quantization(title=title, model_name=model_name, file_path=file_path)

    print("-------- End of {} test ".format(model_name))
