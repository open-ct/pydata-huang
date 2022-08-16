# This is a sample Python script.
import pandas as pd
import xlrd
import xlwt

list=[]

path="剔除不认真作答的问卷开放题.xls"
data=xlrd.open_workbook(path)
table=data.sheet_by_index(0)#通过索引顺序获取
output={}
word=0
singleWord={}
for r in range(table.nrows):#遍历行
    singleWord[r]= 0
    for l in range(table.ncols):#遍历列
        if table.cell(r, l).value!="":
            word = word + 1
            singleWord[r] = singleWord[r] + 1
            text=table.cell(r, l).value
            if text in output:
                output[text] = output[text]+1
            else:
                output[text] = 1

print("总词数："+str(word))
# print(output)
# print(len(output))
print(singleWord)

key = output.keys()
value = output.values()
print(key)
print(value)



MY_EXCEL = xlwt.Workbook(encoding='utf-8') # 创建MY_EXCEL对象
excelsheet = MY_EXCEL.add_sheet('sheet1')# 创建工作表（创建excel里面的工作表）
excelsheet.write(0,0,"情绪词")
excelsheet.write(0,1,"次数")
excelsheet.write(0,2,"答卷id")
excelsheet.write(0,3,"词数")
excelsheet.write(0,4,"总词数：")
excelsheet.write(0,5,str(word))

# 输出词和出现次数
i=1
for key,value in output.items():
        excelsheet.write(i,0,key)
        excelsheet.write(i,1,value)
        i=i+1

# 输出答卷和词数
i=1
for key,value in singleWord.items():
        excelsheet.write(i,2,key)
        excelsheet.write(i,3,value)
        i=i+1
MY_EXCEL.save("output1.xls")





#
# # 利用pandas模块先建立DateFrame类型，然后将两个上面的list存进去
# result_excel = pd.DataFrame()
# result_excel["词"] = key
# result_excel["词频"] = value
# # 写入excel
# result_excel.to_excel("1")

# import xlrd#导入xlrd库
# file='D:/杂货/编码数据.xlsx'#文件路径
# # wb=xlrd.open_workbook(filename=file)#用方法打开该文件路径下的文件
# # ws=wb.sheet_by_name("Sheet1")#打开该表格里的表单
# # dataset=[]
# for r in range(ws.nrows):#遍历行
#     col=[]
#     for l in range(ws.ncols):#遍历列
#         col.append(ws.cell(r, l).value)#将单元格中的值加入到列表中(r,l)相当于坐标系，cell（）为单元格，value为单元格的值
#     dataset.append(col)
# from pprint import pprint#pprint的输出形式为一行输出一个结果，下一个结果换行输出。实质上pprint输出的结果更为完整
# # pprint(dataset)