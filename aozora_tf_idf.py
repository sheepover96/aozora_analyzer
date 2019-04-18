import MeCab as mecab
from sklearn.feature_extraction.text import TfidfVectorizer

import pickle, sys, os

from utils.pickle_helper import pickle_dump, pickle_load

NOVEL_ROOT_DIR = './novels'

NOVEL_TO_IDX = 'novel2idx.pickle'
IDX_TO_NOVEL = 'idx2novel.pickle'
TF_IDF_VEC = 'tf_idf_vec_sw.pickle'
VECTORIZER = 'vectorizer_sw.pickle'


hiragana = [ chr(i) for i in range(12354, 12436)]
with open('stop_words.txt', 'r') as f:
    content = f.read()
    stopwords = [word for word in content.split('\n')]
stopwords.extend(hiragana)

def tokenizer(words, part_use=['名詞', '形容詞']):
    tagger = mecab.Tagger('-d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd ')
    tagger.parse('')
    mecab_word_nodes = tagger.parseToNode(words)
    tokenized = []
    while mecab_word_nodes:
        elements = mecab_word_nodes.feature
        word = mecab_word_nodes.surface
        element_list = elements.split(',')
        gen_word = element_list[6]
        part = element_list[0]

        if not gen_word in stopwords: 
            if part is None:
                tokenized.append(gen_word)
            else:
                if part in part_use and not gen_word.encode('utf-8').isalnum():
                    tokenized.append(gen_word)

        mecab_word_nodes = mecab_word_nodes.next

    return tokenized

def tf_idf(corpus):
    vectorizer = TfidfVectorizer(tokenizer=tokenizer, min_df=0.05, decode_error='ignore')
    tf_idf_vec = vectorizer.fit_transform(corpus)

    return tf_idf_vec, vectorizer

def main():

    idx2novel = []
    novel2idx = {}
    corpus = []
    author_list = [file_name for file_name in os.listdir(NOVEL_ROOT_DIR) if not file_name.startswith('.')]
    idx = 0
    for author in author_list:
        novel_list = [file_name for file_name in os.listdir(os.path.join(NOVEL_ROOT_DIR, author)) if not file_name.startswith('.')]
        for novel in novel_list:
            if not author in novel2idx:
                novel2idx[author] = {}
            novel2idx[author][novel] = idx
            with open(os.path.join(NOVEL_ROOT_DIR, author, novel), 'r') as f:
                novel_content = f.read()
                idx2novel.append(author + ' | ' + novel)
                #corpus.append(novel_content)

            idx += 1
    tf_idf_vec, vectorizer = tf_idf(corpus)

    pickle_dump(novel2idx, os.path.join('./pickle_objects', NOVEL_TO_IDX))
    pickle_dump(idx2novel, os.path.join('./pickle_objects', IDX_TO_NOVEL))
    pickle_dump(tf_idf_vec, os.path.join('./pickle_objects', TF_IDF_VEC))
    pickle_dump(vectorizer, os.path.join('./pickle_objects', VECTORIZER))


if __name__ == '__main__':
    main()