import datetime
from csv import reader

import numpy
import numpy as np
import time
import matplotlib.pyplot as plt
import pandas as pd

filename = 'shuju1.csv'

with open(filename, 'rt', encoding='UTF-8') as raw_data:
    readers = reader(raw_data, delimiter=',')
    x = list(readers)
    data = np.array(x)
    # print(data)
    # print(data.shape)
    # print(data[:,2])
    # print(data[:,3])
    start=data[:,2]
    end=data[:,3]
    id=data[:,1]
    # p="2022-06-20T09:32:04.524+08:00"
    start1=[]
    format1 = "%Y-%m-%dT%H:%M:%S.%f+08:00"
    format2= "%Y-%m-%dT%H:%M:%S+08:00"
    # t1 = time.strptime(p, format1)
    for x in start:
        if x!= "":
            t1 = time.strptime(x, format1)
            t2= time.mktime(t1)
        else:
            t2=0
        start1.append(t2)
    a=0
    for y in end:
        if y!= "" and y!="2022-06-22T12:12:39+08:00":
            t1 = time.strptime(y, format1)
            t2= time.mktime(t1)

            if start1[a]!=0:
                start1[a]=t2-start1[a]
        else:
            start1[a]=0
        a=a+1
    start1=list(filter(None,start1))

    result=numpy.array(start1)


    result.sort()

    print(type(a))
    print(np.mean(result))
    print(np.var(result))



    print(result.size)
    list=range(result.size)
    i=iter(list)
    number =numpy.fromiter(i,dtype=float)
    # plt.scatter(result,id,0.1)
    # plt.show()

bins = [1,300,600,900,1200,1500,1800,2100,2400,2700,15000]
bins_res = pd.cut(result,bins)
print(bins_res)
print(pd.value_counts(bins_res))
bins1 = [300,600,900,1200,1500,1800,2100,2400,2700,10000]
plt.plot(bins1,pd.value_counts(bins_res))
plt.show()
plt.pie(pd.value_counts(bins_res),
        labels=bins1, # 设置饼图标签
       )
plt.show()