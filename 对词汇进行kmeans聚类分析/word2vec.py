import os
import xlrd  # 这个装1.2版本的
import numpy as np
import pandas as pd

from sklearn import metrics
from sklearn.cluster import KMeans




#TODO 请在此行写上需要进行k-means运行的文件夹或者文件。文件夹里必须只包含需要运行的文件
filePath = "/Users/artie/Downloads/test"

#聚类数，0就是不指定。
n_cluster=5


vec110 = pd.read_excel("110.xlsx", sheet_name="page1")
vec190 = pd.read_excel("190.xlsx", sheet_name="page1")

def os_file(path):
    filenames=os.listdir(path)
    print(filenames)
    for filename in filenames:
        file_reader(filePath+"/"+filename,filename)

def file_reader(path,filename):
    # 读取excel文件
    df1 = pd.read_excel(path, sheet_name="190词")
    df2 = pd.read_excel(path, sheet_name="110词")
    # print(df1)
    (result1,score1,bestI1,scores1)=kmeans_caculate(df1,vec190)
    (result2,score2,bestI2,scores2)=kmeans_caculate(df2,vec110)
    file_save(result1,"190词_"+filename,score1,bestI1,scores1)
    file_save(result2, "110词_" + filename,score2,bestI2,scores2)

def kmeans_caculate(df1,vec):
    df1 = np.array(df1)
    vec = np.array(vec)
    # 把word和数组分开
    word = df1[:, 0]
    data = np.delete(df1, 0, axis=1)
    data=np.hstack((data,vec))
    # print(word)
    # print(data)
    # print("-------------------------")
    maxScore = 0
    maxI =-1
    scores = []
    for i in range(2,80):
        kmean=KMeans(n_clusters=i)
        kmeans=kmean.fit(data)


        result=kmeans.labels_

        #测出性能指标
        y_predict = kmean.predict(data)
        score = metrics.calinski_harabasz_score(data, y_predict)


        print(score)
        if i ==4:
            maxScore=score
            BestResult=result
            bestI=i
        scores.append(score)
    result=np.stack([word,BestResult],axis=1)

    return result,maxScore,bestI,scores

def file_save(result,path,score,bestI,scores):
    data = pd.DataFrame(result)
    for k in range(len(scores)):
        print(len(scores))
        data.loc[k,4]=k+2
        data.loc[k,5]=scores[k]
    print(data)
    data.loc[0,6] = score
    data.loc[1,6] = "选用的分类="+str(bestI)
    print(data)
    writer = pd.ExcelWriter(str(bestI)+"_分类_result_"+path)

    data.to_excel(writer, "page_1",header=['名称','所在类别','n_cluster','CH','选用的CH'],index=False)
    writer.save()
    writer.close()
    print("-------")


if __name__ == "__main__":

    if os.path.exists(filePath):
        if    os.path.isdir(filePath):
            os_file(filePath)
        else:
            file_reader(filePath,filePath)
    else:
        print("请输入正确的文件或者文件夹名称")

