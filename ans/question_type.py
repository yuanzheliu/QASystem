'''
As of NLTK v3.3, users should avoid the Stanford NER or POS taggers from nltk.tag, 
and avoid Stanford tokenizer/segmenter from nltk.tokenize. 
They are currently deprecated and will be removed in due time.
'''
from nltk import word_tokenize
from nltk.parse import CoreNLPParser # use this parser

class QuestionType():
    def __init__(self, questions):
        self.questions_type_dict = self.question_type(questions)

    def question_type(self, questions):
        '''
            Tokenize and part-of-speech tagging each question in questions,
            find the indicator word in each question, and return the {question:
            type} dictionary

            Input:
            - questions: a list of strings with each string as a question

            Output:
            - questions_type_dict: a dictionary of {question: type}
        '''
        # Lexical Parser
        parser = CoreNLPParser(url='http://localhost:9000')
        questions_type_dict = {}
        for question in questions:
            parse_question = list(parser.raw_parse(question))
            parse_tree = parse_question[0][0]
            questions_type_dict[question] = self.type(parse_tree,question.lower())
        return questions_type_dict
    
    def get_wh_type(self,parse_tree,question):
        return 'PERSON'

    def type(self, parse_tree, question):
        '''
            Extract the indicator words from a tokenized and tagged question,
            assign, type ('PERSON', 'GPE', 'TIME', 'REASON', 'ORGANIZATION',
            'WAY', 'unknown') to it.

            Input:
            - token_pos: a tokenized and tagged sentence as a list of (token,
              tag) tuples

            Output:
            - type: type of indicator word
        '''
        type = 'unknown'
        yesno = ["is", "are", "was", "were", "does", "did", "have", "has",
                 "had", "can", "could", "will", "would"]
        tokens = word_tokenize(question)

        if parse_tree._label == 'SBARQ' or question.startswith('wh') or question.startswith('ho'):
            type = self.get_wh_type(parse_tree,question)
        elif parse_tree._label == 'SQ' or tokens[0] in yesno:
            type = 'YESNO'
        return type