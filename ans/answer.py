#!/usr/bin/env python3

import sys
from question_type import *
from top_k_sentences import *
from nltk import ne_chunk
from nltk.tree import Tree
from nltk.tag import StanfordNERTagger


class WHQ():
    def __init__(self, questions_type_dict, questions_top_sentences):
        self.questions_type_dict = questions_type_dict
        self.questions_top_sentences = questions_top_sentences
        self.ner = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz',
                                     'stanford-ner.jar')

    def find_answers(self):
        '''
            Find the correct phrase in a sentence's ner dictionary to answer
            the question of type 'type'

            Output:
            - answer: a string phrase to answer the question
        '''
        result = {}
        for question, types in self.questions_type_dict.items():
            answer = "Sorry, I don't know"
            sentences_ner = self.sentence_ner(self.questions_top_sentences[question])

            for type in types:  # buggy: many types, one answer!
                answer = self.answer_for_type(type, sentences_ner)
            result[question] = answer
        return result

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
    if len(sys.argv) !=3:
        exit(-1)
    article_file, questions_file = sys.argv[1],sys.argv[2]
    # Process article and questions
    article_questions = ArticleQuestions(article_file, questions_file, 1)
    questions_top_sentences = article_questions.question_article_similarity()

    qt = QuestionType(article_questions.questions)

    whq = WHQ(qt.questions_type_dict, questions_top_sentences)
    ans = whq.find_answers()

    for i, (q, a) in enumerate(ans.items()):
        a =  "A{} {}\n".format(i, a)
        sys.stdout.buffer.write(a.encode('utf8'))
