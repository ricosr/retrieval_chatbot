# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import pickle
import os

from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir
from jieba.analyse.analyzer import ChineseAnalyzer
import jieba


class Retrieval:
    def __init__(self, num_ir=10, config=None):
        self.num_ir = num_ir
        self.config = config
        self.current_index = None
        self.index_dict = {}
        self.load_index()

    def load_index(self):
        for file_name, file_path in self.config.index_dict.items():
            self.index_dict[file_name] = open_dir(file_path)

    def read_indexes(self, file_name):
        self.current_index = self.index_dict[file_name]

    def search_sentences(self, utterance):
        result_ls = []
        seg_list = [each_word for each_word in jieba.cut(utterance, cut_all=True)]
        with self.current_index.searcher() as searcher:
            for each_seg in seg_list:
                query = QueryParser("content", self.current_index.schema).parse(each_seg)
                results = searcher.search(query, limit=self.num_ir)
                for hit in results:
                    result_ls.append([hit["content"], hit["title"]])
        tmp_result_ls = [(each_content[0], each_content[1]) for each_content in result_ls]
        return list(set(tmp_result_ls))    # TODO: need to improve

    # def read_pickle

class BuildIndex:
    def __init__(self, config):
        self.config = config
        self.files_dict = {}

    def load_pickle(self):
        for file_name, path in self.config.file_dict.items():
            with open(path, 'rb') as fp:
                self.files_dict[file_name] = pickle.load(fp)

    def build_index(self):
        index_config = self.config.index_dict
        analyzer = ChineseAnalyzer()
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
        # try:
        for file_name, content in self.files_dict.items():    # content:[[question], [answer]]
            index_path = index_config[file_name]
            if not os.path.exists(index_path):
                os.mkdir(index_path)
            tmp_index = create_in(index_path, schema)
            writer = tmp_index.writer()
            for i in range(len(content)):
                writer.add_document(
                    title=content[i][1].strip(),
                    path="/{}".format(str(i)),
                    content=content[i][0].strip()
                )
            writer.commit()
        # except Exception as e:
        #     print(e)
