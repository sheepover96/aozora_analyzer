from selenium import webdriver
import MeCab as mecab
import numpy as np

import sys, os, pickle
from pprint import pprint

from utils.image_scraper import search_and_save

BASE_URL = 'https://www.google.co.jp/search?q={}&tbm=isch'
SAVE_ROOT_DIR = './imgs'
DOWNLOAD_NUM = 10

def tokenizer(words, part_use=['名詞', '形容詞']):
    tagger = mecab.Tagger('-d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd ')
    tagger.parse('')
    mecab_word_nodes = tagger.parseToNode(words)
    tokenized = []
    while mecab_word_nodes:
        elements = mecab_word_nodes.feature
        word = mecab_word_nodes.surface
        element_list = elements.split(',')
        part = element_list[0]

        if part is None:
            tokenized.append(word)
        else:
            if part in part_use:
                tokenized.append(word)

        mecab_word_nodes = mecab_word_nodes.next

    return tokenized

with open('./pickle_objects/tf_idf_vec_sw.pickle', 'rb') as f:
    tf_idf_vec = pickle.load(f)

with open('./pickle_objects/vectorizer_sw.pickle', 'rb') as f:
    vectorizer = pickle.load(f)

tf_idf_vec_arr = tf_idf_vec.toarray()
feature_word_idx = tf_idf_vec_arr.argsort(axis=1)[:,::-1]
feature_names = np.array(vectorizer.get_feature_names())
feature_words = feature_names[feature_word_idx]

for idx1, words in enumerate(feature_words):
    for idx2, word in enumerate(words[:10]):
        print(word)
        img_tapple_list = search_and_save(word, DOWNLOAD_NUM, 0)
        for idx3, img_tapple in enumerate(img_tapple_list):
            img = img_tapple[0]
            extension = '.' + img_tapple[1]
            img_name = '-'.join([str(idx1), str(idx2), str(idx3)]) + extension
            img.save(os.path.join(SAVE_ROOT_DIR, img_name))

