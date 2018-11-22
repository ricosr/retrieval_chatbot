# -*- coding: utf-8 -*-

# chinese computing project
# Copyright (c) 2018 by Sun Rui, Mo Feiyu, Wang Zizhe, Liang Zhixuan

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def load_files(path):
    pass

def train(data):
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.append(data.Context.values, data.Utterance.values))

# def predict(self, context, utterances):
#     # Convert context and utterances into tfidf vector
#     vector_context = self.vectorizer.transform([context])
#     vector_doc = self.vectorizer.transform(utterances)
#     # The dot product measures the similarity of the resulting vectors
#     result = np.dot(vector_doc, vector_context.T).todense()
#     result = np.asarray(result).flatten()
#     # Sort by top results and return the indices in descending order
#     return np.argsort(result, axis=0)[::-1]
