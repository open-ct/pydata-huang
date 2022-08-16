import numpy
from gensim.models import KeyedVectors
import json
from collections import OrderedDict
from gensim.models import KeyedVectors
import pandas as pd
import numpy as np

'''
@InProceedings{N18-2028,
  author = 	"Song, Yan
		and Shi, Shuming
		and Li, Jing
		and Zhang, Haisong",
  title = 	"Directional Skip-Gram: Explicitly Distinguishing Left and Right Context for Word Embeddings",
  booktitle = 	"Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 2 (Short Papers)",
  year = 	"2018",
  publisher = 	"Association for Computational Linguistics",
  pages = 	"175--180",
  location = 	"New Orleans, Louisiana",
  url = 	"http://aclweb.org/anthology/N18-2028"
}
'''

def file_reader(path):
    # 读取excel文件
    df1 = pd.read_excel(path, sheet_name="190")
    df2 = pd.read_excel(path, sheet_name="110")
    df1 = np.array(df1)
    df2 =np.array(df2)
    print(df2)
    print(df1)
    search(df1,"190.xlsx")
    search(df2,"110.xlsx")
def search(df,name):
    list1=df.tolist()

    wordlist1=numpy.zeros(shape=(200,200))
    i=0
    for words in list1:
        for word in words:
            print(word)
            try:
                wordvec=wv_from_text.word_vec(word)
                print(wordvec)
                wordlist1[i] = wordvec
                i += 1
            except KeyError:
                print(word)
                print("not in the wordlist")
                i+=1

    print(i)
    data = pd.DataFrame(wordlist1)

    writer = pd.ExcelWriter(name)

    data.to_excel(writer, "page_1",index=False)
    writer.save()
    writer.close()
if __name__ == "__main__":
    wv_from_text = KeyedVectors.load_word2vec_format("tencent-ailab-embedding-zh-d200-v0.2.0-s.txt", binary=False)
    file_reader("词汇表.xlsx")

