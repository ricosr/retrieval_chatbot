# -*- coding: utf-8 -*-

from retrieval_documents import Retrieval
from calculate_distances import TfIdf

# TODO: distribute message by threading or tornado

NUM_OF_IR = 10
DOCUMENTS_PATH = []
MODEL_PATH = []


def start():
    retrieval = Retrieval(10, DOCUMENTS_PATH)
    retrieval.load_documents()
    retrieval.add_indexes()

    tf_idf = TfIdf(MODEL_PATH)

    while True:
        utterance = input(">>>")
        context_ls = retrieval.search_sentences(utterance)
        tf_idf.calculate_tfidf(utterance, context_ls)
        best_index = tf_idf.calculate_distances()
        print("<<<{}".format(context_ls[best_index]))

if __name__ == '__main__':
    start()
