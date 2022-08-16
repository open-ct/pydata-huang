import numpy as np
import wave
import matplotlib.pyplot as plt
from scipy.fftpack import dct
f = wave.open(r"lantian.wav", "rb")
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
str_data = f.readframes(nframes)
signal = np.fromstring(str_data, dtype=np.short)
signal=signal*1.0/(max(abs(signal)))
signal_len=len(signal)
#预加重
signal_add=np.append(signal[0],signal[1:]-0.97*signal[:-1])   #预加重
time=np.arange(0,nframes)/1.0*framerate
#plt.figure(figsize=(20,10))
#plt.subplot(2,1,1)
#plt.plot(time,signal)
#plt.subplot(2,1,2)
#plt.plot(time,signal_add)
#plt.show()
#分帧
wlen=512
inc=128
N=512
if signal_len<wlen:
    nf=1
else:
    nf = int(np.ceil((1.0 * signal_len - wlen + inc) / inc))
pad_len=int((nf-1)*inc+wlen)
zeros=np.zeros(pad_len-signal_len)
pad_signal=np.concatenate((signal,zeros))
indices=np.tile(np.arange(0,wlen),(nf,1))+np.tile(np.arange(0,nf*inc,inc),(wlen,1)).T
indices=np.array(indices,dtype=np.int32)
frames=pad_signal[indices]
win=np.hanning(wlen)
m=24
s=np.zeros((nf,m))
for i in range(nf):
    x=frames[i:i+1]
    y=win*x[0]
    a=np.fft.fft(y)
    b=np.square(abs(a))
    mel_high=1125*np.log(1+(framerate/2)/700)
    mel_point=np.linspace(0,mel_high,m+2)
    Fp=700 * (np.exp(mel_point / 1125) - 1)
    w=int(N/2+1)
    df=framerate/N
    fr=[]
    for n in range(w):
        frs=int(n*df)
        fr.append(frs)
    melbank=np.zeros((m,w))
    for k in range(m+1):
        f1=Fp[k-1]
        f2=Fp[k+1]
        f0=Fp[k]
        n1=np.floor(f1/df)
        n2=np.floor(f2/df)
        n0=np.floor(f0/df)
        for j in range(w):
            if j>= n1 and j<= n0:
                melbank[k-1,j]=(j-n1)/(n0-n1)
            if j>= n0 and j<= n2:
                melbank[k-1,j]=(n2-j)/(n2-n0)
        for c in range(w):
            s[i,k-1]=s[i,k-1]+b[c:c+1]*melbank[k-1,c]
        plt.plot(fr, melbank[k - 1,])
plt.show()
logs=np.log(s)
num_ceps=12
D = dct(logs,type = 2,axis = 0,norm = 'ortho')[:,1 : (num_ceps + 1)]
print(D)
print(np.shape(D))
