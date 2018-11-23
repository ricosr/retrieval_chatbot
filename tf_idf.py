# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class TfIdf:
    def __init__(self, config):
        self.config = config
        self.model_dict = {}
        self.vector_context_ls = []
        self.vector_utterrance_ls = []
        self.load_models(self.config)

    def load_models(self, config):
        for file_name, file_path in self.config.model_dict.items():
            self.model_dict[file_name] = joblib.load(file_path)

    def select_model(self, file_name):
        self.current_model = self.model_dict[file_name]

    def predict_tfidf(self, utterances, context_ls):
        for each_context in context_ls:
            self.vector_context_ls.append(self.current_model.transform([each_context[0] + each_context[1]]))
            self.vector_utterrance_ls.append(self.current_model.transform([utterances + each_context[1]]))

    def calculate_distances(self):
        result_ls = []
        for tfidf_c, tfidf_u in zip(self.vector_context_ls, self.vector_utterrance_ls):
            result_ls.append(self.calculate_cos_similarity(tfidf_c, tfidf_u))
        self.vector_utterrance_ls.clear()
        self.vector_context_ls.clear()
        return result_ls

    def calculate_cos_similarity(self, x, y):
        x = x.reshape(1, -1)
        y = y.reshape(1, -1)
        return cosine_similarity(x, y)


class TrainTfIdf:
    def __init__(self, config):
        self.config = config
        self.files_dict = {}

    def load_pickle(self):
        for file_name, path in self.config.file_dict.items():
            with open(path, 'rb') as fp:
                self.files_dict[file_name] = pickle.load(fp)

    def train(self):
        for file_name, content in self.files_dict.items():  # content:[[question], [answer]]
            for each_chat in content:
                vectorizer = TfidfVectorizer()
                vectorizer.fit(np.append(each_chat[0], each_chat[1]))
                joblib.dump(vectorizer, 'model/{}.pkl'.format(file_name))    # TODO: judge dir

