import sys
from nltk import ne_chunk, word_tokenize, pos_tag
from nltk.tree import Tree
from nltk.tag import StanfordNERTagger
from question_type import QuestionType
from top_k_sentences import ArticleQuestions
from yes_no import yes_no_answer


import sys
from question_type import *
from top_k_sentences import *
from nltk import ne_chunk
from nltk.tree import Tree
from nltk.tag import StanfordNERTagger


class WHQ():
    def __init__(self, question, qtype, top_sentences):
        self.question = question
        self.qtype = qtype
        self.top_sentences = top_sentences
        self.ner = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz',
                                     'stanford-ner.jar')

    def find_answers(self):
        '''
            Find the correct phrase in a sentence's ner dictionary to answer
            the question of type 'type'
            Output:
            - answer: a string phrase to answer the question
        '''
        answer = "Sorry, I don't know"
        sentences_ner = self.sentence_ner(self.top_sentences)
        answer = self.answer_for_type(self.qtype, sentences_ner)
        return answer

    def sentence_ner(self, sentences):
        '''
            Generate a dictionary which maps each sentence to its NER dictionary
            which consists of (type, [phrases]) mappings.
            Input:
            - sentences: a list of top k sentences as strings
            Output:
            - sentences_ner: a dictionary of (sentence, {type: [phrases]})
        '''
        sentences_ner = {}
        for sentence in sentences:
            ner_dict = {}
            dependency_tree = ne_chunk(pos_tag(word_tokenize(sentence)))
            for node in dependency_tree:
                if type(node) == Tree:
                    phrase = ' '.join([token for token, _ in node.leaves()])
                    ner_dict[node.label()] = ner_dict.get(node.label(), []) + [phrase]
            sentences_ner[sentence] = ner_dict
        return sentences_ner

    def answer_for_type(self, type, sentences_ner):
        '''
            Find the correct phrase in a sentence's ner dictionary to answer
            the question of type 'type'
            Input:
            - type: the question's type as a string
            - sentences_ner: a dictionary mapping top k sentences to their NER
              dictionaries
            Output:
            - answer: a string phrase to answer the question
        '''
        answer = "Sorry, I don't know."
        for sentence, ner_dict in sentences_ner.items():
            for (ner, item) in ner_dict.items():
                if type == ner or (type == 'ORGANIZATION' and ner == 'GPE'):
                    answer = item[0]  # TODO: need to pick the right phrase!
        return answer


if __name__ == '__main__':
    article_file, questions_file = sys.argv[1:]

    # Process article and questions
    article_questions = ArticleQuestions(article_file, questions_file, 1)

    # Narrow down search range
    questions_top_sentences = article_questions.question_article_similarity()

    # Figure out the type of each question
    qt = QuestionType(article_questions.questions)

    answer = {}
    for question, qtype in qt.questions_type_dict.items():
        if qtype == 'YESNO':
            answer[question] = yes_no_answer(questions_top_sentences[question], question)
        else:
            whq = WHQ(question, qtype, questions_top_sentences[question])
            answer[question] = whq.find_answers()

    for i, (q, a) in enumerate(answer.items()):
        print('Question {}: {}'.format(i+1, q))
        print('Answer: {}\n'.format(a))
