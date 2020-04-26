from nltk.tag import StanfordNERTagger
from parse import extract_wh_answer


class WHQ():
    def __init__(self, question, qtype, top_sentences):
        self.question = question
        self.qtype = qtype
        self.top_sentences = top_sentences
        self.ner = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz',
                                     'stanford-ner.jar')
        #self.spacy_nlp = spacy.load('en_core_web_lg')

    def find_answers(self):
        '''
            Find the correct phrase in a sentence's ner dictionary to answer
            the question of type 'type'
            Output:
            - answer: a string phrase to answer the question
        '''
        answer = None
        for sentence in self.top_sentences:
            if self.qtype not in ['WHY', 'HOW']:
                answer = extract_wh_answer(self.question, self.qtype, sentence)
            else:  # how and why question return the whole sentence
                answer = self.top_sentences[0]
        if  answer == None or type(answer) != str or len(answer) == 0:
            return self.top_sentences[0]
        # return the most common answer
        return answer
