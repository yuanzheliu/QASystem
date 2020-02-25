import sys
from nltk import sent_tokenize
from collections import Counter
from fuzzywuzzy import fuzz

class GetSentences():
    def __init__(self,article_file,question_file,top_k):
        self.article_file = article_file
        self.question_file = question_file
        self.top_k = top_k

    def read_article(self):
        with open(self.article_file,'r') as f:
            article = f.read()
        article_sentences = sent_tokenize(article)
        self.article_sentences = article_sentences
        return article_sentences

    def read_questions(self):
        questions = []
        with open(self.question_file, 'r') as f:
            for line in f:
                question = line.strip()
                questions.append(question)
        self.questions = questions
        return questions


    def question_article_similarity(self):
        dict = {}
        for question in self.questions:
            dic = {}
            for i, sentence in enumerate(self.article_sentences):
                dic[i] = fuzz.partial_ratio(question, str(sentence))
            k = Counter(dic)
            high = k.most_common(self.top_k)
            res = [self.article_sentences[item[0]] for item in high]
            dict[question] = res
        self.dict = dict
        return dict


if __name__ == '__main__':
    article_file, questions_file = sys.argv[1:]
    GS = GetSentences(article_file,questions_file,3)
    article_sentence = GS.read_article()
    questions = GS.read_questions()
    dict = GS.question_article_similarity()
    for i, (key, v) in enumerate(dict.items()):
        print("\nQuestion {}: {}".format(i+1, key))
        print("\nAnswers:")
        for i in range(len(v)):
            print("{}. {}".format(i+1, v[i]))