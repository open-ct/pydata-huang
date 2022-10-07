
import librosa
import os
from random import shuffle
import numpy as np
import pandas as pd
import pandas.core.ops
from sklearn import svm
import joblib
import sklearn
import logmmse
import wave

from natsort import natsorted
import warnings
warnings.filterwarnings('ignore')

path = r'trainset/casio2'
EMOTION_LABEL = {
    'angry': '1',
    'Delate': '2',
    'disgust': '3',
    'fear': '4',
    'happy': '5',
    'neutral': '6',
    'sad':'7',
    'surprised':'8',
    'TS':'9'
}


# C:误差项惩罚参数,对误差的容忍程度。C越大，越不能容忍误差
# gamma：选择RBF函数作为kernel，越大，支持的向量越少；越小，支持的向量越多
# kernel: linear, poly, rbf, sigmoid, precomputed
# decision_function_shape: ovo, ovr(default)
#
# #

'''
这个模块包含了导入模块和svm模块
导入模块需要librosa，始终有问题，草。
'''

def getFeature(path, mfcc_feature_num=16):
    y, sr = librosa.load(path)

    # 对于每一个音频文件提取其mfcc特征
    # y:音频时间序列;
    # n_mfcc:要返回的MFCC数量
    mfcc_feature = librosa.feature.mfcc(y, sr, n_mfcc=16)
    zcr_feature = librosa.feature.zero_crossing_rate(y)
    energy_feature = librosa.feature.rms(y)
    rms_feature = librosa.feature.rms(y)

    mfcc_feature = mfcc_feature.T.flatten()[:mfcc_feature_num]
    zcr_feature = zcr_feature.flatten()
    energy_feature = energy_feature.flatten()
    rms_feature = rms_feature.flatten()

    zcr_feature = np.array([np.mean(zcr_feature)])
    energy_feature = np.array([np.mean(energy_feature)])
    rms_feature = np.array([np.mean(rms_feature)])

    data_feature = np.concatenate((mfcc_feature, zcr_feature, energy_feature,
                                   rms_feature))

    return data_feature


def deNoise(path):
    f = wave.open(path, "r")
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    #print("nchannels:", nchannels, "sampwidth:", sampwidth, "framerate:", framerate, "nframes:", nframes)
    data = f.readframes(nframes)
    f.close()
    data = np.fromstring(data, dtype=np.short)

    # 降噪
    data = logmmse.logmmse(data=data, sampling_rate=framerate)


    # 保存音频
    file_save = "save"+path
    nframes = len(data)
    f = wave.open(file_save, 'w')
    f.setparams((1, 2, framerate, nframes, 'NONE', 'NONE'))  # 声道，字节数，采样频率，*，*
    # print(data)
    f.writeframes(data)  # outData
    f.close()

def getData(mfcc_feature_num=16):
    """找到数据集中的所有语音文件的特征以及语音的情感标签"""
    wav_file_path = []
    person_dirs = os.listdir(path)
    for person in person_dirs:
        if person.endswith('txt'):
            continue
        emotion_dir_path = os.path.join(path, person)
        emotion_dirs = os.listdir(emotion_dir_path)
        for emotion_dir in emotion_dirs:
            if emotion_dir.endswith('.ini'):
                continue
            emotion_file_path = os.path.join(emotion_dir_path, emotion_dir)
            emotion_files = os.listdir(emotion_file_path)
            for file in emotion_files:
                if not file.endswith('wav'):
                    continue
                wav_path = os.path.join(emotion_file_path, file)
                wav_file_path.append(wav_path)

    # 将语音文件随机排列
    shuffle(wav_file_path)
    data_feature = []
    data_labels = []


    for wav_file in wav_file_path:

        #deNoise(wav_file)

        data_feature.append(getFeature("save"+wav_file, mfcc_feature_num))
        data_labels.append(int(EMOTION_LABEL[wav_file.split('/')[-2]]))

    return np.array(data_feature), np.array(data_labels)


