from nltk import sent_tokenize
from collections import Counter
from fuzzywuzzy import fuzz


class ArticleQuestions():
    def __init__(self, article_file, questions_file, k):
        self.article_sentences = self.read_article(article_file)
        self.questions = self.read_questions(questions_file)
        self.k = k

    def read_article(self, article_file):
        '''
            Read the article and split it into a list of sentences.
            Input:
            - article_file: file path to the article
            Output:
            - article_sentences: a list of article sentences as strings
        '''
        with open(article_file, 'r', encoding="utf-8") as f:
            article = f.read()
        article_sentences = sent_tokenize(article)
        return article_sentences

    def read_questions(self, questions_file):
        '''
            Read questions into a list of strings. Each string is a question.
            Input:
            - questions_file: file path to the questions
            Output:
            - questions: a list of strings with each string as a question
        '''
        questions = []
        with open(questions_file, 'r') as f:
            for line in f:
                question = line.strip()
                questions.append(question)
        questions = list(filter(None, questions))
        return questions

    def question_article_similarity(self):
        '''
            Partially match each sentence with each question and calculate
            similarity score. Take top k most similar sentences for each
            question.
            Output:
            - question_top_sentences: a dictionary mapping from a question to
              a list of k most similar sentences
        '''
        question_top_sentences = {}
        for question in self.questions:
            sentence_score = {}
            for i, sentence in enumerate(self.article_sentences):
                sentence_score[i] = fuzz.partial_ratio(question, sentence)
            top_k = Counter(sentence_score).most_common(self.k)
            top_sentences = [self.article_sentences[tuple[0]] for tuple in top_k]
            question_top_sentences[question] = top_sentences
        return question_top_sentences
