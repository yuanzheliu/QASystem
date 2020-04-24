import spacy
from nltk.tag import StanfordNERTagger
from collections import Counter
from parse import get_who_answer, get_where_answer, get_when_answer, get_what_answer


class WHQ():
    def __init__(self, question, qtype, top_sentences):
        self.question = question
        self.qtype = qtype
        self.top_sentences = top_sentences
        self.ner = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz',
                                     'stanford-ner.jar')
        self.spacy_nlp = spacy.load('en_core_web_lg')

    def find_answers(self):
        '''
            Find the correct phrase in a sentence's ner dictionary to answer
            the question of type 'type'
            Output:
            - answer: a string phrase to answer the question
        '''
        answer_list = []
        if self.qtype == 'PERSON':
            for sentence in self.top_sentences:
                answer = get_who_answer(self.question, sentence)
                answer_list.append(answer)
        elif self.qtype == 'LOCATION':
            for sentence in self.top_sentences:
                answer = get_where_answer(self.question, sentence)
                answer_list.append(answer)
        elif self.qtype == 'TIME':
            for sentence in self.top_sentences:
                answer = get_when_answer(self.question, sentence)
                answer_list.append(answer)
        elif self.qtype == 'WHAT':
            for sentence in self.top_sentences:
                answer = get_what_answer(self.question, sentence)
                answer_list.append(answer)
        # how and why question return the whole sentence
        if len(answer_list) == 0:
            return self.top_sentences[0]
        occurence_count = Counter(answer_list)
        most_common_answer = occurence_count.most_common(1)[0][0]
        # if there is no answer found or answer in the wrong format, return whole sentence
        if type(most_common_answer) != str or len(most_common_answer) == 0:
            return self.top_sentences[0]
        # return the most common answer
        return most_common_answer
