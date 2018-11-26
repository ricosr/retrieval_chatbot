# coding:utf-8

import sys
import gensim
import numpy as np
import pickle
import jieba

from gensim.models.doc2vec import Doc2Vec, LabeledSentence
from sklearn.cluster import KMeans

TaggededDocument = gensim.models.doc2vec.TaggedDocument


def get_datasest():
    with open("../data/xiaohuangji.pkl", "rb") as fp:
        docs = pickle.load(fp)[:1000]
        print(len(docs))

    x_train = []
    # y = np.concatenate(np.ones(len(docs)))
    for i, text in enumerate(docs):
        line = text[0] + text[1]
        line = line.strip('\n')
        word_list = list(jieba.cut(line))
        l = len(word_list)
        word_list[l - 1] = word_list[l - 1].strip()
        document = TaggededDocument(word_list, tags=[i])
        x_train.append(document)

    return x_train


def train(x_train, size=200, epoch_num=1):
    model_dm = Doc2Vec(x_train, min_count=1, window=3, size=size, sample=1e-3, negative=5, workers=4)
    model_dm.train(x_train, total_examples=model_dm.corpus_count, epochs=100)
    model_dm.save('model_dm')

    return model_dm


def cluster(x_train):
    infered_vectors_list = []
    print("load doc2vec model...")
    model_dm = Doc2Vec.load("model_dm")
    print("load train vectors...")
    i = 0
    for text, label in x_train:
        vector = model_dm.infer_vector(text)
        infered_vectors_list.append(vector)
        i += 1

    print("train kmean model...")
    kmean_model = KMeans(n_clusters=15)
    kmean_model.fit(infered_vectors_list)
    labels = kmean_model.predict(infered_vectors_list[0:100])
    cluster_centers = kmean_model.cluster_centers_

    with open("own_claasify.txt", 'w', encoding="utf-8") as wf:
        for i in range(100):
            string = ""
            text = x_train[i][0]
            for word in text:
                string = string + word
            string = string + '\t'
            string = string + str(labels[i])
            string = string + '\n'
            wf.write(string)
    tmp_vector = model_dm.infer_vector("可以做我女朋友吗？")
    labels = kmean_model.predict(tmp_vector.reshape(1, -1))
    print(labels)

    return cluster_centers


if __name__ == '__main__':
    x_train = get_datasest()
    model_dm = train(x_train)
    cluster_centers = cluster(x_train)
