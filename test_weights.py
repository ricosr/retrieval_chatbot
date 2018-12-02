# -*- coding: utf-8 -*-

# COMP5412: Chinese computing project
# Copyright (c) by 2018 Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import pickle

import control


test_num = 500
interval_num = 5
step = 100

def create_test_data(pickle_file):
    with open(pickle_file, "rb") as pfw:
        data_lines = pickle.load(pfw)
    data_length = len(data_lines)
    interval = int(data_length/interval_num)
    test_data_ls = data_lines[0:step] + data_lines[interval: interval+step]
    test_data_ls += data_lines[interval*2: interval*2+step] + data_lines[interval*3: interval*3+step]
    test_data_ls += data_lines[interval*4: interval*4+step]
    return test_data_ls

fuzzy_weight = 0.58
tf_idf_weight = 0.42

while True:
    right_times = 0
    fuzzy_weight -= 0.01
    tf_idf_weight += 0.01
    test_data_ls = create_test_data("sentence_cluster/data/all_data.pkl")
    if fuzzy_weight == 0.5:
        break
    exe_obj = control.Agent()
    exe_obj.fuzzy_weight = fuzzy_weight
    exe_obj.tf_idf_weight = tf_idf_weight
    for each_data in test_data_ls:
        result = exe_obj.api(each_data[0])
        if result[0].strip() == each_data[1].strip() or result[0].strip() in each_data[1].strip() or each_data[1].strip() in result[0].strip():
            right_times += 1
    print("fuzzy_weight={}, tf_idf_weight={}".format(fuzzy_weight, tf_idf_weight))
    print("right times: {}, accuracy rate: {}".format(right_times, right_times/test_num))

