# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import pickle
import os

import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib
from sklearn.metrics.pairwise import cosine_similarity


class TfIdf:
    def __init__(self, config):
        self.config = config
        self.model_dict = {}
        self.vector_context_ls = []
        self.vector_utterrance_ls = []
        self.load_models(self.config)

    def load_models(self, config):
        try:
            for file_name, file_path in self.config.model_dict.items():
                self.model_dict[file_name] = joblib.load(file_path)
        except Exception as e:
            pass

    def select_model(self, file_name):
        try:
            self.current_model = self.model_dict[file_name]
        except Exception as e:
            pass

    def predict_tfidf(self, utterances, context_ls):
        for each_context in context_ls:
            self.vector_context_ls.append(self.current_model.transform(
                [self.parse_cn_to_en_format(each_context[0]) + self.parse_cn_to_en_format(each_context[1])]))
            self.vector_utterrance_ls.append(self.current_model.transform(
                [self.parse_cn_to_en_format(utterances) + self.parse_cn_to_en_format(each_context[1])]))
            # print([self.parse_cn_to_en_format(each_context[0]) + self.parse_cn_to_en_format(each_context[1])])
            # print([self.parse_cn_to_en_format(utterances) + self.parse_cn_to_en_format(each_context[1])])

    def calculate_distances(self):
        result_ls = []
        for tfidf_c, tfidf_u in zip(self.vector_context_ls, self.vector_utterrance_ls):
            result_ls.append(self.calculate_cos_similarity(tfidf_c, tfidf_u))
        result_ls = self.normalization(result_ls)
        self.vector_utterrance_ls.clear()
        self.vector_context_ls.clear()
        return result_ls

    def calculate_cos_similarity(self, x, y):
        x = x.reshape(1, -1)
        y = y.reshape(1, -1)
        return cosine_similarity(x, y)

    def parse_cn_to_en_format(self, chinese_characters):
        seg_list = [each_word for each_word in jieba.cut(chinese_characters, cut_all=False)]
        return " ".join(seg_list)

    def normalization(self, ratio_ls):
        max_ratio = max(ratio_ls)
        min_ratio = min(ratio_ls)
        return [(each_ratio - min_ratio) / (max_ratio - min_ratio) for each_ratio in ratio_ls]


class TrainTfIdf:
    def __init__(self, config):
        self.config = config
        self.files_dict = {}

    def load_pickle(self, file=None):
        if file:
            with open(self.config.file_dict[file], 'rb') as fp:
                self.files_dict[file] = pickle.load(fp)
        else:
            for file_name, path in self.config.file_dict.items():
                with open(path, 'rb') as fp:
                    self.files_dict[file_name] = pickle.load(fp)

    def parse_cn_to_en_format(self, chinese_characters):
        seg_list = [each_word for each_word in jieba.cut(chinese_characters, cut_all=False)]
        return " ".join(seg_list)

    def train(self):
        if not os.path.exists("model"):
            os.mkdir("model")
        for file_name, content in self.files_dict.items():  # content:[[question], [answer]]
            tmp_content = map(lambda each_chat: map(self.parse_cn_to_en_format, each_chat), content)
            content_str_ls = [''.join(list(each_chat)) for each_chat in tmp_content]
            vectorizer = TfidfVectorizer()
            vectorizer.fit_transform(content_str_ls)
            joblib.dump(vectorizer, 'model/{}.pkl'.format(file_name))

