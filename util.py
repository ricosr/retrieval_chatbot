# -*- coding: utf-8 -*-


import os
import pickle
import yaml
import json

import jieba.posseg as pseg
import nltk
import numpy as np

from retrieval_documents import BuildIndex
from tf_idf import TrainTfIdf
from config import config


# pickle origin_corpus of conversations must exist, config.file_dict and config.index_dict must be right
def add_index(args):
    build_index = BuildIndex(config)
    build_index.load_pickle(args.f)
    build_index.build_index()


def add_domain_index(args):
    build_index = BuildIndex(config)
    build_index.load_pickle(args.f)
    build_index.build_domains_index()


def train_tf_idf(args):
    tf_idf = TrainTfIdf(config)
    tf_idf.load_pickle(args.f)
    tf_idf.train()


def yml_to_pickle(args):
    if not args.s:
        file_ls = os.listdir("origin_corpus/yml")
        for each_file in file_ls:
            with open("origin_corpus/yml/{}".format(each_file), 'r', encoding='utf-8') as fp:
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
        source_file = args.s if key else "origin_corpus/conv/{}.conv".format(file_name)
        with open("{}".format(source_file), 'r', encoding='utf-8') as fp:
            file_lines = fp.readlines()
        chat_ls = []
        tmp_ls = []
        for i in range(len(file_lines)):
            if file_lines[i].strip() == "E":
                continue
            if file_lines[i].split(' ')[0] == 'M':
                if file_lines[i].lstrip('M').strip():
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
        file_ls = os.listdir("origin_corpus/conv")
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


def divide_bar_to_pickle(args):
    bar_file = args.s
    file_name = bar_file.split('/')[-1].split('.')[0]
    chat_ls = []
    with open(bar_file, 'r', encoding='utf-8') as fpr:
        data_line = fpr.readline()
        while data_line:
            # print(data_line.split('|')[0].strip())
            if data_line.split('|')[0].strip():
                # print(data_line)
                chat_ls.append([data_line.split('|')[0].strip(), data_line.split('|')[1].strip()])
            data_line = fpr.readline()
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
    with open("frequency_domain.py", "w", encoding="utf-8") as fwp:
        fwp.write("frequency_dict = {}".format(str(frequency_dict)))


def combine_pickle(args):
    dir_path = args.p
    final_ls = []
    dir_ls = os.listdir(dir_path)
    for each_file in dir_ls:
        with open("{}/{}".format(dir_path, each_file), 'rb') as fp:
            final_ls += pickle.load(fp)
    print("the count of all data is {}".format(str(len(final_ls))))
    with open("data/{}".format(args.o), 'wb') as fpw:
        pickle.dump(final_ls, fpw)


def combine_array(args):
    dir_path = args.p
    dir_ls = os.listdir(dir_path)
    tmp_array = None
    for each_file in dir_ls:
        with open("{}/{}".format(dir_path, each_file), 'rb') as fpr:
            if type(tmp_array) is not np.ndarray:
                tmp_array = pickle.load(fpr)
            else:
                tmp_array = np.concatenate((tmp_array, pickle.load(fpr)), axis=0)
    print("the count of all data is {}".format(str(len(tmp_array))))
    with open("sentence_cluster/vec_data/{}".format(args.o), 'wb') as fpw:
        pickle.dump(tmp_array, fpw)


def create_stop_words_ls():
    with open("stopwords/baidu.txt", 'r', encoding='utf-8') as fpb:
        baidu_stop = fpb.readlines()

    with open("stopwords/HIT.txt", 'r', encoding='utf-8') as fpH:
        HIT_stop = fpH.readlines()

    with open("stopwords/SCU.txt", 'r', encoding='utf-8') as fpS:
        SCU_stop = fpS.readlines()

    with open("stopwords/ZH.txt", 'r', encoding='utf-8')as fpZ:
        ZH_stop = fpZ.readlines()

    all_stop = HIT_stop
    new_stop = map(lambda a: a.strip(), all_stop)
    with open("stopwords/all_stop.pkl", 'wb') as fpw:
        pickle.dump(list(set(new_stop)), fpw)

# create_stop_words_ls()
