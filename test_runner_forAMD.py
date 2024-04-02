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
    with np.load(datafile, allow_pickle=True) as data:
        data_in = data['data']

    new_arr = np.zeros((6,1,128,2), dtype='float32')
    new_arr[0] = data_in[0].reshape(6,1,128,2)
    return new_arr

if __name__ == "__main__":
    args = parse_args()
    main(args.xmodel, args.datafile)
