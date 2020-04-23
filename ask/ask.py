#!/usr/bin/env python3

from ask_sentence import ask_sentence
import sys
from nltk import sent_tokenize
import heapq

class model_ask(): 
    def __init__(self, sentences, num_questions):
        '''
        sentences: A list of strings. Each string is one sentence
        num_questions: Number of questions to generate
        '''
        self.num_questions = num_questions
        self.sentences = sentences

        self.who = []
        self.what = []
        self.when = []
        self.where = []
        self.why = []
        self.yesno = []
    
    def add_question(self, queue ,question): 
        if len(queue) >= self.num_questions: 
            heapq.heappushpop(queue, question)
        else: 
            heapq.heappush(queue,question)

    def generate_question(self):
        for s in self.sentences: 
            qs = ask_sentence(s)
            if len(qs) == 0: 
                continue 
            else: 
                for (score,question,answer,q_type) in qs:

                    if q_type == 'Who':
                        self.add_question(self.who, (score,question,answer))
                    elif q_type == 'What':
                        self.add_question(self.what, (score,question,answer))
                    elif q_type == 'When':
                        self.add_question(self.when, (score,question,answer))
                    elif q_type == 'Where':
                        self.add_question(self.where, (score,question,answer))
                    elif q_type == 'Why':
                        self.add_question(self.why, (score,question,answer))
                    elif q_type == 'yesno': 
                        self.add_question(self.yesno, (score,question,answer))

    def ask_question(self):
        result = []
        i = -1
        while len(result) < self.num_questions:
            if len(self.who) == 0 and len(self.what) == 0 and len(self.when) == 0 and len(self.why) == 0 and len(self.where) == 0 and len(self.yesno) == 0:
                break 
            i += 1
            if i % 6 == 0:
                if len(self.who) != 0:
                    result += [heapq.heappop(self.who)]
                    continue
            elif i % 6 == 1:
                if len(self.what) != 0:
                    result += [heapq.heappop(self.what)]
                    continue
            elif i % 6 == 2:
                if len(self.when) != 0:
                    result += [heapq.heappop(self.when)]
                    continue
            elif i % 6 == 3:
                if len(self.where) != 0:
                    result += [heapq.heappop(self.where)]
                    continue
            elif i % 6 == 4:
                if len(self.why) != 0:
                    result += [heapq.heappop(self.why)]
                    continue
            elif i % 6 == 5:
                if len(self.yesno) != 0:
                    result += [heapq.heappop(self.yesno)]
                    continue
        return result
                

if __name__ == "__main__":
    file_path, num_questions  = "", 0
    try:
        file_path = sys.argv[1]
        num_questions = int(sys.argv[2])
    except:
        print('usage: python ./ask.py <path to file> <number of questions>')
    
    model = None
    with open(file_path, 'r', encoding= 'utf-8') as f: 
        article = f.read()
        article_sentences = sent_tokenize(article)
        model = model_ask(article_sentences, num_questions)
    
    model.generate_question()
    result = model.ask_question()
    questions = [q[1] for q in result]
    answers = [q[2] for q in result]
    i = 1
    for q in questions:
        print("Q{} {}".format(i,q))
        i += 1

