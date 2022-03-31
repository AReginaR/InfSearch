import pymorphy2
import nltk
import re

from nltk.corpus import stopwords
from bs4.element import Comment

nltk.download('punkt')
nltk.download("stopwords")
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_ru')

functors_pos = {'CONJ', 'ADV-PRO', 'CONJ', 'PART', 'PR'}


# function for checking if text in an html file is visible
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def lemmatize_text(text: str, result_tokens: set, result_lemmas: dict):
    text = re.sub('-', ' ', text)
    tokens = nltk.word_tokenize(text, language="russian")
    tokens = remove_stop_words(tokens)
    morph = pymorphy2.MorphAnalyzer()
    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        result_tokens.add(token)
        lemma_tokens_in_dict = result_lemmas.get(lemma)
        if lemma_tokens_in_dict is None:
            result_lemmas[lemma] = [token]
        else:
            if token not in lemma_tokens_in_dict:
                result_lemmas[lemma] = lemma_tokens_in_dict + [token]
    return result_tokens, result_lemmas


def lemmatize_text2(text: str, result_tokens: list, result_lemmas: dict):
    text = re.sub('-', ' ', text)
    tokens = nltk.word_tokenize(text, language="russian")
    tokens = remove_stop_words(tokens)
    morph = pymorphy2.MorphAnalyzer()
    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        result_tokens.append(token)
        lemma_tokens_in_dict = result_lemmas.get(lemma)
        if lemma_tokens_in_dict is None:
            result_lemmas[lemma] = [token]
        else:
            if token not in lemma_tokens_in_dict:
                result_lemmas[lemma] = lemma_tokens_in_dict + [token]
    return result_tokens, result_lemmas


def remove_stop_words(tokens):
    tokens = [re.sub(r"\W", "", token, flags=re.I) for token in tokens]
    stop_words = stopwords.words('russian')
    only_cyrillic_letters = re.compile('[а-яА-Я]')

    tokens = [token.lower() for token in tokens if (token not in stop_words)
              and only_cyrillic_letters.match(token)
              and (not len(token) == 1 or token == 'я')
              and not token.isdigit()
              and token != '']

    tokens = [token for token, pos in nltk.pos_tag(tokens, lang='rus')
              if pos not in functors_pos]

    return tokens
