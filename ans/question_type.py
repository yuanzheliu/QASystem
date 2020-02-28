from nltk import word_tokenize, pos_tag
from top_k_sentences import *


class QuestionType():
    def __init__(self, questions):
        self.questions_type_dict = self.q_type(questions)

    def q_type(self, questions):
        '''
            Tokenize and part-of-speech tagging each question in questions,
            find the wh-word in each question, and return the {question:
            [wh-words]} dictionary

            Input:
            - questions: a list of strings with each string as a question

            Output:
            - questions_wh_dict
        '''
        questions_wh_dict = {}
        for question in questions:
            token = word_tokenize(question)
            token_pos = pos_tag(token)
            questions_wh_dict[question] = self.wh_type(token_pos)
        return questions_wh_dict

    def wh_type(self, q_pos):
        '''
            Extract wh-words from a tokenized and tagged question, assign types
            ('PERSON', 'GPE', 'TIME', 'REASON', 'ORGANIZATION', 'WAY', 'unknown')
            to each wh-word.

            Input:
            - q_pos: a tokenized and tagged sentence as a list of (token, tag)
              tuples

            Output:
            - wh_types: a list of types of wh-words
        '''
        # be careful for whom->NNP and whose->JJ questions!!
        poses = ['WP', 'WP$', 'WRB', 'WDT']
        person = ['who', 'whom', 'whose']
        location = ['where']
        time = ['when']
        reason = ['why']
        object = ['what', 'which']
        way = ['how']

        wh_types = []
        for token, pos in q_pos:
            if pos in poses:
                wh = token.lower()
                if wh in person:
                    wh_types.append('PERSON')
                elif wh in location:
                    wh_types.append('GPE')
                elif wh in time:
                    wh_types.append('TIME')
                elif wh in reason:
                    wh_types.append('REASON')
                elif wh in object:
                    wh_types.append('ORGANIZATION')
                elif wh in way:
                    wh_types.append('WAY')
                else:
                    wh_types.append('unknown')
        return wh_types
