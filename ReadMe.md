## fmtt网格数据转换为vtk格式

> author：peanut, yujh, d103-6 sysu
> date: 202-12-08
> version：1.0



### 1. 首先安装下列python3扩展包

```
pip install pyvista scipy numpy
# 如果有conda虚拟环境，直接激活虚拟环境安装即可，例如
conda activate yourenv
pip install pyvista scipy numpy
```

### 2.运行程序

```
python fmtt_grid_to_vtk.py
```



### 3. 如何打开程序输出的vts文件

- 下载并安装paraview程序
- file-> load data，点击apply，类型选择surface，左下方editcolordata，选择data
- 显示grid与axes，直接在左下方搜索框中搜索grid或axes，对应勾选即可
- 切片，点击左上角切片标示，拖动调整对应方向，点击apply即可，可添加多个切片