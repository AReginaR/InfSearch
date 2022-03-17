import os
import re

from bs4 import BeautifulSoup
from nums_from_string import nums_from_string
from task2.tokenise_helper import tag_visible


def get_lemmas_from_file():
    text_file = open('../result/lemmas.txt', 'r')
    tokens = dict()
    for line in text_file.readlines():
        s = re.split(r': ', line[:-1])
        tokens[s[0]] = re.split(r' ', s[1])
    return tokens


def create_index(texts, terms):
    index = dict()
    for term, arr in terms.items():
        for token in arr:
            for i, text in texts.items():
                if token in texts[i]:
                    if term not in index:
                        index[term] = [i]
                    else:
                        if i not in index[term]:
                            index[term].append(i)
    return index


page_texts = dict()
for page in os.listdir('../pages/'):
    with open('../pages/' + page, 'r', encoding='utf-8') as file:
        counter = int(nums_from_string.get_nums(page)[0])
        page_context = file.read()
        soup = BeautifulSoup(page_context, features="html.parser")
        page_text = soup.findAll(text=True)
        visible_texts = filter(tag_visible, page_text)
        file_content_text = u" ".join(t.strip() for t in visible_texts)
        file_content_text = re.sub(r"\W", "", file_content_text, flags=re.I)
        page_texts[counter] = file_content_text.lower()

lemmas = get_lemmas_from_file()

inv_index = create_index(page_texts, lemmas)

with open('../result/index.txt', 'w') as index_file:
    for key, val in inv_index.items():
        index_file.write('{}:'.format(key))
        for v in val:
            index_file.write(' {}'.format(v))
        index_file.write('\n')
