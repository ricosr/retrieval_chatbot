# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import pickle
import yaml

from retrieval_documents import BuildIndex
from tf_idf import TrainTfIdf
import config


# pickle file of conversations must exist, config.file_dict and config.index_dict must be right
def add_index(args):
    build_index = BuildIndex(config)
    build_index.load_pickle()
    build_index.build_index()

def train_tf_idf(args):
    tf_idf = TrainTfIdf(config)
    tf_idf.load_pickle()
    tf_idf.train()

def yml_to_pickle(args):
    with open("{}".format(args.s), 'r', encoding='utf-8') as fp:
        data = yaml.load(fp)
    with open("{0}/{1}.pkl".format(args.d[0], data["categories"][0]), 'wb') as fpw:
        pickle.dump(data["conversations"], fpw)

