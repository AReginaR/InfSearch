import re

from task2.tokenise_helper import lemmatize_text


def get_all_indexes():
    text_file = open('../result/index.txt', 'r')
    indexes = dict()
    for line in text_file.readlines():
        terms = re.split(r': ', line[:-1])
        indexes[terms[0]] = list(map(int, re.split(r' ', terms[1])))
    return indexes


def lemmatize_query(query):
    _, lemmas = set(), dict()
    _, lemmas = lemmatize_text(query, _, lemmas)
    return lemmas


def get_index(query):
    inverted_index = get_all_indexes()
    search = dict()
    for term in query:
        if term in inverted_index.keys():
            search[term] = inverted_index[term]
        else:
            search[term] = list()
    return search


def boolean_search(search_type, search_request):
    terms = list(search_request.keys())
    if not search_request:
        raise Exception('Empty search request')
    else:
        search_result = search_request[terms[0]]
    for term in terms[1:]:
        if search_type == 'AND':
            search_result = list(set(search_result) & set(search_request[term]))
        elif search_type == 'OR':
            search_result = list(set(search_result) | set(search_request[term]))
        else:
            raise Exception('Wrong search type')
    return search_result


text_query = 'Пожарный Майк обнаружил малышку в огне'
query_lemmas = lemmatize_query(text_query)
request = get_index(query_lemmas)
result = boolean_search('AND', request)
print(result)
