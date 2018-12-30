# -*- coding: utf-8 -*-

# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import pickle
import os
import copy
from functools import reduce

from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir
from jieba.analyse.analyzer import ChineseAnalyzer
import jieba
import jieba.posseg as pseg


class Retrieval:
    def __init__(self, num_ir, config=None):
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

    def cut_words(self, sentence):
        words_result = []
        words = pseg.cut(sentence)
        for (word, flag) in words:
            if flag == 't' or flag == 'b' or flag == 'ul':
                continue
            else:
                words_result.append(word)
        return words_result

    def remove_stop_words(self, stop_words_ls, cut_words_ls):
        if len(cut_words_ls) > 6:
            # tmp_ls = copy.deepcopy(origin_ls)
            for i in range(len(cut_words_ls)):
                if cut_words_ls[i] in stop_words_ls:
                    cut_words_ls[i] = 0
                    # tmp_ls.pop(i)
            while True:
                if 0 in cut_words_ls:
                    cut_words_ls.remove(0)
                else:
                    break
            return cut_words_ls, True
        if cut_words_ls[-1] in self.config.special_modal_words:
            cut_words_ls.pop(-1)
        return cut_words_ls, False

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

    def filter_results_by_seg(self, result_utter, utter_seg):
        count = 0
        for each_seg in utter_seg:
            if len(each_seg) == 1:
                continue
            if each_seg in result_utter:
                count += 1
        if count < 2:
            return False, count
        return True, count

    def find_max_min_length(self, words_ls):
        max_length = 0
        max_count = 0
        min_length = 100
        min_count = 0
        for each_word in words_ls:
            if len(each_word) == max_length:
                max_count += 1
            if len(each_word) == min_length:
                min_count += 1
            if len(each_word) > max_length:
                max_length = len(each_word)
                max_count = 1
            if len(each_word) < min_length:
                min_length = len(each_word)
                min_count = 1
        return (max_length, max_count), (min_length, min_count)

    def search_sentences(self, utterance, stop_words):
        utterance_ls = self.cut_by_punctuation(utterance)
        result_ls = []
        cache_resutl_ls = []
        seg_list = []
        for each_part in utterance_ls:
            tmp_words_ls = self.cut_words(each_part)
            # # print("tmp_words_ls: {}".format(tmp_words_ls))
            # seg_list.append(self.remove_stop_words(stop_words, tmp_words_ls))
            seg_list.extend(tmp_words_ls)
        # segments = list(reduce((lambda ls1, ls2: ls1+ls2), seg_list))
        print("seg_list1:{}".format(seg_list))
        new_seg_list, stop_key = self.remove_stop_words(stop_words, seg_list)
        print("new_seg_list:{}".format(new_seg_list))
        # if len(seg_list) == 1 and len(seg_list[0]) < 5:
        #     for each_seg_ls in seg_list:
        #         self.tmp_seg_ls = []
        #         self.create_query_segments(each_seg_ls)
        #         new_seg_ls.append(self.tmp_seg_ls)
        # else:
        #     for each_seg_ls in seg_list:
        #         self.tmp_seg_ls = []
        #         self.create_query_segments(each_seg_ls)
        #         # if len(self.tmp_seg_ls) > 1:
        #         #     list(map(self.tmp_seg_ls.remove, each_seg_ls))
        #         # if len(self.tmp_seg_ls) > 2:
        #         #     self.tmp_seg_ls.remove(sorted(self.tmp_seg_ls, key=lambda k: len(k), reverse=True)[0])
        #         new_seg_ls.append(self.tmp_seg_ls)
        # for each_seg_ls in new_seg_list:
        #     self.tmp_seg_ls = []
        #     self.create_query_segments(each_seg_ls)
        #     new_seg_ls.append(self.tmp_seg_ls)
        self.tmp_seg_ls = []
        self.create_query_segments(new_seg_list)
        # utter_seg = sorted(new_seg_list, key=lambda k: len(k), reverse=True)
        print(stop_key)
        if not stop_key and len(self.tmp_seg_ls) > 1:
            list(map(self.tmp_seg_ls.remove, new_seg_list))
        new_seg_ls = self.tmp_seg_ls
        print("new_seg_ls: {}".format(new_seg_ls))
        utter_seg = sorted(new_seg_ls, key=lambda k: len(k), reverse=True)
        search_length = len(utter_seg)
        print("utter_seg:{}".format(utter_seg))
        with self.current_index.searcher() as searcher:
            # result_count = 0
            for each_seg in utter_seg:
                query = QueryParser("content", self.current_index.schema).parse(each_seg)
                results = searcher.search(query, limit=self.num_ir)
                # print("result length:{}".format(len(results)))
                # result_count += len(results)
                filter_key = False
                for hit in results:
                    cache_resutl_ls.append([hit["content"], hit["title"]])
                    # filter_key = True
                    filter_key, count = self.filter_results_by_seg(hit["content"]+hit["title"], set(new_seg_list))
                    if filter_key is True:
                        result_ls.append([hit["content"], hit["title"]])
                # if not stop_key:
                if len(cache_resutl_ls) >= search_length*self.num_ir/2:
                    print("result_count:{}".format(len(cache_resutl_ls)))
                    break

        if not result_ls:
            print("no result....")
            result_ls = cache_resutl_ls
        tmp_result_ls = [(each_content[0], each_content[1]) for each_content in result_ls]
        print("result ls:{}".format(set(tmp_result_ls)))
        return list(set(tmp_result_ls))


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
