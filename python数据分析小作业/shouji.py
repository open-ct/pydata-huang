from csv import reader
import numpy as np
from user_agents import parse
from pyecharts import options as opts
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
from pyecharts.charts import Pie
import stylecloud

filename = 'shuju1.csv'

with open(filename, 'rt', encoding='UTF-8') as raw_data:
    readers = reader(raw_data, delimiter=',')
    x = list(readers)
    data = np.array(x)
    shouji = data[:, 4]
    #print(shouji)
    a=0

phone=[]
system=[]
browser=[]
#Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.9 Safari/537.36
for x in shouji :
    a=a+1
    ua_string =x
    user_agent = parse(ua_string)

# # 浏览器属性
# print(user_agent.browser)  # Browser(family='Mobile Safari', version=(5, 1), version_string='5.1')
# print(user_agent.browser.family)  # 'Mobile Safari'
# print(user_agent.browser.version)  # (5, 1)
# print(user_agent.browser.version_string)  # '5.1'
#
# # 操作系统属性
# print(user_agent.os)  # OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
# print(user_agent.os.family)  # 'iOS'
# print(user_agent.os.version)  # (5, 1)
# print(user_agent.os.version_string)  # '5.1'
#
# 设备属性
#     print(user_agent.device)  # Device(family=u'iPhone', brand=u'Apple', model=u'iPhone')
#     print(user_agent.device.family)  # 'iPhone'
#     print(user_agent.device.brand)  # 'Apple'
#     print(user_agent.device.model)  # 'iPhone'
#
# # 美观的字符串版本
#     print(a)
#     print(str(user_agent))  # "iPhone / iOS 5.1 / Mobile Safari 5.1"
    phone.append(user_agent.device.family)
    system.append(user_agent.os.family)
    browser.append(user_agent.browser.family)
# print(phone)

phone1=np.array(phone)
print(np.unique(phone1))

values = phone1
value_cnt = {}  # 将结果用一个字典存储
# 统计结果

for value in values:
	# get(value, num)函数的作用是获取字典中value对应的键值, num=0指示初始值大小。
	value_cnt[value] = value_cnt.get(value, 0) + 1

# 打印输出结果
print(value_cnt)
print([key for key in value_cnt.keys()])
print([value for value in value_cnt.values()])


stylecloud.gen_stylecloud(file_path='111',
                          icon_name='fas fa-apple-alt',
                          colors='white',
                          background_color='black',
                          output_name='apple.png',
                          collocations=False)

# print(browser)
# print(system)

