import os
import wave
import numpy as np
import pylab as plt
import librosa

path = "../wav"
files = os.listdir(path)
files = [path + "/" + f for f in files if f.endswith('.wav')]
CutTime = 10  # 单位长度4s


def CutAudios():
    for i in range(len(files)):
        FileName = files[i]
        f = wave.open(r"" + FileName, 'rb')
        params = f.getparams()  # 读取音频文件信息
        nchannels, sampwidth, framerate, nframes = params[:4]  # 声道数, 量化位数, 采样频率, 采样点数
        str_data = f.readframes(nframes)
        f.close()

        wave_data = np.frombuffer(str_data, dtype=np.short)
        # 根据声道数对音频进行转换
        if nchannels > 1:
            wave_data.shape = -1, 2
            wave_data = wave_data.T
            temp_data = wave_data.T
        else:
            wave_data = wave_data.T
            temp_data = wave_data.T

        CutFrameNum = framerate * CutTime
        Cutnum = nframes / CutFrameNum  # 音频片段数
        StepNum = int(CutFrameNum)
        StepTotalNum = 0

        for j in range(int(Cutnum)):
            FileName = r"cut_result" + files[i][-17:-4] + "-" + str(j) + ".wav"
            temp_dataTemp = temp_data[StepNum * (j):StepNum * (j + 1)]
            StepTotalNum = (j + 1) * StepNum
            temp_dataTemp.shape = 1, -1
            temp_dataTemp = temp_dataTemp.astype(np.short)  # 打开WAV文档
            f = wave.open(FileName, 'wb')
            # 配置声道数、量化位数和取样频率
            f.setnchannels(nchannels)
            f.setsampwidth(sampwidth)
            f.setframerate(framerate)
            f.writeframes(temp_dataTemp.tobytes())  # 将wav_data转换为二进制数据写入文件
            f.close()


if __name__ == '__main__':
    CutAudios()

