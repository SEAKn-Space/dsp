import argparse
import random

import numpy as np
import pandas as pd

import vart
import xir


def parse_args():
    parser = argparse.ArgumentParser(prog="Test graph runner")
    parser.add_argument("xmodel")
    parser.add_argument("datafile")
    return parser.parse_args()


def main(xmodel: str, datafile: str):
    args = parse_args()

    g = xir.Graph.deserialize(xmodel)
    subgraphs = g.get_root_subgraph().toposort_child_subgraph()

    # Only the 4th subgraph should be run on the DPU, others are CPU data reshaping
    sg_dpu = subgraphs[3]

    dpu_runner = vart.Runner.create_runner(sg_dpu, "run")

    # In and out dims
    input_tensor = dpu_runner.get_input_tensors()
    output_tensor = dpu_runner.get_output_tensors()

    in_dim = tuple(input_tensor[0].dims)
    out_dim = tuple(output_tensor[0].dims)

    # Run some number of tests, each with randomly selected input data
    for i in range(1):
        dpu_out = np.zeros(out_dim, dtype="float32")

        dpu_in = load_data(args.datafile)

        exec_async(
            dpu_runner,
            {
                "CNN2D__CNN2D_ret_3_swim_transpose_0_fix": dpu_in,
                "CNN2D__CNN2D_Linear_fc2__ret_fix": dpu_out,
            },
        )

        print(f"Test {i}: \r\n{dpu_out}")


def exec_async(dpu, tensor_buffers_dict):
    input_tensor_buffers = [
        tensor_buffers_dict[t.name] for t in dpu.get_input_tensors()
    ]
    output_tensor_buffers = [
        tensor_buffers_dict[t.name] for t in dpu.get_output_tensors()
    ]
    jid = dpu.execute_async(input_tensor_buffers, output_tensor_buffers)
    return dpu.wait(jid)


def load_data(datafile):
    int_rand = random.randint(0, 994)

    # Load in real data from the provided file
    data = pd.read_pickle(datafile, compression="infer")
    qpsk_data = data[("QPSK", 2)]
    bpsk_data = data[("BPSK", 2)]

    b_sample = bpsk_data[int_rand : int_rand + 6, :, :].reshape(6, 1, 128, 2)
    q_sample = qpsk_data[int_rand : int_rand + 6, :, :].reshape(6, 1, 128, 2)

    sample = q_sample

    new_sample = np.empty((6, 1, 128, 2), dtype="float32")

    for i, s in enumerate(sample):
        new_sample[i] = norm_sample(s[0])

    return new_sample


def norm_sample(samp):

    real = samp[:, 0]
    imag = samp[:, 1]

    return np.array(
        [
            2 * (real - min(real) / (max(real) - min(real) + 1e-10)) - 1,
            2 * (imag - min(imag) / (max(imag) - min(imag) + 1e-10)) - 1,
        ]
    ).reshape(1, 128, 2)


if __name__ == "__main__":
    args = parse_args()
    main(args.xmodel, args.datafile)
