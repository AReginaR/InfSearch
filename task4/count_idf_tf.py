from task3.boolean_search import get_all_indexes
from math import log
import os
import re

from bs4 import BeautifulSoup
from nums_from_string import nums_from_string

from task3.inverted_index import get_lemmas_from_file
from task3.inverted_index_token import get_token_from_file
from task2.tokenise_helper import tag_visible, lemmatize_text2

lemmas_file_path = '../result/index.txt'
tokens_file_path = '../result/index_token.txt'

LEMMAS_INDEXES = get_all_indexes(lemmas_file_path)
TOKEN_INDEXES = get_all_indexes(tokens_file_path)


def count_idf(word, type):
    if type == 'lemmas':
        num_of_docs = len(LEMMAS_INDEXES[word])
    else:
        num_of_docs = len(TOKEN_INDEXES[word])
    return log(100 / num_of_docs)


pages_texts = dict()
for page in os.listdir('../pages/'):
    with open('../pages/' + page, 'r', encoding='utf-8') as file:
        counter = int(nums_from_string.get_nums(page)[0])
        page_context = file.read()
        soup = BeautifulSoup(page_context, features="html.parser")
        page_text = soup.findAll(text=True)
        visible_texts = filter(tag_visible, page_text)
        file_content_text = u" ".join(t.strip() for t in visible_texts)
        pages_texts[counter] = file_content_text.lower()


def count_tf(tokens_dict_idf, lemmas_dict_idf):
    for i, page in pages_texts.items():
        tokens_from_dict, lemmas = list(), dict()
        tokens_list, lemmas_dict = lemmatize_text2(
            page, tokens_from_dict, lemmas
        )
        count_token = dict()
        for token_ in set(tokens_list):
            count_token[token_] = 0
        for word in tokens_list:
            count_token[word] += 1
        n = len(tokens_list)
        count_lemmas = dict()
        for lemma_from_dict, tokens_from_dict in lemmas_dict.items():
            for t in tokens_from_dict:
                if lemma_from_dict in count_lemmas:
                    count_lemmas[lemma_from_dict] += count_token[t]
                else:
                    count_lemmas[lemma_from_dict] = count_token[t]
        with open(f'../result/tokens_tf_idf/{i}.txt', 'w', encoding='utf-8') as tokens_file:
            for t, k in count_token.items():
                if t in tokens_dict_idf:
                    token_tf = k / n
                    token_tf_idf = tokens_dict_idf[t] * token_tf
                    tokens_file.write(t + ' ' + str(tokens_dict_idf[t]) + ' ' + str(token_tf_idf) + '\n')
        with open(f'../result/lemmas_tf_idf/{i}.txt', 'w', encoding='utf-8') as lemmas_file:
            for t, k in count_lemmas.items():
                if t in lemmas_dict_idf:
                    lemma_tf = k / n
                    lemma_tf_idf = lemmas_dict_idf[t] * lemma_tf
                    lemmas_file.write(t + ' ' + str(lemmas_dict_idf[t]) + ' ' + str(lemma_tf_idf) + '\n')


if __name__ == '__main__':
    lemmas = get_lemmas_from_file()
    lemmas_idf = dict()
    tokens_idf = dict()

    for lemma, tokens in lemmas.items():
        lemma_idf = count_idf(lemma, 'lemmas')
        lemmas_idf[lemma] = lemma_idf
        for token in tokens:
            token_idf = count_idf(token, 'tokens')
            tokens_idf[token] = token_idf

    count_tf(tokens_idf, lemmas_idf)
