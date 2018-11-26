# -*- coding: utf-8 -*-

# COMP5412: Chinese computing project
# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import os
import pickle
import yaml
import json

import jieba.posseg as pseg
import nltk

from retrieval_documents import BuildIndex
from tf_idf import TrainTfIdf
from config import config


# pickle file of conversations must exist, config.file_dict and config.index_dict must be right
def add_index(args):
    build_index = BuildIndex(config)
    build_index.load_pickle(args.f[0])
    build_index.build_index()

def add_domain_index(args):
    build_index = BuildIndex(config)
    build_index.load_pickle(args.f[0])
    build_index.build_domains_index()

def train_tf_idf(args):
    tf_idf = TrainTfIdf(config)
    tf_idf.load_pickle(args.f[0])
    tf_idf.train()

def yml_to_pickle(args):
    if not args.s:
        file_ls = os.listdir("file/yml")
        for each_file in file_ls:
            with open("file/yml/{}".format(each_file), 'r', encoding='utf-8') as fp:
                data = yaml.load(fp)
            if not os.path.exists(args.d[0]):
                os.mkdir(args.d[0])
            with open("{0}/{1}.pkl".format(args.d[0], data["categories"][0]), 'wb') as fpw:
                pickle.dump(data["conversations"], fpw)
    else:
        with open("{}".format(args.s), 'r', encoding='utf-8') as fp:
            data = yaml.load(fp)
        if not os.path.exists(args.d[0]):
            os.mkdir(args.d[0])
        with open("{0}/{1}.pkl".format(args.d[0], data["categories"][0]), 'wb') as fpw:
            pickle.dump(data["conversations"], fpw)

def conv_to_pickle(args):
    def write_pickle(args, file_name, key):
        source_file = args.s if key else "file/conv/{}.conv".format(file_name)
        with open("{}".format(source_file), 'r', encoding='utf-8') as fp:
            file_lines = fp.readlines()
        chat_ls = []
        tmp_ls = []
        for i in range(len(file_lines)):
            if file_lines[i].strip() == "E":
                continue
            if file_lines[i].split(' ')[0] == 'M':
                tmp_ls.append(file_lines[i].lstrip('M').strip())
                if i <= len(file_lines)-1:
                    if i+1 == len(file_lines):
                        chat_ls.append(tmp_ls)
                        break
                    if file_lines[i+1].strip() == "E":
                        chat_ls.append(tmp_ls)
                        tmp_ls = []
        if not os.path.exists(args.d[0]):
            os.mkdir(args.d[0])
        with open("{0}/{1}.pkl".format(args.d[0], file_name), 'wb') as fpw:
            pickle.dump(chat_ls, fpw)
    if not args.s:
        file_ls = os.listdir("file/conv")
        for each_file in file_ls:
            write_pickle(args, each_file.split('.')[0], False)
    else:
        file_name = args.s.split('/')[-1].split('.')[0]
        write_pickle(args, file_name, True)

def json_to_pickle(args):   # only be used in this special format corpus of this project
    json_file = args.s
    file_name = json_file.split('/')[-1].split('.')[0]
    with open(json_file, 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)
    chat_ls = []
    for each_chat in json_data:
        utterance = each_chat[0][0]
        utterance = ''.join(utterance.split(' ')).strip()
        content = each_chat[1][0]
        content = ''.join(content.split(' ')).strip()
        chat_ls.append([utterance, content])
    if not os.path.exists(args.d[0]):
        os.mkdir(args.d[0])
    with open("{0}/{1}.pkl".format(args.d[0], file_name), 'wb') as fpw:
        pickle.dump(chat_ls, fpw)

def count_none_frequency(file_name):   # just save none
    frequency_dict = {}
    with open(file_name, "rb") as fp:
        chat_ls = pickle.load(fp)
    for each_pair in chat_ls:
        for each_sentence in each_pair:
            words_ls = []
            cut_words = dict(pseg.cut(each_sentence))
            for word, flag in cut_words.items():
                if 'n' in flag:
                    words_ls.append(word)
            freq_dict_tmp = nltk.FreqDist(words_ls)
            for word, freq in freq_dict_tmp.items():
                if word in frequency_dict:
                    frequency_dict[word] = frequency_dict[word] + freq
                else:
                    frequency_dict[word] = freq
    with open("config/frequency_domain.py", "w", encoding="utf-8") as fwp:
        fwp.write("frequency_dict = {}".format(str(frequency_dict)))


def combine_pickle(dir_path):
    final_ls = []
    dir_ls = os.listdir(dir_path)
    for each_file in dir_ls:
        with open("{}/{}".format(dir_path, each_file), 'rb') as fp:
            final_ls += pickle.load(fp)
    with open("data/domains.pkl", 'wb') as fpw:
        pickle.dump(final_ls, fpw)

count_none_frequency("data/domains.pkl")











