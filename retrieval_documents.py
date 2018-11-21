# -*- coding: utf-8 -*-

# chinese computing project
# members: Mo Feiyu, Sun Rui, Wang Zizhe, copyright

from whoosh.qparser import QueryParser
from whoosh.index import create_in,open_dir
from jieba.analyse.analyzer import ChineseAnalyzer
import jieba


# class Retrieval:
#     def __init__(self, num_ir=10, documents_dict=None):
#         self.num_ir = num_ir
#         self.documents_dict = documents_dict
#         self.files_dict = {}
#         self.load_index()

    # def load_documents(self):
    #     for file_name, path in self.documents_dict.items():
    #         with open(path, 'r') as f:
    #             self.files_dict[file_name] = f.readlines()
    #
    # def add_indexes(self):
    #     pass

class Retrieval:
    def __init__(self, num_ir=10, config=None):
        self.num_ir = num_ir
        # self.documents_dict = documents_dict
        self.files_dict = {}
        self.load_index()

    def load_index(self, index_path):
        pass

    def read_indexes(self):
        ix = open_dir("tmp")



    def search_sentences(self, utterance, file_name):
        context_ls = []
        return context_ls
