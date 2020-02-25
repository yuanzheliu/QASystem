import sys
import numpy as np
import nltk
import spacy
from nltk import word_tokenize, pos_tag,sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
from fuzzywuzzy import process
from TopKsentence import *

class QuestionType():
    def __init__(self,question_file):
        self.question_file = question_file


if __name__ == '__main__':
    article_file, questions_file = sys.argv[1:]
    GS = GetSentences(article_file, questions_file, 3)
    article_sentence = GS.read_article()
    questions = GS.read_questions()
    dict = GS.question_article_similarity()
    for i, (key, v) in enumerate(dict.items()):
        print('Number ',i)
        #print(highest_answer(v,key))
        print('*'*20)

