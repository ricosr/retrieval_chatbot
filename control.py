# -*- coding: utf-8 -*-

# Copyright (c) by 2018 Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

from random import choice

import jieba
from gensim.models.doc2vec import Doc2Vec, LabeledSentence
from sklearn.externals import joblib

from retrieval_documents import Retrieval
from fuzzy_match import fuzzy_matching, fuzzy_for_domains
from tf_idf import TfIdf
from config import config, frequency_domain

# TODO: distribute message by threading or tornado

NUM_OF_IR = 2

class Agent:
    def __init__(self):
        self.config = config
        self.punctuation_str = ''.join(self.config.punctuation_ls)
        self.frequency_domain_dict = frequency_domain.frequency_dict
        self.cluster_md = self.config.cluster_model
        self.vec_md = self.config.doc_vector_model
        self.init_all_states()
        self.fuzzy_weight = 0.7
        self.tf_idf_weight = 0.3
        # self.record_chat_ls = [] # TODO

    def init_all_states(self):
        self.retrieval = Retrieval(num_ir=NUM_OF_IR, config=self.config)
        self.tf_idf = TfIdf(self.config)
        # TODO: wait for models
        self.cluster_model = joblib.load(self.cluster_md)
        self.vec_model = Doc2Vec.load(self.vec_md)
        jieba.initialize()

    def select_domain(self, utterance):
        utterance_words = [each_word for each_word in jieba.cut(utterance, cut_all=False)]
        for each_word in utterance_words:
            if each_word in self.frequency_domain_dict.keys() and len(each_word) > 1:
                return "domains"
        return "xiaohuangji"

    def get_utterance_type(self, utterance):
        # TODO: wait for models
        tmp_vector = self.vec_model.infer_vector(utterance)
        label = self.cluster_model.predict(tmp_vector.reshape(1, -1))
        return self.config.cluster_file[label[0]]

    def record_good_chat(self):
        pass       # TODO: build a new thread to record conversation whose score is more than 0.95 in interval time
                   # TODO: by this way we can get a lot of good conversations

    def random_chose_index(self, score_ls, max_score):
        max_score_indexes = []
        for i in range(len(score_ls)):
            if score_ls[i] == max_score:
                max_score_indexes.append(i)
        return choice(max_score_indexes)

    def get_answer(self, utterance, file_name=None):
        try:
            utterance = utterance.rstrip(self.punctuation_str)
            if not file_name:
                file_name = self.select_domain(utterance)

            self.retrieval.read_indexes(file_name)
            context_ls = self.retrieval.search_sentences(utterance)
            if not context_ls and file_name != "domains":
                return "对不起亲，没听懂你说啥，你再重新组织一下语言吧。"
            if not context_ls and file_name == "domains":
                answer = self.get_answer(utterance, "weibo")
                return answer

            if file_name == "domains":
                fuzzy_ratio_ls = fuzzy_for_domains(utterance, context_ls)
            else:
                fuzzy_ratio_ls = fuzzy_matching(utterance, context_ls)

            self.tf_idf.select_model(file_name)
            self.tf_idf.predict_tfidf(utterance, context_ls)
            tf_idf_score_ls = self.tf_idf.calculate_distances()

            if fuzzy_ratio_ls.count(max(fuzzy_ratio_ls)) > 1:
                fuzzy_best_index = self.random_chose_index(fuzzy_ratio_ls, max(fuzzy_ratio_ls))
            else:
                fuzzy_best_index = fuzzy_ratio_ls.index(max(fuzzy_ratio_ls))

            if tf_idf_score_ls.count(max(tf_idf_score_ls)) > 1:
                tftdf_best_index = self.random_chose_index(tf_idf_score_ls, max(tf_idf_score_ls))
            else:
                tftdf_best_index = tf_idf_score_ls.index(max(tf_idf_score_ls))

            fuzzy_best_content = context_ls[fuzzy_best_index][0].rstrip(self.punctuation_str)
            tfidf_best_content = context_ls[tftdf_best_index][0].rstrip(self.punctuation_str)
            if fuzzy_best_content == utterance or utterance in fuzzy_best_content:
                best_index = fuzzy_best_index
                return context_ls[best_index][1]

            if tfidf_best_content == utterance or utterance in tfidf_best_content:
                best_index = tftdf_best_index
                return context_ls[best_index][1]

            final_score_ls = [(fuzzy_ratio * self.fuzzy_weight + tf_tdf_score * self.tf_idf_weight) for fuzzy_ratio, tf_tdf_score in
                              zip(fuzzy_ratio_ls, tf_idf_score_ls)]
            # TODO: find a suitable weight
            if max(final_score_ls) < 0.85 and file_name != "weibo" and file_name != "domains": # TODO: ugly code
                answer = self.get_answer(utterance, "weibo")
                return answer
            else:
                max_score = max(final_score_ls)
                if final_score_ls.count(max_score) > 1:
                    best_index = self.random_chose_index(final_score_ls, max_score)
                else:
                    best_index = final_score_ls.index(max_score)
                return context_ls[best_index][1]
        except Exception as e:
            return "对不起亲，这个问题实在不晓得呀！"

    def get_answer2(self, utterance, file_name=None):
        try:
            utterance = utterance.rstrip(self.punctuation_str)
            file_name = self.get_utterance_type(utterance)

            self.retrieval.read_indexes(file_name)
            context_ls = self.retrieval.search_sentences(utterance)
            if not context_ls:
                return "", 0

            fuzzy_ratio_ls = fuzzy_matching(utterance, context_ls)

            self.tf_idf.select_model(file_name)
            self.tf_idf.predict_tfidf(utterance, context_ls)
            tf_idf_score_ls = self.tf_idf.calculate_distances()

            if fuzzy_ratio_ls.count(max(fuzzy_ratio_ls)) > 1:
                fuzzy_best_index = self.random_chose_index(fuzzy_ratio_ls, max(fuzzy_ratio_ls))
            else:
                fuzzy_best_index = fuzzy_ratio_ls.index(max(fuzzy_ratio_ls))

            if tf_idf_score_ls.count(max(tf_idf_score_ls)) > 1:
                tftdf_best_index = self.random_chose_index(tf_idf_score_ls, max(tf_idf_score_ls))
            else:
                tftdf_best_index = tf_idf_score_ls.index(max(tf_idf_score_ls))

            fuzzy_best_content = context_ls[fuzzy_best_index][0].rstrip(self.punctuation_str)
            tfidf_best_content = context_ls[tftdf_best_index][0].rstrip(self.punctuation_str)
            if fuzzy_best_content == utterance or utterance in fuzzy_best_content:
                best_index = fuzzy_best_index
                return context_ls[best_index][1], max(fuzzy_ratio_ls)

            if tfidf_best_content == utterance or utterance in tfidf_best_content:
                best_index = tftdf_best_index
                return context_ls[best_index][1], max(tf_idf_score_ls)

            final_score_ls = [(fuzzy_ratio * self.fuzzy_weight + tf_tdf_score * self.tf_idf_weight) for fuzzy_ratio, tf_tdf_score in
                              zip(fuzzy_ratio_ls, tf_idf_score_ls)]
            # TODO: find a suitable weight

            max_score = max(final_score_ls)
            if final_score_ls.count(max_score) > 1:
                best_index = self.random_chose_index(final_score_ls, max_score)
            else:
                best_index = final_score_ls.index(max_score)
            return context_ls[best_index][1], max_score
        except Exception as e:
            return "", 0

    def test(self, utterance):
        answer = self.get_answer2(utterance)
        return answer

    def start(self):
        while True:
            utterance = input(">>>")
            if utterance.strip() == "exit1":
                break
            answer = self.get_answer2(utterance)
            print("<<<{}".format(answer))

    def api(self, utterance):
        answer, score = self.get_answer2(utterance)
        return [answer, score]


# if __name__ == '__main__':
#     agent = Agent()
#     agent.start()
