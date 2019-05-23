# -*- coding: utf-8 -*-


from fuzzywuzzy import fuzz


def normalization(ratio_ls):
    max_ratio = max(ratio_ls)
    min_ratio = min(ratio_ls)
    if max_ratio == min_ratio:
        return [1]*len(ratio_ls)
    return [(each_ratio - min_ratio)/(max_ratio - min_ratio) for each_ratio in ratio_ls]


def fuzzy_matching(utterance, context_ls):
    ratio_ls = []
    for i in range(len(context_ls)):
        if context_ls[i] == (0, 0):
            continue
        ratio_sum = 0
        ratio_sum += fuzz.ratio(utterance+','+context_ls[i][1], context_ls[i][0]+','+context_ls[i][1])
        ratio_sum += fuzz.partial_ratio(utterance+','+context_ls[i][1], context_ls[i][0]+','+context_ls[i][1])
        ratio_sum += fuzz.token_sort_ratio(utterance+','+context_ls[i][1], context_ls[i][0]+','+context_ls[i][1])
        ratio_sum += fuzz.token_set_ratio(utterance+','+context_ls[i][1], context_ls[i][0]+','+context_ls[i][1])
        mean_ratio = ratio_sum / 4
        ratio_ls.append(mean_ratio)
    return normalization(ratio_ls)


def fuzzy_for_domains(utterance, context_ls):
    ratio_ls = []
    for i in range(len(context_ls)):
        ratio_sum = 0
        ratio_sum += fuzz.ratio(utterance, context_ls[i][0]+context_ls[i][1])
        ratio_sum += fuzz.partial_ratio(utterance, context_ls[i][0]+context_ls[i][1])
        ratio_sum += fuzz.token_sort_ratio(utterance, context_ls[i][0]+context_ls[i][1])
        ratio_sum += fuzz.token_set_ratio(utterance, context_ls[i][0]+context_ls[i][1])
        mean_ratio = ratio_sum / 4
        ratio_ls.append(mean_ratio)
    return normalization(ratio_ls)
