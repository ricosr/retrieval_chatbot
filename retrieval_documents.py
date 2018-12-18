# -*- coding: utf-8 -*-

# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import pickle
import os
import copy

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
        jieba.initialize()

    def load_index(self):
        try:
            for file_name, file_path in self.config.index_dict.items():
                self.index_dict[file_name] = open_dir(file_path)
        except Exception as e:
            pass

    def read_indexes(self, file_name):
        try:
            self.current_index = self.index_dict[file_name]
        except Exception as e:
            pass

    def remove_high_freq_words(self, words_ls, origin_ls):
        if words_ls:
            tmp_ls = copy.deepcopy(origin_ls)
            for i in range(len(origin_ls)):
                if origin_ls[i] in words_ls:
                    tmp_ls.pop(i)
            return tmp_ls
        return origin_ls

    def search_sentences(self, utterance):
        utterance_ls = self.cut_by_punctuation(utterance)
        result_ls = []
        seg_list = []
        new_seg_ls = []
        for each_part in utterance_ls:
            tmp_words_ls = [each_word for each_word in jieba.cut(each_part, cut_all=False)]
            seg_list.append(self.remove_high_freq_words(self.config.remove_words, tmp_words_ls))
        if len(seg_list) == 1 and len(seg_list[0]) < 5:
            for each_seg_ls in seg_list:
                self.tmp_seg_ls = []
                self.create_query_segments(each_seg_ls)
                new_seg_ls.append(self.tmp_seg_ls)
        else:
            for each_seg_ls in seg_list:
                self.tmp_seg_ls = []
                self.create_query_segments(each_seg_ls)
                if len(self.tmp_seg_ls) > 1:
                    list(map(self.tmp_seg_ls.remove, each_seg_ls))
                if len(self.tmp_seg_ls) > 2:
                    self.tmp_seg_ls.remove(sorted(self.tmp_seg_ls, key=lambda k: len(k), reverse=True)[0])
                new_seg_ls.append(self.tmp_seg_ls)
        for each_new_seg in new_seg_ls:
            with self.current_index.searcher() as searcher:
                for each_seg in each_new_seg:
                    query = QueryParser("content", self.current_index.schema).parse(each_seg)
                    results = searcher.search(query, limit=self.num_ir)
                    for hit in results:
                        result_ls.append([hit["content"], hit["title"]])
        tmp_result_ls = [(each_content[0], each_content[1]) for each_content in result_ls]
        return list(set(tmp_result_ls))    # TODO: need to improve

    def cut_by_punctuation(self, sentence):
        sentence_ls = list(sentence)
        for i in range(len(sentence_ls)):
            if sentence_ls[i] in self.config.punctuation_ls:
                sentence_ls[i] = '\t'
        return ''.join(sentence_ls).strip().split('\t')

    def create_query_segments(self, seg_list):
        temp_seg = ''
        for each in seg_list:
            temp_seg += each
            self.tmp_seg_ls.append(temp_seg)
        if len(seg_list) == 0:
            return
        self.create_query_segments(seg_list[1:])


class BuildIndex:
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

    def build_index(self):
        index_config = self.config.index_dict
        analyzer = ChineseAnalyzer()
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
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

    def build_domains_index(self):
        index_config = self.config.index_dict
        analyzer = ChineseAnalyzer()
        schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True, analyzer=analyzer))
        for file_name, content in self.files_dict.items():  # content:[[question], [answer]]
            index_path = index_config[file_name]
            if not os.path.exists(index_path):
                os.mkdir(index_path)
            tmp_index = create_in(index_path, schema)
            writer = tmp_index.writer()
            for i in range(len(content)):
                writer.add_document(
                    title=content[i][1].strip(),
                    path="/{}".format(str(i)),
                    content=content[i][0].strip() + content[i][1].strip()
                )
            writer.commit()
