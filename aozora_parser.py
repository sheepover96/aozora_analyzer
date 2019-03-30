from bs4 import BeautifulSoup as bs
import numpy as np

import re, sys, os

def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

def save_novel(file_path, text):
    if not os.path.exists(file_path):
        print('saved', file_path)
        with open(file_path, 'w') as f:
            f.write(text)

if __name__ == '__main__':
    pass

    cards = os.listdir('./cards')

    for card in cards:
        if card.isdecimal() and os.path.exists('./cards/' + card + '/files'):
            novels = os.listdir('./cards/' + card + '/files')
            for novel in novels:
                #print(novel[-4:])
                if novel[-4:] == 'html':
                    with open('./cards/' + card + '/files/' + novel, 'r') as f:
                        novel_page_html = f.read()
                        novel_parsed = bs(novel_page_html, 'html.parser')
                        novel_title = novel_parsed.find('h1', class_='title')
                        novel_author = novel_parsed.find('h2', class_='author')
                        novel_content = novel_parsed.find('div', class_='main_text')
                        if novel_author is not None and novel_author.string is not None:
                            make_dir('./novels/' + novel_author.string)
                            save_novel('./novels/' + novel_author.string + '/' + novel_title.string, novel_content.text)