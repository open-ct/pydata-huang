# 默认路径
DEFAULT_PATH = "junior_class2"


# 对图像进行切割 切割大小的四个参数,分别对应上左下右。
CROP_BOX1 = 0.1
CROP_BOX2 = 0.2
CROP_BOX3 = 1
CROP_BOX4 = 0.95

# 当文字相似度小于这个值，那么就有可能是不同视频
WORD_DIFFERENT = 0.87
# 当图像相似度小于这个值，那么就有可能是不同视频
HASH_DIFFERENT=0.85
#线程数
THREAD=10