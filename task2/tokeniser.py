import os
import re
from bs4 import BeautifulSoup

from task2.tokenise_helper import tag_visible, lemmatize_text

tokens, lemmas = set(), dict()

for page in os.listdir('../pages/'):
    with open('../pages/' + page, 'r', encoding='utf-8') as file:
        page_context = file.read()
        soup = BeautifulSoup(page_context, features="html.parser")
        page_text = soup.findAll(text=True)
        visible_texts = filter(tag_visible, page_text)
        file_content_text = u" ".join(t.strip() for t in visible_texts)
        tokens, lemmas = lemmatize_text(
            file_content_text, tokens, lemmas
        )

with open('../result/tokens.txt', 'w', encoding='utf-8') as tokens_file:
    for token in tokens:
        tokens_file.write(token + '\n')

with open('../result/lemmas.txt', 'w', encoding='utf-8') as lemmas_file:
    for key in lemmas:
        lemma = key
        k = 1
        for value in lemmas[key]:
            if k == 1:
                lemma = lemma + ': ' + value
                k += 1
            else:
                lemma = lemma + ' ' + value
        lemmas_file.write(lemma + '\n')
