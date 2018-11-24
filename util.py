# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import pickle
import yaml
import json

from retrieval_documents import BuildIndex
from tf_idf import TrainTfIdf
import config


# pickle file of conversations must exist, config.file_dict and config.index_dict must be right
def add_index(args):
    build_index = BuildIndex(config)
    build_index.load_pickle(args.f[0])
    build_index.build_index()

def train_tf_idf(args):
    tf_idf = TrainTfIdf(config)
    tf_idf.load_pickle(args.f[0])
    tf_idf.train()

def yml_to_pickle(args):
    with open("{}".format(args.s), 'r', encoding='utf-8') as fp:
        data = yaml.load(fp)
    with open("{0}/{1}.pkl".format(args.d[0], data["categories"][0]), 'wb') as fpw:
        pickle.dump(data["conversations"], fpw)

def conv_to_pickle(args):
    file_name = args.s.split('/')[-1].split('.')[0]
    with open("{}".format(args.s), 'r', encoding='utf-8') as fp:
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
    with open("{0}/{1}.pkl".format(args.d[0], file_name), 'wb') as fpw:
        pickle.dump(chat_ls, fpw)

def json_to_pickle(args):
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
    with open("{0}/{1}.pkl".format(args.d[0], file_name), 'wb') as fpw:
        pickle.dump(chat_ls, fpw)









