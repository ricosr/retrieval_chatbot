# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) by 2018 Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import argparse

import util


parser = argparse.ArgumentParser(
    description='convert file to pickle file, add index of pickle file, create TF-IDF models')
sub_parsers = parser.add_subparsers()

parser_yaml = sub_parsers.add_parser('ymltopkl', help='convert yml file to pickle file')
parser_yaml.add_argument('-s', metavar='source file', type=str, help='mandatory! the yaml or yml file you want to convert')
parser_yaml.add_argument('-d', metavar='destination folder', type=str, default=["data"], nargs='+',
                         help='default: data, if assign other folders, change config.py')
parser_yaml.set_defaults(func=util.yml_to_pickle)




args = parser.parse_args()
args.func(args)