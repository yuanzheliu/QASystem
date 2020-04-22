'''
As of NLTK v3.3, users should avoid the Stanford NER or POS taggers from nltk.tag, 
and avoid Stanford tokenizer/segmenter from nltk.tokenize. 
They are currently deprecated and will be removed in due time.
'''
from nltk import word_tokenize
from nltk.parse import CoreNLPParser  # use this parser


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
        #parser = CoreNLPParser(url='http://localhost:9000')
        questions_type_dict = {}
        '''
        for question in questions:
            parse_question = list(parser.raw_parse(question))
            parse_tree = parse_question[0][0]
            questions_type_dict[question] = self.type(parse_tree,question.lower())
        '''
        for question in questions:
            questions_type_dict[question] = self.type(question.lower())
        return questions_type_dict
    
    def get_wh_type(self,tokens):
        question_type = 'WHAT'
        multi_answer = ['are','were','they','them','our','we']
        check_len = 5
        if len(tokens)<5:
            check_len = len(tokens)
        if 'who' == tokens[0] or 'whom' == tokens[0] or 'whose' == tokens[0]:
            question_type = 'PERSON'
        elif 'when' == tokens[0]:
            question_type = 'TIME'
        elif 'where' == tokens[0]:
            question_type = 'LOCATION'
        elif 'why' == tokens[0]:
            question_type = 'WHY'
        elif 'how' == tokens[0]:
            question_type = 'HOW'
        
        # multi-answers question
        for t in tokens[:check_len]:
            if t in multi_answer:
                question_type = 'MULTI'
                break
        return question_type
    '''  
    def type(self, parse_tree, question):
        question_type = 'unknown'
        yesno = ["is", "are", "was", "were", "does", "did", "have", "has",
                 "had", "can", "could", "will", "would"]
        tokens = word_tokenize(question)

        if parse_tree._label == 'SBARQ' or question.startswith('wh') or question.startswith('ho'):
            question_type = self.get_wh_type(parse_tree,tokens)
        elif parse_tree._label == 'SQ' or tokens[0] in yesno:
            question_type = 'YESNO'
        return question_type
    '''
    def type(self,question):
        question_type = 'WHAT'
        tokens = word_tokenize(question)
        yesno = ["is", "are", "was", "were", "does", "did", "have", "has",
                 "had", "can", "could", "will", "would"]
        if question.startswith('wh') or question.startswith('ho'):
            question_type = self.get_wh_type(tokens)
        elif tokens[0] in yesno:
            question_type ='YESNO'
        return question_type
