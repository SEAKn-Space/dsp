import vart
import xir

import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(prog='Test graph runner')
    parser.add_argument('fname')
    return parser.parse_args()

def main(fname: str):
    args = parse_args()

    g = xir.Graph.deserialize(fname)
    subgraphs = g.get_root_subgraph().toposort_child_subgraph()

    sg_dpu = subgraphs[3]

    dpu_runner = vart.Runner.create_runner(sg_dpu, "run")

    # In and out dims
    input_tensor = dpu_runner.get_input_tensors()
    output_tensor = dpu_runner.get_output_tensors()

    in_dim = tuple(input_tensor[0].dims)
    out_dim = tuple(output_tensor[0].dims)

    dpu_out = np.zeros(out_dim, dtype='float32')

    dpu_in = load_data(args.fname)

    exec_async(dpu_runner, {
        "CNN2D__CNN2D_ret_3_swim_transpose_0_fix": dpu_in[0],
        "CNN2D__CNN2D_Linear_fc2__ret_fix": dpu_out[0]
        })

    print(dpu_out)

def exec_async(dpu, tensor_buffers_dict):
    input_tensor_buffers = [
            tensor_buffers_dict[t.name] for t in dpu.get_input_tensors()
            ]
    print(dpu.get_input_tensors()[0].dims)
    output_tensor_buffers = [
            tensor_buffers_dict[t.name] for t in dpu.get_output_tensors()
            ]
    print(dpu.get_output_tensors()[0].dims)
    jid = dpu.execute_async(input_tensor_buffers, output_tensor_buffers)
    return dpu.wait(jid)

def load_data(fname):
    in_data = np.random.rand(1,2,128).astype('float32')
    print("in_data:", in_data.shape)
    out_data = in_data.reshape(1,1,128,2)
    print("out_data:", out_data.shape)
    return out_data

if __name__ == '__main__':
    args = parse_args()
    main(args.fname)
