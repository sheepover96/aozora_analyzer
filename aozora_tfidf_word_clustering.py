from sklearn.cluster import KMeans
from gensim.models import word2vec
import numpy as np

import os, sys

from utils.pickle_helper import pickle_load, pickle_dump
from utils.tokenizers import tokenizer

DATASET_DIR = './novels'
MODEL_PATH = './pickle_objects/aozora_w2v.pickle'
MODEL_PATH2 = './pickle_objects/aozora_w2v.model'


def main():
    w2vmodel = word2vec.Word2Vec.load(MODEL_PATH2)
    vocab = w2vmodel.wv.vocab.keys()
    words_array = []
    for word in vocab:
        words_array.append(w2vmodel[word])
    print('clustering')
    words_array_np = np.array(words_array)
    kmeans_res = KMeans(n_clusters=300, max_iter=1).fit(words_array_np)
    print(kmeans_res)


if __name__ == '__main__':
    main()

