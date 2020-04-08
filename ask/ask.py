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
        self.questions = [] # A list of tuple (score, 'Question', 'Answer'), score is the quality of a question. 

    def ask_questions(self):
        number = 1
        for s in self.sentences: 
            tmp = ask_sentence(s)
            if tmp != None: 
                if number > self.num_questions:
                    heapq.heappushpop(self.questions,tmp)
                else: 
                    heapq.heappush(self.questions,tmp)
                    number += 1
        return self.questions


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

    result = model.ask_questions()
    questions = [q[1] for q in result]
    answers = [q[2] for q in result]
    print('***************************')
    i = 1
    for q in questions:
        print("Q{} {}".format(i,q))
        i += 1    
    i = 1
    print('***************************')
    for a in answers:
        print("A{} {}".format(i,a))
        i += 1
    print('***************************')

