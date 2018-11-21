# -*- coding: utf-8 -*-

# chinese computing project
# members: Mo Feiyu, Sun Rui, Wang Zizhe, copyright

import pickle
from retrieval_documents import Retrieval
from calculate_distances import TfIdf

# TODO: distribute message by threading or tornado

NUM_OF_IR = 10
DOCUMENTS_PATH = {}
MODEL_PATH = []

class Agent:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = ''
        self.load_config()
        self.init_all_states()

    def load_config(self):
        with open(self.config_path, 'rb') as f:
            self.config = pickle.load(f)

    def init_all_states(self):
        self.retrieval = Retrieval(num_ir=10)
        self.tf_idf = TfIdf(MODEL_PATH)

    def get_utterance_type(self, utterance):    # TODO
        return "test"    # return file_name

    def start(self):
        while True:
            utterance = input(">>>")
            file_name = self.get_utterance_type(utterance)
            index_path = self.config[file_name]
            self.retrieval.load_index(index_path)
            context_ls = self.retrieval.search_sentences(utterance, file_name)
            self.tf_idf.calculate_tfidf(utterance, context_ls)
            best_index = self.tf_idf.calculate_distances()
            print("<<<{}".format(context_ls[best_index]))

if __name__ == '__main__':
    agent = Agent('config_path')
