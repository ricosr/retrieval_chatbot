# -*- coding: utf-8 -*-

# COMP5412: Chinese computing project
# Copyright (c) by 2018 Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

from random import choice

from retrieval_documents import Retrieval
from fuzzy_match import fuzzy_matching
from tf_idf import TfIdf
import config

# TODO: distribute message by threading or tornado

NUM_OF_IR = 2

class Agent:
    def __init__(self):
        self.config = config
        self.punctuation_str = ''.join(config.punctuation_ls)
        self.init_all_states()

    def init_all_states(self):
        self.retrieval = Retrieval(num_ir=NUM_OF_IR, config=self.config)
        self.tf_idf = TfIdf(config)

    # def select_domain(self):
    #
    # def get_utterance_type(self, utterance):    # TODO get correct file name by utterance
    #     return "weibo"    # return file_name  0.9

    def random_chose_index(self, score_ls, max_score):
        max_score_indexes = []
        for i in range(len(score_ls)):
            if score_ls[i] == max_score:
                max_score_indexes.append(i)
        return choice(max_score_indexes)

    def get_answer(self, utterance, file_name):
        try:
            utterance = utterance.rstrip(self.punctuation_str)

            # file_name = self.get_utterance_type(utterance)
            self.retrieval.read_indexes(file_name)
            context_ls = self.retrieval.search_sentences(utterance)
            if not context_ls:
                return "对不起亲，没听懂你说啥，你再重新组织一下语言吧。"
            fuzzy_ratio_ls = fuzzy_matching(utterance, context_ls)

            self.tf_idf.select_model(file_name)
            self.tf_idf.predict_tfidf(utterance, context_ls)
            tf_idf_score_ls = self.tf_idf.calculate_distances()

            if fuzzy_ratio_ls.count(max(fuzzy_ratio_ls)) > 1:
                fuzzy_best_index = self.random_chose_index(fuzzy_ratio_ls, max(fuzzy_ratio_ls))
            else:
                fuzzy_best_index = fuzzy_ratio_ls.index(max(fuzzy_ratio_ls))

            if tf_idf_score_ls.count(max(tf_idf_score_ls)) > 1:
                tftdf_best_index = tf_idf_score_ls.index(max(tf_idf_score_ls))
            else:
                tftdf_best_index = tf_idf_score_ls.index(max(tf_idf_score_ls))

            fuzzy_best_content = context_ls[fuzzy_best_index][0].rstrip(self.punctuation_str)
            tfidf_best_content = context_ls[tftdf_best_index][0].rstrip(self.punctuation_str)
            if fuzzy_best_content == utterance or utterance in fuzzy_best_content:
                best_index = fuzzy_best_index
                print(context_ls[best_index][0])
                return context_ls[best_index][1]

            if tfidf_best_content == utterance or utterance in tfidf_best_content:
                best_index = tftdf_best_index
                print(context_ls[best_index][0])
                return context_ls[best_index][1]

            final_score_ls = [(fuzzy_ratio * 0.7 + tf_tdf_score * 0.3) for fuzzy_ratio, tf_tdf_score in
                              zip(fuzzy_ratio_ls, tf_idf_score_ls)]
            # TODO: find a suitable weight
            print(final_score_ls)
            if max(final_score_ls) < 0.9 and file_name != "weibo":
                print(max(final_score_ls))
                answer = self.get_answer(utterance, "weibo")
                return answer
            else:
                print(max(final_score_ls))
                max_score = max(final_score_ls)
                if final_score_ls.count(max_score) > 1:
                    best_index = self.random_chose_index(final_score_ls, max_score)
                else:
                    best_index = final_score_ls.index(max_score)
                print(context_ls[best_index][0])
                return context_ls[best_index][1]

            # print(context_ls[best_index][0])
            # print(max(final_score_ls))# 0.8 ->微博
            # print(final_score_ls)

            # print(context_ls[fuzzy_ratio_ls.index(max(fuzzy_ratio_ls))], fuzzy_ratio_ls.index(max(fuzzy_ratio_ls)))
            # print(context_ls[tf_idf_score_ls.index(max(tf_idf_score_ls))], tf_idf_score_ls.index(max(tf_idf_score_ls)))
            # print(best_index)
        except Exception as e:
            pass

    def start(self):
        while True:
            utterance = input(">>>")
            if utterance.strip() == "exit1":
                break
            answer = self.get_answer(utterance, "xiaohuangji")
            print("<<<{}".format(answer))


if __name__ == '__main__':
    agent = Agent()
    agent.start()
