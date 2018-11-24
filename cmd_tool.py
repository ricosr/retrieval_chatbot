# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) by 2018 Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import argparse

import util


parser = argparse.ArgumentParser(
    description='convert file to pickle file, add index of pickle file, create TF-IDF models')
sub_parsers = parser.add_subparsers()

parser_yaml = sub_parsers.add_parser('ymltopkl', help='convert yml file to pickle file')
parser_yaml.add_argument('-s', metavar='source file', type=str,
                         help='default: None, if not assign the yaml or yml file you want to convert, then convert all in directory file/yml')
parser_yaml.add_argument('-d', metavar='destination folder', type=str, default=["data"], nargs='+',
                         help='default: data, if assign other folders, change config.py')
parser_yaml.set_defaults(func=util.yml_to_pickle)


parser_conv = sub_parsers.add_parser('convtopkl', help='convert conv file to pickle file')
parser_conv.add_argument('-s', metavar='source file', type=str,
                         help='default: None, if not assign the conv file you want to convert, then convert all in directory file/conv')
parser_conv.add_argument('-d', metavar='destination folder', type=str, default=["data"], nargs='+',
                         help='default: data, if assign other folders, change config.py')
parser_conv.set_defaults(func=util.conv_to_pickle)


parser_json = sub_parsers.add_parser('jsontopkl', help='convert json file to pickle file')
parser_json.add_argument('-s', metavar='source file', type=str, help='mandatory! the conv file you want to convert')
parser_json.add_argument('-d', metavar='destination folder', type=str, default=["data"], nargs='+',
                         help='default: data, if assign other folders, change config.py')
parser_json.set_defaults(func=util.json_to_pickle)


parser_index = sub_parsers.add_parser('index', help='add indexes')
parser_index.add_argument('-f', metavar='file name', type=str, default=[], nargs='+',
                         help='default: None, if no assign the value, build indexes for all data files')
parser_index.set_defaults(func=util.add_index)


parser_tfidf = sub_parsers.add_parser('tfidf', help='train TF-IDF model')
parser_tfidf.add_argument('-f', metavar='file name', type=str, default=[], nargs='+',
                         help='default: None, if no assign the value, train TF-IDF for all data files')
parser_tfidf.set_defaults(func=util.train_tf_idf)


args = parser.parse_args()
args.func(args)
