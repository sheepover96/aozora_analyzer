from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

import os, sys

from utils.pickle_helper import pickle_load, pickle_dump
from utils.tokenizers import tokenizer

DATASET_DIR = './novels'
#MODEL_PATH = './pickle_objects/aozora_w2v_nonormalize.pickle'
MODEL_PATH2 = './pickle_objects/aozora_doc2vec_nonormalize.model'

def main():
    novel2idx = pickle_load('./pickle_objects/novel2idx.pickle')

    all_novel_list = []
    for author_idx, author in enumerate(novel2idx.keys()):
        for novel in novel2idx[author]:
            novel_words = []
            novel_idx = novel2idx[author][novel]
            with open(os.path.join(DATASET_DIR, author, novel), 'r') as f:
                novel_content = f.read()
                novel_text_lines = novel_content.split('\n')
                for text_line in novel_text_lines: 
                    novel_words.extend(tokenizer(text_line, part_use=None, normalize_word=False))
            all_novel_list.append(TaggedDocument(words=novel_words, tags=[author_idx, novel_idx]))
    print('training')
    model = Doc2Vec(all_novel_list, size=300, iter=100)
    #pickle_dump(model, MODEL_PATH)
    model.save(MODEL_PATH2)


if __name__ == '__main__':
    main()

