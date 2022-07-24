# pip3 install xlwt -i https://pypi.tuna.tsinghua.edu.cn/simple
# pip3 install xlrd -i https://pypi.tuna.tsinghua.edu.cn/simple

import xlrd  # 导入库
import xlwt
import pandas as pd
import numpy as np
import datetime
import time


def put_in():
    source_data = pd.read_csv("数据收集-ds (9).csv")
    list = source_data.values.tolist()

    reasons = []
    details = []

    for student in list:

        reason = [student[0], student[1]]

        if student[5] != "完成":  # 判断完成
            reason += ["不合格"]
            reason += ["未完成"]

        # 这部分是对作答时间的判断，如果在时间内，则提示问题。
        # format1 = "%Y-%m-%d%H:%M:%S.%f"
        format2 = '%Y-%m-%d%H:%M:%S'
        format4 = '%Y/%m/%d%H:%M'
        # format3 = "%Y-%m-%d %H:%M:%S.%.2f\r\n"
        student[4] = str(student[4]).replace(" ", "")
        student[3] = str(student[3]).replace(" ", "")

        try:
            if str(student[4]) != "nan" and str(student[3]) != "nan" and str(student[4]) != "" and str(
                    student[3]) != "":
                time1 = time.mktime(time.strptime((student[4])[:18], format2)) - time.mktime(
                    time.strptime((student[3])[:18], format2))
                if time1 < 600:          # 这是作答时间，600s就是10分钟
                    reason += ["不合格"]
                    reason += ['作答时间过短']
                    reason += ['作答时间为' + str(time1) + 's']
                    print(reason)
                else:
                    print("没问题")
        except ValueError:
            # 只有分没有秒的情况
            # 只有分没有秒的情况
            time1 = time.mktime(time.strptime(student[4], format4)) - time.mktime(
                time.strptime(student[3], format4))
            if time1 < 600:  # 这是作答时间，600s就是10分钟
                reason += ["不合格"]
                reason += ['作答时间过短']
                reason += ['作答时间为' + str(time1) + 's']
                print(reason)
            else:
                print("没问题")

        cehuangti = [
            [41, 2],
            [101, 4],
            [177, 4],
            [234, 2],
            [294, 4],
            [370, 4],
            [427, 2],
            [487, 4],
            [563, 4],
            [620, 2],
            [680, 4],
            [756, 4],
            [813, 2],
            [873, 4],
            [949, 4],
        ]

        zuocuodecehuangti = []
        for i in cehuangti:
            if i[0] <= len(student) and student[i[0]] != i[1]:
                zuocuodecehuangti += [i[0]]
        if len(zuocuodecehuangti) > 0:
            reason += ["不合格"]
            reason += ["测谎题作答错误"]
            reason += ["：错误的题号为：" + str(zuocuodecehuangti)]

        last = "0"
        count = 0
        maxcount = 0
        items = 0
        i = 0
        for ans in student:
            i += 1
            if ans == last:
                count += 1
            else:
                count = 0
            if count > maxcount:
                maxcount = count
                items = i
            last = ans
        if maxcount > 15:  # TODO 连续多少个元素一致 可以改数字
            reason += ["不合格"]
            reason += ["作答规律性过强"]
            reason += ["：连续%d个元素一致,在%d列出现" % (maxcount, items - count)]

        for i in range(1, 5):
            if student.count(1) > len(student) * 0.7:
                reason += ["不合格"]
                reason += ["作答规律性过强"]
                reason += ["：超过70%题目选择同一选项"]

        reasons.append(reason)

    curr_time = datetime.datetime.now()
    output = open("out_" + str(curr_time.day) + "日" +
                  str(curr_time.hour) + "时" +
                  str(curr_time.minute) + "分" +
                  str(curr_time.second) + "秒"
                                          ".xls"
                  , 'w', encoding='gbk')
    output.write('准考证号\t姓名\t是否合格\t不合格原因\n')
    for i in range(len(reasons)):
        for j in range(len(reasons[i])):
            output.write(str(reasons[i][j]))  # write函数不能写int类型的参数，所以使用str()转化
            output.write('\t')  # 相当于Tab一下，换一个单元格
        output.write('\n')  # 写完一行立马换行
    output.close()
    print("已成功输出 out_" + str(curr_time.day) + "日" +
          str(curr_time.hour) + "时" +
          str(curr_time.minute) + "分" +
          str(curr_time.second) + "秒"
                                  ".xls")

    # #  将数据写入新文件
    # f = xlwt.Workbook()
    # sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet

    # i = 0
    # num = 0
    # for every in d:
    #     sheet1.write(i, 0, every)
    #     # sheet1.write(i, 1, d[every])
    #     for j in range(len(d[every])):
    #         sheet1.write(i, d[every][j], d[every][j])
    #     i = i + 1
    #
    #
    # curr_time = datetime.datetime.now()
    #
    # f.save("out_" +  str(curr_time.day) +
    #                     str(curr_time.hour) +
    #                     str(curr_time.minute) +
    #                     str(curr_time.second) +
    #                     ".xls"
    #                     )  # 保存文件
    # print(f"结果已输出在out文件中")
    #
    # print(f"输入文件共 {num_sources} 个")
    # print(f"输入文件去重后共 {len(d)} 个")


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    put_in()
