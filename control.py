# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

from retrieval_documents import Retrieval
from calculate_distances import TfIdf
from config import index_dict

# TODO: distribute message by threading or tornado

NUM_OF_IR = 10
DOCUMENTS_PATH = {}
MODEL_PATH = []

class Agent:
    def __init__(self):
        self.config = index_dict
        self.init_all_states()

    def init_all_states(self):
        self.retrieval = Retrieval(num_ir=10, config=self.config)
        self.tf_idf = TfIdf(MODEL_PATH)

    def get_utterance_type(self, utterance):    # TODO get correct file name by utterance
        return "tmp"    # return file_name

    def start(self):
        while True:
            utterance = input(">>>")
            file_name = self.get_utterance_type(utterance)
            # index_path = self.config[file_name]
            self.retrieval.read_indexes(file_name)
            context_ls = self.retrieval.search_sentences(utterance)
            self.tf_idf.calculate_tfidf(utterance, context_ls)
            best_index = self.tf_idf.calculate_distances()
            print("<<<{}".format(context_ls[best_index]))

if __name__ == '__main__':
    agent = Agent()
