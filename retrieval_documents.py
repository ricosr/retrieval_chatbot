# -*- coding: utf-8 -*-

# chinese computing project
# members: Mo Feiyu, Sun Rui, Wang Zizhe, copyright

import os.path

from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir
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
        self.config = config
        # self.files_dict = {}
        self.current_index = None
        self.index_dict = {}
        self.load_index()

    def load_index(self):
        for file_name, file_path in self.config.index_dict:
            self.index_dict[file_name] = open_dir(file_path)

    def read_indexes(self, file_name):
        self.current_index = self.index_dict[file_name]

    def search_sentences(self, utterance):
        result_ls = []
        seg_list = [each_word for each_word in jieba.cut(utterance, cut_all=True)]
        with self.current_index.searcher() as searcher:
            for each_seg in seg_list:
                query = QueryParser("content", self.current_index.schema).parse(each_seg)
                result_ls.append(searcher.search(query, limit=self.num_ir))
        return list(set(result_ls))

class BuildIndex:
    def __init__(self, config):
        self.config = config
        self.files_dict = {}

    def load_documents(self):
        for file_name, path in self.config.file_dict.items():
            with open(path, 'r') as f:
                self.files_dict[file_name] = f.readlines()

    def build_index(self):
        analyzer = ChineseAnalyzer()
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
        for file, content in self.files_dict.items():
            # TODO !!!!!
            ix = create_in("tmp", schema) # for create new index