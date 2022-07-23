import cv2

#采用均值hash函数进行图像相似度判断
# Hash值对比
from PIL import UnidentifiedImageError

from textSimilar import find_student_picture, picture_cut


def cmpHash(hash1, hash2, shape=(10, 10)):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 相等则n计数+1，n最终为相似度
        if hash1[i] == hash2[i]:
            n = n + 1
    return n / (shape[0] * shape[1])


# 均值哈希算法
def aHash(img, shape=(10, 10)):
    # 缩放为10*10
    img=cv2.imread(img)
    img = cv2.resize(img, shape)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(shape[0]):
        for j in range(shape[1]):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 100
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(shape[0]):
        for j in range(shape[1]):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


def hash_similar(hashResult):
    hashList=[]
    for i in range(len(hashResult)-1):
        n = cmpHash(hashResult[i], hashResult[i+1])
        hashList.append(n)
        print("hash相似度："+str(n))
    return hashList

def picture_to_hash(filePath):
    studentPicture =find_student_picture(filePath)
    result=[]
    for singlePicture in studentPicture:
        try:
            picture_cut(filePath,filePath + "/" + singlePicture)
            hashResult = aHash(filePath+"/tempPicture.jpg")
            result.append(hashResult)
        except UnidentifiedImageError:
            print(singlePicture)
    print(result)
    hashSimilarList=hash_similar(result)
    return hashSimilarList