# -*- coding: utf-8 -*-

# COMP5412: Chinese computing project
# Copyright (c) by 2018 Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

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

    def get_utterance_type(self, utterance):    # TODO get correct file name by utterance
        return "weibo"    # return file_name  0.8

    def start(self):
        while True:
            try:
                utterance = input(">>>")
                utterance = utterance.rstrip(self.punctuation_str)
                if utterance == "exit1":
                    break    # TODO: remove when deploy
                file_name = self.get_utterance_type(utterance)
                self.retrieval.read_indexes(file_name)
                context_ls = self.retrieval.search_sentences(utterance)
                if not context_ls:
                    continue
                fuzzy_ratio_ls = fuzzy_matching(utterance, context_ls)

                self.tf_idf.select_model(file_name)
                self.tf_idf.predict_tfidf(utterance, context_ls)
                tf_idf_score_ls = self.tf_idf.calculate_distances()
                fuzzy_best_index = fuzzy_ratio_ls.index(max(fuzzy_ratio_ls))
                tftdf_best_index = tf_idf_score_ls.index(max(tf_idf_score_ls))
                fuzzy_best_content = context_ls[fuzzy_best_index][0].rstrip(self.punctuation_str)
                tfidf_best_content = context_ls[tftdf_best_index][0].rstrip(self.punctuation_str)
                if fuzzy_best_content == utterance or utterance in fuzzy_best_content:
                    best_index = fuzzy_best_index
                    print("<<<{}".format(context_ls[best_index][1]))
                    print(context_ls[best_index][0])
                    continue
                if tfidf_best_content == utterance or utterance in tfidf_best_content:
                    best_index = tftdf_best_index
                    print("<<<{}".format(context_ls[best_index][1]))
                    print(context_ls[best_index][0])
                    continue

                final_score_ls = [(fuzzy_ratio*0.7 + tf_tdf_score*0.3) for fuzzy_ratio, tf_tdf_score in zip(fuzzy_ratio_ls, tf_idf_score_ls)]
                # TODO: find a suitable weight
                best_index = final_score_ls.index(max(final_score_ls))
                print("<<<{}".format(context_ls[best_index][1]))
                print(context_ls[best_index][0])
                print(max(final_score_ls))# 0.8 ->微博
                print(final_score_ls)


                print(context_ls[fuzzy_ratio_ls.index(max(fuzzy_ratio_ls))], fuzzy_ratio_ls.index(max(fuzzy_ratio_ls)))
                print(context_ls[tf_idf_score_ls.index(max(tf_idf_score_ls))], tf_idf_score_ls.index(max(tf_idf_score_ls)))
                print(best_index)
            except Exception as e:
                pass

if __name__ == '__main__':
    agent = Agent()
    agent.start()
