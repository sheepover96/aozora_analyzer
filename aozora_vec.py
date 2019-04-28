from gensim.models import word2vec

import os, sys

from utils.pickle_helper import pickle_load, pickle_dump
from utils.tokenizers import tokenizer

DATASET_DIR = './novels'
MODEL_PATH = './pickle_objects/aozora_w2v_nonormalize.pickle'
MODEL_PATH2 = './pickle_objects/aozora_w2v2_nonormalize.model'

def main():
    novel2idx = pickle_load('./pickle_objects/novel2idx.pickle')

    all_novel_lines = []
    for author in novel2idx.keys():
        for novel in novel2idx[author]:
            with open(os.path.join(DATASET_DIR, author, novel), 'r') as f:
                novel_content = f.read()
                novel_text_lines = novel_content.split('\n')
                tokenized_novel_text_lines = [ tokenizer(text_line, part_use=None, normalize_word=False) for text_line in novel_text_lines]
                all_novel_lines.extend(tokenized_novel_text_lines)
    print('training')
    model = word2vec.Word2Vec(all_novel_lines, iter=100)
    pickle_dump(model, MODEL_PATH)
    model.save(MODEL_PATH2)


if __name__ == '__main__':
    main()
