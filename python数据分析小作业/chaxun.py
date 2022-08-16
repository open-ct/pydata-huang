import requests
from csv import reader
import numpy as np
import time
from openpyxl import Workbook

filename = 'shuju1.csv'

def checkip(ip):
    r = requests.get('https://api.ip138.com/ip/?ip=%s&datatype=jsonp&token=7e49bdb8f9a7916c61b5ec01b81f367a' % ip)
    if r.json()['ret'] == 'ok':
        i = r.json()['data']
        country = i[0]
        province = i[1]
        city = i[2]
        print(country + ' ' + province + ' ' + city)
    else:
        print('未查到归属地')







with open(filename, 'rt', encoding='UTF-8') as raw_data:
    readers = reader(raw_data, delimiter=',')
    x = list(readers)
    data = np.array(x)
    # print(data)
    # print(data.shape)
    # print(data[:,2])
    # print(data[:,3])
    ip=data[:,5]
    # print(ip)
    b=[]
    for a in ip:
        ipa=checkip(a)

        b.append(ipa)

    print(b)



