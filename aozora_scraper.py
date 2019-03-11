import numpy as np
import pandas as pd

from bs4 import BeautifulSoup as bs
import urllib

import re, sys, os, time

NOVEL_SAVE_DIR = './novels'

ROOT_URL = 'https://www.aozora.gr.jp/'
MIDDLE_URI = 'index_pages/'
SLEEP_SECONDS = 2


def remove_tail_filename(text, target_word):
    position = 0
    for letter in reversed(text):
        if letter == target_word:
            break
        else:
            position += 1
    return text[:-position]

def make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

def is_downloaded(author_name, downloaded_author_list):
    for author in downloaded_author_list:
        if author_name in author:
            return True
    return False


def save_novel(file_path, text):
    if not os.path.exists(file_path):
        print('saved', file_path)
        with open(file_path, 'w') as f:
            f.write(text)

if __name__ == '__main__':

    downloaded_author_list = os.listdir('./novels')

    with urllib.request.urlopen(ROOT_URL) as response:
        aozora_top = response.read()

    time.sleep(SLEEP_SECONDS)

    toppage_soup = bs(aozora_top, 'html.parser')
    idx_link_list = toppage_soup.find_all(href=re.compile('person'))
    print(idx_link_list[0].string)

    try:
        # get author list
        for idx_link in idx_link_list:
            with urllib.request.urlopen(ROOT_URL + idx_link.get('href')) as response:
                author_list = response.read()
            time.sleep(SLEEP_SECONDS)
            author_list_soup = bs(author_list, 'html.parser')
            author_link_list = author_list_soup.find_all(href=re.compile('person[0-9]+'))
            # get novel list
            for author_link in author_link_list:
                with urllib.request.urlopen(ROOT_URL + MIDDLE_URI + author_link.get('href')) as response:
                    author_list = response.read()
                time.sleep(SLEEP_SECONDS)
                author_list_soup = bs(author_list, 'html.parser')
                novel_link_list = author_list_soup.find_all(href=re.compile('person[0-9]+'))
                # get novel detail
                for novel_link in novel_link_list:
                    novel_link_author = novel_link.string
                    print(novel_link_author)
                    if is_downloaded(novel_link_author, downloaded_author_list):
                        print('donwnload')
                        with urllib.request.urlopen(ROOT_URL + MIDDLE_URI + author_link.get('href')) as response:
                            novel_detail_list = response.read()
                        time.sleep(SLEEP_SECONDS)
                        novel_detail_list_soup = bs(novel_detail_list, 'html.parser')
                        novel_detail_link_list = novel_detail_list_soup.find_all(href=re.compile('card[0-9]+'))
                        # download novel
                        for novel_detail_link in novel_detail_link_list:
                            novel_detail_complete_link = ROOT_URL + novel_detail_link.get('href')[3:]
                            with urllib.request.urlopen(novel_detail_complete_link) as response:
                                novel_detail = response.read()
                            time.sleep(SLEEP_SECONDS)
                            # access to xhtml
                            novel_detail_soup = bs(novel_detail, 'html.parser')
                            novel_detail_parent = remove_tail_filename(novel_detail_complete_link, '/')
                            novel_link = novel_detail_soup.find(href=re.compile('\./files.+html'))
                            if novel_link is not None:
                                novel_html_complete_link = novel_detail_parent + novel_link.get('href')[2:]
                                with urllib.request.urlopen(novel_html_complete_link) as response:
                                    novel_html = response.read()
                                time.sleep(SLEEP_SECONDS)
                                try:
                                    novel_html_soup = bs(novel_html, 'html.parser')
                                    novel_title = novel_html_soup.find('h1', class_='title')
                                    novel_author = novel_html_soup.find('h2', class_='author')
                                    novel_content = novel_html_soup.find('div', class_='main_text')
                                    print(novel_title.string)
                                    print(novel_author.string)
                                    make_dir('novels/' + novel_link_author)
                                    save_novel('novels/' + novel_link_author + '/' + novel_title.string, novel_content.text)
                                    #print(novel_content.text)
                                except AttributeError as e:
                                    print(e)
                                    print(novel_link)
                                except urllib.error.URLError as e2:
                                    print(e2)
                                    print(novel_link)
                                except OSError as e3:
                                    print(e3)
                                    print(novel_link)
                                except urllib.error.HTTPError as e4:
                                    print(e4)
                                    print(novel_link)
                    else:
                        print('skip')
    except:
        import traceback
        traceback.print_exc()
