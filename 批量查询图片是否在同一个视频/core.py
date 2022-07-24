import os
import shutil
import time



from textSimilar import pictureList_to_wordList, find_student_picture
from hashSimilar import picture_to_hash

from concurrent.futures import ThreadPoolExecutor

from control import *


def create_dir(file_path, WORD_DIFFERENT=WORD_DIFFERENT, HASH_DIFFERENT=HASH_DIFFERENT):
    k=1#第几个文件夹
    #使用hash
    hashSimilarList=picture_to_hash(file_path)
    #使用ocr
    wordList=pictureList_to_wordList(file_path)

    studentPicture=find_student_picture(file_path)

    if not os.path.exists(file_path + "/视频" + str(k)):
        os.makedirs(file_path + "/视频" + str(k))
        shutil.copy(file_path + "/" + studentPicture[0], file_path + "/视频" + str(k))
    for i in range(len(hashSimilarList)):
        # TODO 在某个条件下，默认是两个都要小于某个值
        if  wordList[i]< WORD_DIFFERENT and hashSimilarList[i]<HASH_DIFFERENT:
            k = k + 1
            isExists = os.path.exists(file_path + "/视频" + str(k))
            if not isExists:
                os.makedirs(file_path + "/视频" + str(k))
        shutil.copy(file_path + "/" + studentPicture[i+1], file_path + "/视频" + str(k))
    return k





if __name__ == "__main__":
    #create_dir(file_path=DEFAULT_PATH)
    allFile = os.listdir(DEFAULT_PATH)
    thread_pool = ThreadPoolExecutor(max_workers=THREAD)
    print(allFile)
    for i in allFile:
        # create_dir(DEFAULT_PATH+"/"+i)
        thread_pool.submit(create_dir, DEFAULT_PATH+"/"+i)
        print(DEFAULT_PATH+"/"+i)
