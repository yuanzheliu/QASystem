import spacy
from nltk.tag import StanfordNERTagger
from parse import extract_wh_answer


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
        for sentence in self.top_sentences:
            if self.qtype not in ['WHY', 'HOW']:
                answer = extract_wh_answer(self.question, self.qtype, sentence)
                answer_list.append(answer)
            else:  # how and why question return the whole sentence
                answer_list.append(self.top_sentences[0])
        most_common_answer = max(set(answer_list), key=answer_list.count)
        if type(most_common_answer) != str or len(most_common_answer) == 0:
            return self.top_sentences[0]
        # return the most common answer
        return most_common_answer
