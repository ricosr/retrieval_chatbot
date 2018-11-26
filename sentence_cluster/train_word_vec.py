# -*-coding:utf-8-*-

import pickle

import jieba
import gensim
import numpy as np
from sklearn.cluster import KMeans

# get input file,text format
with open("../data/xiaohuangji.pkl", "rb") as fp:
    data_lines = pickle.load(fp)[:1000]
count = len(data_lines)
print('源文件行数为：'+str(count))

#read file and seperate words
output = open('output.seq', 'w', encoding='utf-8')
for each_ls in data_lines:
    line = each_ls[0] + each_ls[1]
    line = line.strip('\n')
    seg_list = jieba.cut(line)
    output.write(' '.join(seg_list)+'\n')

#训练并保存模型
sentences = gensim.models.doc2vec.TaggedLineDocument('output.seq')
model = gensim.models.Doc2Vec(sentences, vector_size=100, window=3)
model.train(sentences, epochs=20, total_examples=model.corpus_count)
model.save('all_model.txt')

num_clusters=10 #设定聚类个数
km=KMeans(n_clusters=num_clusters)  #设置模型参数
result=km.fit_predict(model.docvecs)  #用doc2vec训练的模型产生的句向量作为k-means的输入

#将聚类预测结果和具体文档处理对应上
# f1=open('legal_data_raw.txt','r')
f2=open('legal_data_clustering_result.txt','w')
for i in range(num_clusters):
    for linenumber,eachline in enumerate(data_lines):
        if linenumber>=len(result):
            break
        if result[linenumber]==i:
            f2.write(eachline+'\n')
    f2.write(str(i)+'---------------------hello-----------------------------\n')

