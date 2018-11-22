# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import pickle
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib


class TfIdf:
    def __init__(self, config):
        self.load_models(model_path)
        pass

    def load_models(self, model_path):
        pass

    def calculate_distances(self):
        best_index = ''
        return best_index

    def calculate_tfidf(self, utterances, contexts):
        pass

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

