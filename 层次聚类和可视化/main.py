# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
import pandas as pd
filePath= "file1"   #输入文件夹
bigname=111
# -*- coding: utf-8 -*-
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster, set_link_color_palette
from matplotlib import pyplot as plt

def os_file(path):   #遍历输入文件夹有多少个文件
    filenames = os.listdir(path)

    for filename in filenames:
        print(filename)
        filename1=filename[0:-5]    #删掉了文件后缀
        print(filename1)
        if filename!=".DS_Store":
            file_reader(filePath + "/" + filename,filename1)


def file_reader(path,name):
    df1 = pd.read_excel(path, sheet_name="Sheet1")  #输入的文件必须放在Sheet1
    df1 = np.array(df1)
    importance=df1[-1,:]        #获取最后一行的所有列信息（权重）
    importance = np.delete(importance, 0, axis=0)
    df1=df1[0:-1,:]      #获取除了权重行的所有数据
    #print(importance)

    # 把word和数组分开
    word = df1[:, 0]    #获取第一列所有行（词）
    data = np.delete(df1, 0, axis=1)   #获取除第一列的其他列信息（打分）
   # print("data1")
    #print(data)
    data=data*importance  #权重与数值相乘
    #print(word)
    #print("data2")
    #print(data)
    nums,indics=hierarchy_cluster(data,word,name)
    print(indics)
    for i in range(len(indics)):
        group = "为一组"
        for j in range(len(indics[i])):
            group=word[indics[i][j]]+" "+group
        print(group)









def hierarchy_cluster(data,word,name, method='complete', threshold=600.0):  #complete-linkage
    '''层次聚类

    Arguments:
        data [[0, float, ...], [float, 0, ...]] -- 文档 i 和文档 j 的距离

    Keyword Arguments:
        method {str} -- [linkage的方式： single、complete、average、centroid、median、ward] (default: {'average'})
        threshold {float} -- 聚类簇之间的距离
    Return:
        cluster_number int -- 聚类个数
        cluster [[idx1, idx2,..], [idx3]] -- 每一类下的索引
    '''
    data = np.array(data)
    plt.figure(figsize=(10, 15), dpi=300)      #代表宽和高的尺寸，dpi代表分辨率
    Z = linkage(data, method=method,metric='euclidean')      #欧式距离公式

    cluster_assignments = fcluster(Z, threshold, criterion='distance')


    num_clusters = cluster_assignments.max()

    indices = get_cluster_indices(cluster_assignments)
    z = linkage(data, method='ward')
    print(z.shape)
    dendrogram(z, labels=word, color_threshold=80,orientation='right', leaf_font_size=8,above_threshold_color='black')
    set_link_color_palette(['#0000FF', '#4A766E', '#2F4F4F','871F78','FF7F00','E47833','FF6666','FFCCFF'])  #color_threshold是画线位置；orientation调成left图换方向
    #n_clusters=10                                                     #leaf_font_size词间距
    #color_threshold=25

    plt.grid(True, which='minor', ls='--')        #minor代表不显示网格线，major代表显示
    #name = "college"    #设置图片标题
    plt.title(name, fontdict={'fontproperties':'Times New Roman','size': 10}) #标题的字体字号
    plt.yticks(fontproperties='Times New Roman', size=8)  #设置y轴字体和字号，大小及加粗
    plt.xticks(fontproperties='Times New Roman', size=8)
    plt.plot(linewidth = '0.5')    #设置线粗细

    f = plt.gcf()

    f.savefig(name + ".png")
    plt.show()
    f.clear()

    return num_clusters,indices


def get_cluster_indices(cluster_assignments):   #层次聚类的实现函数
    '''映射每一类至原数据索引

    Arguments:
        cluster_assignments 层次聚类后的结果

    Returns:
        [[idx1, idx2,..], [idx3]] -- 每一类下的索引
    '''
    n = cluster_assignments.max()
    indices = []
    for cluster_number in range(1, n + 1):
        indices.append(np.where(cluster_assignments == cluster_number)[0])

    return indices


if __name__ == "__main__":
    os_file(filePath)
