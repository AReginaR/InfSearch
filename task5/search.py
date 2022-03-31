from collections import OrderedDict

from task3.boolean_search import lemmatize_query, get_all_indexes
from nums_from_string import nums_from_string
import os
import re


def get_tf_idf():
    all = dict()
    for page in os.listdir('result/lemmas_tf_idf'):
        with open('result/lemmas_tf_idf/' + page, 'r', encoding='utf-8') as file:
            counter = int(nums_from_string.get_nums(page)[0])
            res = dict()
            for line in file.readlines():
                str = re.split(r' ', line[:-1])
                res[str[0]] = [float(str[1]), float(str[2])]
            all[counter] = res
    return all


indexes = get_all_indexes('result/index.txt')


def get_links(file_path):
    with open(file_path, 'r') as file:
        links_dict = {}
        for line in file.readlines():
            line = line.split('. ')
            links_dict[line[0]] = line[1]
    return links_dict


def vector_search(query: str, docs_dict, tf_idf_dict, num_of_results=None):
    if len(query.split(' ')) >= 1:
        lemmatized_query = lemmatize_query(query)
    else:
        raise Exception('Empty query')

    query_words = []
    for word, tokens in lemmatized_query.items():
        if word not in query_words:
            query_words.append(word)

    query_word_count = {}
    for word in query_words:
        query_word_count[word] = query.lower().split().count(word)

    scores = {}
    for doc_id in docs_dict.keys():
        doc_id = int(doc_id)
        score = 0
        for word in query_words:
            if word in tf_idf_dict[doc_id]:
                if tf_idf_dict[doc_id][word][1] != 0:
                    score += query_word_count[word] * tf_idf_dict[doc_id][word][1]
                else:
                    score += query_word_count[word]
        scores[doc_id] = score
    sorted_result_values = OrderedDict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    if num_of_results:
        result = {k: sorted_result_values[k] for k in list(sorted_result_values)[:num_of_results] if
                  sorted_result_values[k] != 0}
    else:
        result = {k: sorted_result_values[k] for k in list(sorted_result_values) if sorted_result_values[k] != 0}

    search_result = dict()
    for k, res in result.items():
        search_result[k] = docs_dict[str(k)][:-1]
    return search_result


doc_dict = get_links('index.txt')
tfidf_scr = get_tf_idf()

print(vector_search("пожарный", doc_dict, tfidf_scr))


def search(q):
    return vector_search(q, doc_dict, tfidf_scr)
