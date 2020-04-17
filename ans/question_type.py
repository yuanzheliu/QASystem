from nltk import word_tokenize, pos_tag


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
        questions_type_dict = {}
        for question in questions:
            tokens = word_tokenize(question)
            token_pos = pos_tag(tokens)  # list of (token, pos)
            questions_type_dict[question] = self.type(token_pos)
        return questions_type_dict

    def type(self, token_pos):
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
        # be careful for whom->NNP and whose->JJ questions!!
        poses = ['WP', 'WP$', 'WRB', 'WDT']
        person = ['who', 'whom', 'whose']
        location = ['where']
        time = ['when']
        reason = ['why']
        object = ['what', 'which']
        way = ['how']
        yesno = ["is", "are", "was", "were", "does", "did", "have", "has",
                 "had", "can", "could", "will", "would"]

        type = 'unknown'
        for i, (token, pos) in enumerate(token_pos):
            word = token.lower()
            if i == 0 and word in yesno:
                type = 'YESNO'
            elif pos in poses:
                if word in person:
                    type = 'PERSON'
                elif word in location:
                    type = 'GPE'
                elif word in time:
                    type = 'TIME'
                elif word in reason:
                    type = 'REASON'
                elif word in object:
                    type = 'ORGANIZATION'
                elif word in way:
                    type = 'WAY'
        return type