def getData1(mfcc_feature_num,path):
    """找到数据集中的所有语音文件的特征以及语音的情感标签"""


    wav_file_path = []
    person_dirs = os.listdir(path)
    for person in person_dirs:
        if person.endswith('txt') :
            continue
        emotion_dir_path = os.path.join(path, person)
        emotion_dirs = os.listdir(emotion_dir_path)
        for emotion_dir in emotion_dirs:
            if emotion_dir.endswith('.ini'):
                continue
            emotion_file_path = os.path.join(emotion_dir_path, emotion_dir)
            emotion_files = os.listdir(emotion_file_path)
            emotion_files=natsorted(emotion_files)
            for file in emotion_files:
                if not file.endswith('wav'):
                    continue
                wav_path = os.path.join(emotion_file_path, file)
                wav_file_path.append(wav_path)

    # 将语音文件随机排列

    data_feature = []
    data_labels = []


    for wav_file in wav_file_path:

        data_feature.append(getFeature(wav_file, mfcc_feature_num))

    return np.array(data_feature),wav_file_path

def train():
    # 使用svm进行预测
    best_acc = 0
    best_mfcc_feature_num = 0
    best_C = 0

    for C in range(13, 20):
        for i in range(40, 55):
            data_feature, data_labels = getData(i)
            split_num = 200
            train_data = data_feature[:split_num, :]
            train_label = data_labels[:split_num]
            test_data = data_feature[split_num:, :]
            test_label = data_labels[split_num:]
            clf = svm.SVC(
                decision_function_shape='ovo',
                kernel='rbf',
                C=C,
                gamma=0.0003,
                probability=True)
            print("train start")
            clf.fit(train_data, train_label)
            print("train over")
            print(C, i)
            acc_dict = {}
            for test_x, test_y in zip(test_data, test_label):
                pre = clf.predict([test_x])[0]
                if pre in acc_dict.keys():
                    continue
                acc_dict[pre] = test_y
            acc = sklearn.metrics.accuracy_score(
                clf.predict(test_data), test_label)
            if acc > best_acc:
                best_acc = acc
                best_C = C
                best_mfcc_feature_num = i
                print('best_acc', best_acc)
                print('best_C', best_C)
                print('best_mfcc_feature_num', best_mfcc_feature_num)
                print()


            # 保存模型
            joblib.dump(clf,
                        'Models/C_' + str(C) + '_mfccNum_' + str(i) + '.m')

    print('most_best_acc', best_acc)
    print('best_C', best_C)
    print('best_mfcc_feature_num', best_mfcc_feature_num)


def getData2(path):
    data_features,wavefile = getData1(52,path)
    label=[]
    for data_feature in data_features:
        new_svm2 = joblib.load('Models/C_16_mfccNum_52.m')

        kk=new_svm2.predict(data_feature.reshape(1,-1))
        label.append(str(kk[0]))

    print(label)
    return label,wavefile

def run():
    paths = ["wav/1-1", "wav/1-2", "wav/1-5", "wav/1-7", "wav/1-14"]

    for path in paths:
        label, wavefile = getData2(path)
        emotions = []
        for labe in label:
            if labe == "1":
                emotions.append('angry')
            elif labe == "2":
                emotions.append('Delate')
            elif labe == "3":
                emotions.append('disgust')
            elif labe == "4":
                emotions.append('fear')
            elif labe == "5":
                emotions.append('happy')
            elif labe == "6":
                emotions.append('neutral')
            elif labe == "7":
                emotions.append('sad')
            elif labe == "8":
                emotions.append('surprised')
            elif labe == "9":
                emotions.append('TS')

        c = {"label": label, "wavefile": wavefile, "emotions": emotions}
        mySeries = pandas.DataFrame(c)
        writer = pd.ExcelWriter(path + ".xlsx")  # 初始化一个writer
        mySeries.to_excel(writer, float_format='%.5f')  # table输出为excel, 传入writer
        writer.save()  # 保存

if __name__ == "__main__":

    train()



