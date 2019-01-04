# -*- coding: utf-8 -*-

# Copyright (c) by 2018 Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

from random import choice
import pickle
import threading
import time

import jieba
from gensim.models.doc2vec import Doc2Vec, LabeledSentence
from sklearn.externals import joblib
import numpy as np

from retrieval_documents import Retrieval
from fuzzy_match import fuzzy_matching
from tf_idf import TfIdf
from config import config, frequency_domain


NUM_OF_IR = 20


class Agent:
    good_qualified_corpus = set()

    def __init__(self):
        self.config = config
        self.stop_words = ''
        self.punctuation_str = ''.join(self.config.punctuation_ls)
        self.frequency_domain_dict = frequency_domain.frequency_dict
        self.cluster_md = self.config.cluster_model
        self.vec_md = self.config.doc_vector_model
        self.init_all_states()
        self.fuzzy_weight = 0.15
        self.tf_idf_weight = 0.85
        self.good_corpus_threshold = 1000
        self.good_corpus_score = 0.99

    def init_all_states(self):
        self.retrieval = Retrieval(num_ir=NUM_OF_IR, config=self.config)
        self.tf_idf = TfIdf(self.config)
        self.cluster_model = joblib.load(self.cluster_md)
        self.vec_model = Doc2Vec.load(self.vec_md)
        self.load_stop_words(self.config)
        jieba.initialize()

    def get_utterance_type(self, utterance):
        tmp_vector = self.vec_model.infer_vector(utterance)
        label = self.cluster_model.predict(tmp_vector.reshape(1, -1))
        return self.config.cluster_file[label[0]]

    def record_good_conversations(self, utterance, score_ls, context_ls):
        def write_conversations():
            localtime = (time.asctime(time.localtime(time.time()))).replace(' ', '_').replace(':', '-')
            with open(self.config.path_of_good_conversation+localtime, 'wb') as wfp:
                pickle.dump(Agent.good_qualified_corpus, wfp)
            Agent.good_qualified_corpus.clear()
            # print(Agent.good_qualified_corpus)
        for index in range(len(score_ls)):
            if score_ls[index] > self.good_corpus_score:
                if context_ls[index][0] and context_ls[index][1]:
                    # print((utterance, context_ls[index][1]))
                    Agent.good_qualified_corpus.add((utterance, context_ls[index][1]))
        # print(len(Agent.good_qualified_corpus))
        if len(Agent.good_qualified_corpus) > self.good_corpus_threshold:
            record_thread = threading.Thread(target=write_conversations)
            record_thread.start()

    def random_chose_index(self, score_ls, max_score):
        max_score_indexes = []
        for i in range(len(score_ls)):
            if score_ls[i] == max_score:
                max_score_indexes.append(i)
        return choice(max_score_indexes)

    def load_stop_words(self, config):
        with open(config.stop_words, 'rb') as fpr:
            self.stop_words = pickle.load(fpr)

    def remove_special_words(self, stop_words_ls, input_sentence):
        sentence = input_sentence
        for special_word in self.config.special_modal_words:
            if special_word in sentence:
                sentence = sentence.replace(special_word, '')
        return sentence

    def response_answer(self, reply_msg, max_score):
        if type(max_score) is np.ndarray:
            final_max_score = max_score[0][0]
        else:
            final_max_score = max_score
        return reply_msg, final_max_score

    def get_answer(self, utterance, file_name=None):
        try:
            utterance = utterance.rstrip(self.punctuation_str)
            file_name = self.get_utterance_type(utterance)

            self.retrieval.read_indexes(file_name)
            context_ls = self.retrieval.search_sentences(utterance, self.stop_words)
            if not context_ls:
                return "", 0
            utterance_no_stop = self.remove_special_words(self.stop_words, utterance)
            new_context_ls = []
            for each_context in context_ls:
                ques = self.remove_special_words(self.stop_words, each_context[0])
                ans = self.remove_special_words(self.stop_words, each_context[1])
                if not ques or not ans:
                    new_context_ls.append((0, 0))
                    continue
                new_context_ls.append((ques, ans))
            # print("control!!!!!!!!!!!!!!!!!: {},{}".format(utterance, new_context_ls))
            # print(len(new_context_ls))
            fuzzy_ratio_ls = fuzzy_matching(utterance_no_stop, new_context_ls)

            self.tf_idf.select_model(file_name)
            self.tf_idf.predict_tfidf(utterance_no_stop, new_context_ls)
            tf_idf_score_ls = self.tf_idf.calculate_distances()

            if fuzzy_ratio_ls.count(max(fuzzy_ratio_ls)) > 1:
                fuzzy_best_index = self.random_chose_index(fuzzy_ratio_ls, max(fuzzy_ratio_ls))
            else:
                fuzzy_best_index = fuzzy_ratio_ls.index(max(fuzzy_ratio_ls))

            if tf_idf_score_ls.count(max(tf_idf_score_ls)) > 1:
                tftdf_best_index = self.random_chose_index(tf_idf_score_ls, max(tf_idf_score_ls))
            else:
                tftdf_best_index = tf_idf_score_ls.index(max(tf_idf_score_ls))

            fuzzy_best_content = context_ls[fuzzy_best_index][0].rstrip(self.punctuation_str)
            tfidf_best_content = context_ls[tftdf_best_index][0].rstrip(self.punctuation_str)
            if fuzzy_best_content == utterance or utterance.strip(''.join(config.special_modal_words)) in fuzzy_best_content:
                best_index = fuzzy_best_index
                # return context_ls[best_index][1], max(fuzzy_ratio_ls)
                return self.response_answer(context_ls[best_index][1], max(fuzzy_ratio_ls))

            if tfidf_best_content == utterance or utterance.strip(''.join(config.special_modal_words)) in tfidf_best_content:
                best_index = tftdf_best_index
                # return context_ls[best_index][1], max(tf_idf_score_ls)
                return self.response_answer(context_ls[best_index][1], max(tf_idf_score_ls))

            final_score_ls = [(fuzzy_ratio * self.fuzzy_weight + tf_tdf_score * self.tf_idf_weight) for fuzzy_ratio, tf_tdf_score in
                              zip(fuzzy_ratio_ls, tf_idf_score_ls)]
            # TODO: find a suitable weight
            self.record_good_conversations(utterance, final_score_ls, context_ls)
            max_score = max(final_score_ls)
            if final_score_ls.count(max_score) > 1:
                best_index = self.random_chose_index(final_score_ls, max_score)
            else:
                best_index = final_score_ls.index(max_score)
            # print("final result:{}".format(context_ls[best_index]))
            # print(type(max_score))
            return self.response_answer(context_ls[best_index][1], max_score)
        except Exception as e:
            return "", 0

    def test(self, utterance):
        answer = self.get_answer(utterance)
        return answer

    def start_cmd(self):
        while True:
            utterance = input(">>>")
            if utterance.strip() == "exit1":
                break
            answer, score = self.get_answer(utterance)
            print("<<<{}:{}".format(answer, score))

    def api(self, utterance):
        answer, score = self.get_answer(utterance)
        return [answer, score]

    def socket_get(self, utterance):
        answer, score = self.get_answer(utterance)
        # print(answer + '---' + str(score[0][0]))
        return answer + '---' + str(score)

#
# if __name__ == '__main__':
#     agent = Agent()
#     agent.start_cmd()
