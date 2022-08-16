import librosa
import numpy as np
import soundfile






def extract_feature(file_name, mfcc, chroma, mel):
    '''
    2.定义一个函数extract_feature从声音文件中提取mfcc，chroma和mel特征。此函数采用4个参数-文件名和3个布尔参数用于这三个特征：

    mfcc：梅尔频率倒谱系数，表示声音的短期功率谱
    chroma：属于12种不同的音高等级
    mel：梅尔频谱图频率
    使用with-as通过soundfile.SoundFile打开声音文件，这样一旦完成，将会自动关闭。从中读取
    并命名为X。同时得到采样率。如果chroma为True，则获取X的Short-Time傅立叶变换。

    让结果为一个空的numpy数组。现在，对于这三个特征中的每个特征（如果存在），从librosa.feature（
    例如，对于mfcc为librosa.feature.mfcc）调用相应的函数，并获取平均值。从numpy中调用带有结果和特征值的函
    数hstack（），并将其存储在结果中。hstack（）按水平顺序（以柱状方式）堆叠数组。然后，返回结果。
    '''
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate=sound_file.samplerate
        if chroma:
            stft=np.abs(librosa.stft(X))

        result=np.array([])
        if mfcc:
            mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result=np.hstack((result, mfccs))
        if chroma:
            chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result=np.hstack((result, chroma))
        if mel:
            mel=np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
            result=np.hstack((result, mel))

	return result
