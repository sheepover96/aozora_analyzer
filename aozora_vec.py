from gensim.models import word2vec

import os, sys

from utils.pickle_helper import pickle_load, pickle_dump
from utils.tokenizers import tokenizer

DATASET_DIR = './novels'
MODEL_PATH = './pickle_objects/aozora_w2v.pickle'

def main():
    novel2idx = pickle_load('./pickle_objects/novel2idx.pickle')

    all_novel_lines = []
    for author in novel2idx.keys():
        for novel in novel2idx[author]:
            with open(os.path.join(DATASET_DIR, author, novel), 'r') as f:
                print(author)
                novel_content = f.read()
                novel_text_lines = novel_content.split('\n')
                print(type(novel_text_lines))
                tokenized_novel_text_lines = [ tokenizer(text_line, part_use=None) for text_line in novel_text_lines]
                all_novel_lines.append(tokenized_novel_text_lines)
    
    model = word2vec.Word2Vec(all_novel_lines, iter=2)
    pickle_dump(model, MODEL_PATH)


if __name__ == '__main__':
    main()
