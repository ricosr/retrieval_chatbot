# -*- coding: utf-8 -*-

# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan


cluster_file = {0: "cluster_0", 1: "cluster_1", 2: "cluster_2", 3: "cluster_3", 4: "cluster_4",
                5: "cluster_5", 6: "cluster_6", 7: "cluster_7", 8: "cluster_8", 9: "cluster_9"
                }

file_dict = {"cluster_0": "data/cluster_0.pkl", "cluster_1": "data/cluster_1.pkl", "cluster_2": "data/cluster_2.pkl",
             "cluster_3": "data/cluster_3.pkl", "cluster_4": "data/cluster_4.pkl", "cluster_5": "data/cluster_5.pkl",
             "cluster_6": "data/cluster_6.pkl", "cluster_7": "data/cluster_7.pkl", "cluster_8": "data/cluster_8.pkl",
             "cluster_9": "data/cluster_9.pkl"
             }

index_dict = {"cluster_0": "index/cluster_0", "cluster_1": "index/cluster_1", "cluster_2": "index/cluster_2",
              "cluster_3": "index/cluster_3", "cluster_4": "index/cluster_4", "cluster_5": "index/cluster_5",
              "cluster_6": "index/cluster_6", "cluster_7": "index/cluster_7", "cluster_8": "index/cluster_8",
              "cluster_9": "index/cluster_9"
              }

model_dict = {"cluster_0": "model/cluster_0.pkl", "cluster_1": "model/cluster_1.pkl", "cluster_2": "model/cluster_2.pkl",
              "cluster_3": "model/cluster_3.pkl", "cluster_4": "model/cluster_4.pkl", "cluster_5": "model/cluster_5.pkl",
              "cluster_6": "model/cluster_6.pkl", "cluster_7": "model/cluster_7.pkl", "cluster_8": "model/cluster_8.pkl",
              "cluster_9": "model/cluster_9.pkl"
              }

cluster_model = "cluster_model/kmeans.pkl"

doc_vector_model = "vec_model/doc_vec"

punctuation_ls = ['`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=',
                  '{', '[', '}', ']', '|', '\\', ':', ';', '\'', '\"', '<', ',', '>', '.', '?', '/',
                  '！', '·', '￥', '……', '（', '）', '——', '【', '】', '、', '：', '；', '’', '‘', '“',
                  '”', '《', '，', '。', '》', '？']

stop_words = "stopwords/all_stop.pkl"

special_modal_words = ['啊', '呢', '了', '吧', '吗', '呀', '噻', '哈', '呦', '的', '哎', '我', '你', '他', '今天', '明天',
                       '昨天', '去', '走', '这', '那']

path_of_good_conversation = "good_conversations/"

# three dictionaries has same keys corresponding the pickle files and searching indexes
# index_dict = {"AI": "index/AI", "profile": "index/profile", "conversations": "index/conversations",
#              "emotion": "index/emotion", "food": "index/food", "gossip": "index/gossip",
#              "greetings": "index/greetings", "history": "index/history", "humor": "index/humor",
#              "literature": "index/literature", "money": "index/money", "movies": "index/movies",
#              "politics": "index/politics", "psychology": "index/psychology", "science": "index/science",
#              "sports": "index/sports", "trivia": "index/trivia", "xiaohuangji": "index/xiaohuangji",
#              "weibo": "index/weibo", "domains": "index/domains"}
#
# file_dict = {"AI": "data/AI.pkl", "profile": "data/profile.pkl", "conversations": "data/conversations.pkl",
#              "emotion": "data/emotion.pkl", "food": "data/food.pkl", "gossip": "data/gossip.pkl",
#              "greetings": "data/greetings.pkl", "history": "data/history.pkl", "humor": "data/humor.pkl",
#              "literature": "data/literature.pkl", "money": "data/money.pkl", "movies": "data/movies.pkl",
#              "politics": "data/politics.pkl", "psychology": "data/psychology.pkl", "science": "data/science.pkl",
#              "sports": "data/sports.pkl", "trivia": "data/trivia.pkl", "xiaohuangji": "data/xiaohuangji.pkl",
#              "weibo": "data/weibo.pkl", "domains": "data/domains.pkl"}
#
# model_dict = {"AI": "model/AI.pkl", "profile": "model/profile.pkl", "conversations": "model/conversations.pkl",
#              "emotion": "model/emotion.pkl", "food": "model/food.pkl", "gossip": "model/gossip.pkl",
#              "greetings": "model/greetings.pkl", "history": "model/history.pkl", "humor": "model/humor.pkl",
#              "literature": "model/literature.pkl", "money": "model/money.pkl", "movies": "model/movies.pkl",
#              "politics": "model/politics.pkl", "psychology": "model/psychology.pkl", "science": "model/science.pkl",
#              "sports": "model/sports.pkl", "trivia": "model/trivia.pkl", "xiaohuangji": "model/xiaohuangji.pkl",
#              "weibo": "model/weibo.pkl", "domains": "model/domains.pkl"}