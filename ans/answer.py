import sys
import numpy as np
import nltk
import spacy
from spacy.vocab import Vocab
from spacy.language import Language
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from collections import Counter
from fuzzywuzzy import fuzz


def read_article(article_file):
    nlp = spacy.load('en_core_web_sm')
    with open(article_file, 'r') as f:
        article = f.read()
    about_article = nlp((article))
    article_sentences = list(about_article.sents)
    return article_sentences


def read_questions(questions_file):
    questions = []
    with open(questions_file, 'r') as f:
        for line in f:
            question = line.strip()
            # question = word_tokenize(question)
            # token_tag = pos_tag(question)
            questions.append(question)
    return questions


def question_article_similarity(questions, article, top_k):
    dict = {}
    for question in questions:
        dic = {}
        for i, sentence in enumerate(article):
            dic[i] = fuzz.partial_ratio(question, str(sentence))
        k = Counter(dic)
        high = k.most_common(top_k)
        res = [article[item[0]] for item in high]
        dict[question] = res
    return dict


if __name__ == '__main__':
    article_file, questions_file = sys.argv[1:]
    article = read_article(article_file)
    questions = read_questions(questions_file)
    dict = question_article_similarity(questions, article, 3)
    for i, (key, v) in enumerate(dict.items()):
        print("\nQuestion {}: {}".format(i+1, key))
        print("\nAnswers:")
        for i in range(len(v)):
            print("{}. {}".format(i+1, v[i]))
