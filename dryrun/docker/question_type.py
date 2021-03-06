from nltk import word_tokenize


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
        questions_type_dict = {}
        for question in questions:
            questions_type_dict[question] = self.type(question.lower())
        return questions_type_dict

    def get_wh_type(self, tokens):
        question_type = 'HOW'  # 'how' question will return the whole sentence
        # multi_answer = ['are','were','they','them','our','we']

        if 'who' == tokens[0] or 'whom' == tokens[0] or 'whose' == tokens[0]:
            question_type = 'PERSON'
        elif 'when' == tokens[0]:
            question_type = 'TIME'
        elif 'where' == tokens[0]:
            question_type = 'GPE'
        elif 'what' == tokens[0]:
            question_type = 'WHAT'
        elif 'why' == tokens[0]:
            question_type = 'WHY'
        elif 'how' == tokens[0]:
            question_type = 'HOW'
        return question_type

    def type(self, question):
        question_type = 'HOW'  # default question type to return the whole sentence
        tokens = word_tokenize(question)
        yesno = ["is", "are", "was", "were", "does", "did", "have", "has",
                 "had", "can", "could", "will", "would"]
        if question.startswith('wh') or question.startswith('ho'):
            question_type = self.get_wh_type(tokens)
        elif tokens[0] in yesno:
            question_type = 'YESNO'
        return question_type
