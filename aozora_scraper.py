import numpy as np
import pandas as pd

from bs4 import BeautifulSoup as bs
import urllib

import re, sys, os, time


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
        


if __name__ == '__main__':

    with urllib.request.urlopen(ROOT_URL) as response:
        aozora_top = response.read()

    time.sleep(SLEEP_SECONDS)

    toppage_soup = bs(aozora_top, 'html.parser')
    idx_link_list = toppage_soup.find_all(href=re.compile('person'))

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
                    novel_html_complete_link = novel_detail_parent + novel_link.get('href')[2:]
                    with urllib.request.urlopen(novel_html_complete_link) as response:
                        novel_html = response.read()
                    novel_html_soup = bs(novel_html, 'html.parser')
                    print(novel_html_soup)


