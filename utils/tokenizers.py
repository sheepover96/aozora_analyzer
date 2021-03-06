import MeCab as mecab

hiragana = [ chr(i) for i in range(12354, 12436)]
with open('stop_words.txt', 'r') as f:
    content = f.read()
    stopwords = [word for word in content.split('\n')]
stopwords.extend(hiragana)

def tokenizer(words, part_use=['名詞', '形容詞'], normalize_word=True):
    tagger = mecab.Tagger('-d /usr/local/mecab/lib/mecab/dic/mecab-ipadic-neologd ')
    tagger.parse('')
    mecab_word_nodes = tagger.parseToNode(words)
    tokenized = []
    while mecab_word_nodes:
        elements = mecab_word_nodes.feature
        word = mecab_word_nodes.surface
        element_list = elements.split(',')
        if normalize_word:
            word = element_list[6]
        part = element_list[0]

        if not word in stopwords:
            if part is None or part_use is None:
                tokenized.append(word)
            elif part in part_use and not word.encode('utf-8').isalnum():
                tokenized.append(word)

        mecab_word_nodes = mecab_word_nodes.next

    return tokenized
