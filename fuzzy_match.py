# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def fuzzy_matching(utterance, context_ls):
    mean_ratio_ls = []
    for i in range(len(context_ls)):
        ratio_sum = 0
        ratio_sum += fuzz.ratio(utterance, context_ls[i][0])
        ratio_sum += fuzz.partial_ratio(utterance, context_ls[i][0])
        ratio_sum += fuzz.token_sort_ratio(utterance, context_ls[i][0])
        ratio_sum += fuzz.token_set_ratio(utterance, context_ls[i][0])
        mean_ratio = ratio_sum / 4
        mean_ratio_ls.append(mean_ratio)
    return sorted(mean_ratio_ls, reverse=True)[0]

