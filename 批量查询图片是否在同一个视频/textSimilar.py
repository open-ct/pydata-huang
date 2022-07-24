import os

import easyocr
from PIL import UnidentifiedImageError
import difflib
from control import CROP_BOX1 ,CROP_BOX2 ,CROP_BOX3 , CROP_BOX4
from PIL import Image



iii = 0


def find_student_picture(filePath):
    studentPicture = os.listdir(filePath)
    studentPicture.sort()
    print(studentPicture)
    return studentPicture

# 图像切割
def picture_cut(filePath,picturePath):
    img_1 = Image.open(picturePath)
    # 设置裁剪的位置
    # crop_box =  (0,600,1078,1680)
    crop_box = (
        [CROP_BOX1 * img_1.size[0], CROP_BOX2 * img_1.size[1], CROP_BOX3 * img_1.size[0], CROP_BOX4 * img_1.size[1]])
    # 裁剪图片
    imgAfterCut = img_1.crop(crop_box)
    # 保存图片
    pathAfterCut = filePath+"/tempPicture.jpg"
    # TODO
    imgAfterCut.save(pathAfterCut)
    return imgAfterCut

# ocr运行函数
def picture_to_text(path):
    res = []
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)

    result = reader.readtext(path)
    # 第一列为文件名
    res.append(path)
    for i in result:
        word = i[1]
        res.append(word)
    print(res)
    return res


# # 存储
# # TODO 感觉不需要了
# def result_to_excel(result):
#     MY_EXCEL = xlwt.Workbook(encoding='utf-8')  # 创建MY_EXCEL对象
#     excelsheet = MY_EXCEL.add_sheet('sheet1')  # 创建工作表（创建excel里面的工作表）
#
#     for i in range(len(result)):
#         for j in range(len(result[i])):
#             excelsheet.write(i, j, result[i][j])
#
#     MY_EXCEL.save("output1.xls")


# 文本相似度进行判断

def string_similar(result, file_path, singlePicture, i):

    # print(list[i])
    diff = difflib.SequenceMatcher(None, result[i], result[i - 1]).quick_ratio()
    print("相似度："+str(diff))
    print(file_path + "/" + singlePicture)
    return diff





# 将图片list输出为wordlist
def pictureList_to_wordList(filePath):
    result = []
    wordList=[]
    i = 0  # 第几个视频
    studentPicture = find_student_picture(filePath)

    for singlePicture in studentPicture:
        try:
            picture_cut(filePath,filePath + "/" + singlePicture)
            OcrResult = picture_to_text(filePath+"/tempPicture.jpg")
            result.append(OcrResult)
            if i>0:
                diff = string_similar(result, filePath, singlePicture, i)
                wordList.append(diff)
            i = i + 1
        except UnidentifiedImageError:
            print(singlePicture)
    return wordList





# TODO 待修改
# -*- coding: utf-8 -*-




# if __name__=="__main__":
#     main()
