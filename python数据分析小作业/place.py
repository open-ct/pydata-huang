import requests
from csv import reader
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker

filename = 'aaa.csv'

with open(filename, 'rt', encoding='UTF-8') as raw_data:
    readers = reader(raw_data, delimiter=',')
    x = list(readers)
    data = np.array(x)
    # print(data)
    # print(data.shape)
    # print(data[:,2])
    # print(data[:,3])
    place=data[:,17]


values = place

value_cnt = {}  # 将结果用一个字典存储
# 统计结果

for value in values:
	# get(value, num)函数的作用是获取字典中value对应的键值, num=0指示初始值大小。
	value_cnt[value] = value_cnt.get(value, 0) + 1

# 打印输出结果
print(value_cnt)
print([key for key in value_cnt.keys()])
print([value for value in value_cnt.values()])
lables = value_cnt.keys()
counts = value_cnt.values()
#一次性遍历两个列表
china_data = [list(z) for z in zip (lables,counts)]

C = Map()
#调用数据
C.add("ip来源",china_data,'china')
C.set_global_opts(visualmap_opts=opts.VisualMapOpts(max_=100),title_opts=opts.TitleOpts(title="大学老师ip地址所在地"))
#设置保存的位置
C.render('t4.html')
C.render_notebook()