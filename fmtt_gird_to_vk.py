
# fmtt网格数据转换为vtk格式
# author：peanut, yujh, d103-6 sysu
# date: 202-12-08

# 首先安装下列python3扩展包
# pip install pyvista scipy numpy

# 如果有conda虚拟环境，直接激活虚拟环境安装即可，例如
# conda activate yourenv
# pip install pyvista scipy numpy

# 运行程序
# python fmtt_grid_to_vtk.py

# 如何打开程序输出的vts文件
# 需要打开paraview程序，load data，选择surface，editcolordata，选择data


import re
import os
import numpy as np

import pyvista as pv
from scipy.ndimage import zoom


def readGrid(file, zscale=0.01, zoom_scaler=8, save=""):
    '''读取fmtt网格数据
    函数自动读取网格文件数据
        - 确保文件由fmtt自动生成，未被后期修改
        - 如果文件被后期修改
            - 确保文件行数目没有被打乱
            - 确保文件中仅存在数字或自然计算法形式的数字，如1e+10，确保文件
        
    zscale: 深度值缩放的比例
    zoom_scaler: 将原始网格，以样条插值方法缩放到指定倍数（在所有维度上）
    save: 如果不为空，则是保存网格文件的名字
    return grid：生成的网vtk数据, data：读取的网格文件速度值
    '''
    assert os.path.join(file), "文件不存在"
    with open(file, "r") as f:
        lines = f.readlines()
    # 提取数字
    lines = [re.findall(r'-?\d+\.?\d*[eE]?-?\d+', i) for i in lines]
    # 去除空行
    lines = [i for i in lines if len(i)>0]
    
    print("{}共：{}行".format(file, len(lines)))

    # 读取形状信息
    nnr, nnt, nnp = [int(i)+2 for i in lines[0]]
    # 读取经纬度信息
    gor, got, gop = [float(i) for i in lines[1]]
    # 读取间距及网格信息
    rgsr, rgst, rgsp = [float(i) for i in lines[2]]

    assert len(lines)-3 == nnr*nnt*nnp
    
    print("读取网格形状:{} {} {}".format(nnr, nnt, nnp))
    
    # 第一列为深度值, 转为负值，乘以z轴缩放因子
    z = (np.arange(nnr) * rgsr * -1 * zscale * zoom_scaler) + gor*zscale
    # 第二列为纬度值
    x = (np.arange(nnt) * rgst * zoom_scaler) + got
    # 第三列为经度值
    y = (np.arange(nnp) * rgsp * zoom_scaler) + gop
    
    # 读取数据
    index = 3
    data = np.full((nnr, nnt, nnp), 0)
    for i in np.arange(nnp):
        for j in np.arange(nnt):
            for k in np.arange(nnr):
                data[k,j,i] = float(lines[index][0])
                index += 1
    # 插值后原始数据   
    print("将原始网格数据进行三次样条插值，缩放到原始形状的{}倍".format(zoom_scaler))
    zoom_data = zoom(data, zoom_scaler, order=3)
    print("三次样条插值完成")
                
    # 创建网格
    zz, yy, xx = np.meshgrid(z, y, x)
    grid = pv.StructuredGrid(xx, yy, zz)
    # 设置网格点数据，先设置的属性默认显示
    grid["data"] = np.rollaxis(data, axis=1).reshape(-1,1)
    # 设置深度数据
    grid["depth"] = (zz*1/zscale).reshape(-1,1)
    
    if( save!= None and save!=""):
        grid.save(save+".vts")
        print("网格文件保存成功:{}".format(save+".vts"))
    
    return grid, zoom_data, data


if __name__ == "__main__":
    file = r"D:\Notebook\层析成像UI\VTK\gridc.vtx"
    save_vtk_file = r"D:\paraviewTest\gridc.vts"
    grid, data, origin_data = readGrid(file, zscale=0.01, zoom_scaler=10, save=save_vtk_file)