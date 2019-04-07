import MeCab as mecab
from sklearn.feature_extraction.text import TfidfVectorizer

import pickle, sys, os

NOVEL_ROOT_DIR = './novels'

TF_IDF_VEC = 'tf_idf_vec.pickle'
VECTORIZER = 'vectorizer.pickle'


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

def tf_idf(corpus):
    vectorizer = TfidfVectorizer(tokenizer=tokenizer, decode_error='ignore')
    tf_idf_vec = vectorizer.fit(corpus)

    return tf_idf_vec, vectorizer

def main():
    novel_title = []
    corpus = []
    author_list = [file_name for file_name in os.listdir(NOVEL_ROOT_DIR) if not file_name.startswith('.')]
    for author in author_list:
        novel_list = [file_name for file_name in os.listdir(os.path.join(NOVEL_ROOT_DIR, author)) if not file_name.startswith('.')]
        for novel in novel_list:
            with open(os.path.join(NOVEL_ROOT_DIR, author, novel), 'r') as f:
                novel_content = f.read()
                novel_title.append(author + ' | ' + novel)
                print(len(tokenizer(novel_content)))
                corpus.append(novel_content)

    tf_idf_vec, vectorizer = tf_idf(corpus)

    with open(os.path.join('./pickle', TF_IDF_VEC), 'wb') as f:
        pickle.dump(tf_idf_vec, f)

    with open(os.path.join('./pickle', VECTORIZER), 'wb') as f:
        pickle.dump(vectorizer, f)


if __name__ == '__main__':
    main()