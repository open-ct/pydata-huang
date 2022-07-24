## python进行批量图像识别2.0
#### 使用easyocr和均值hash进行图像相似度判断

easyocr准确度不高，但是对同一张图片识别结果一致，因此可用于相似度判断。

均值哈希算法是哈希算法的一类，主要用来做相似图片的搜索工作。

这次的问题是一旦中途停止会丢失一部分进度，还有就是easyocr速度慢。

#### 请确认是否安装好环境
```
pip install torch

pip install torchvision

pip install easyocr

pip install PIL

pip install os

pip install shutil

pip install difflib

pip install thread pool

pip install cv2
```



### 

#### 在control中进行参数调节

```
# 默认路径
DEFAULT_PATH = "10117"

# 对图像进行切割 切割大小的四个参数,分别对应上左下右。
CROP_BOX1 = 0.1
CROP_BOX2 = 0.2
CROP_BOX3 = 1
CROP_BOX4 = 0.95

# 当文字相似度小于这个值，那么就有可能是不同视频
WORD_DIFFERENT = 0.87
# 当图像相似度小于这个值，那么就有可能是不同视频
HASH_DIFFERENT=0.87
#线程数
THREAD=3
```

一次处理一个压缩包结构的文件

default_path设置为一级目录（junior_class）

线程数表示同时进行几个任务。

#### 代码结构

core是文件操作模块和主运行单元，在core中的main函数进行运行。

其中create_dir中可以把wordList=pictureList_to_wordList(file_path)注释掉，只进行hash判断，速度会很快，适合初测。

control是参数所在位置

其他两个是两种相似度判断模块











