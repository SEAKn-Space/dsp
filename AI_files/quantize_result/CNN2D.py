# GENETARED BY NNDCT, DO NOT EDIT!

import torch
from torch import tensor
import pytorch_nndct as py_nndct

class CNN2D(py_nndct.nn.NndctQuantModel):
    def __init__(self):
        super(CNN2D, self).__init__()
        self.module_0 = py_nndct.nn.Input() #CNN2D::input_0(CNN2D::nndct_input_0)
        self.module_1 = py_nndct.nn.Module('nndct_unsqueeze') #CNN2D::CNN2D/ret.3(CNN2D::nndct_unsqueeze_1)
        self.module_2 = py_nndct.nn.Interpolate() #CNN2D::CNN2D/Upsample[upsample]/ret.5(CNN2D::nndct_resize_2)
        self.module_3 = py_nndct.nn.Conv2d(in_channels=2, out_channels=64, kernel_size=[1, 3], stride=[1, 1], padding=[0, 1], dilation=[1, 1], groups=1, bias=True) #CNN2D::CNN2D/Conv2d[conv1]/ret.7(CNN2D::nndct_conv2d_3)
        self.module_4 = py_nndct.nn.ReLU(inplace=False) #CNN2D::CNN2D/ReLU[relu1]/ret.9(CNN2D::nndct_relu_4)
        self.module_5 = py_nndct.nn.AdaptiveAvgPool2d(output_size=[1, 64]) #CNN2D::CNN2D/AdaptiveAvgPool2d[adaptive_pool1]/446(CNN2D::nndct_adaptive_avg_pool2d_5)
        self.module_6 = py_nndct.nn.Conv2d(in_channels=64, out_channels=128, kernel_size=[1, 3], stride=[1, 1], padding=[0, 1], dilation=[1, 1], groups=1, bias=True) #CNN2D::CNN2D/Conv2d[conv2]/ret.11(CNN2D::nndct_conv2d_6)
        self.module_7 = py_nndct.nn.ReLU(inplace=False) #CNN2D::CNN2D/ReLU[relu2]/ret.13(CNN2D::nndct_relu_7)
        self.module_8 = py_nndct.nn.AdaptiveAvgPool2d(output_size=[1, 32]) #CNN2D::CNN2D/AdaptiveAvgPool2d[adaptive_pool2]/486(CNN2D::nndct_adaptive_avg_pool2d_8)
        self.module_9 = py_nndct.nn.AdaptiveAvgPool2d(output_size=[1, 1]) #CNN2D::CNN2D/AdaptiveAvgPool2d[adaptive_avg_pool2d]/504(CNN2D::nndct_adaptive_avg_pool2d_9)
        self.module_10 = py_nndct.nn.Module('nndct_shape') #CNN2D::CNN2D/507(CNN2D::nndct_shape_10)
        self.module_11 = py_nndct.nn.Module('nndct_reshape') #CNN2D::CNN2D/ret.17(CNN2D::nndct_reshape_11)
        self.module_12 = py_nndct.nn.Linear(in_features=128, out_features=256, bias=True) #CNN2D::CNN2D/Linear[fc1]/ret.19(CNN2D::nndct_dense_12)
        self.module_13 = py_nndct.nn.ReLU(inplace=False) #CNN2D::CNN2D/ReLU[relu3]/ret.21(CNN2D::nndct_relu_13)
        self.module_14 = py_nndct.nn.Linear(in_features=256, out_features=2, bias=True) #CNN2D::CNN2D/Linear[fc2]/ret(CNN2D::nndct_dense_14)

    @py_nndct.nn.forward_processor
    def forward(self, *args):
        output_module_0 = self.module_0(input=args[0])
        output_module_0 = self.module_1(input=output_module_0, dim=-2)
        output_module_0 = self.module_2(input=output_module_0, size=None, scale_factor=[1.0,2.0], mode='bilinear', align_corners=False)
        output_module_0 = self.module_3(output_module_0)
        output_module_0 = self.module_4(output_module_0)
        output_module_0 = self.module_5(output_module_0)
        output_module_0 = self.module_6(output_module_0)
        output_module_0 = self.module_7(output_module_0)
        output_module_0 = self.module_8(output_module_0)
        output_module_0 = self.module_9(output_module_0)
        output_module_10 = self.module_10(input=output_module_0, dim=0)
        output_module_11 = self.module_11(input=output_module_0, shape=[output_module_10,-1])
        output_module_11 = self.module_12(output_module_11)
        output_module_11 = self.module_13(output_module_11)
        output_module_11 = self.module_14(output_module_11)
        return output_module_11
