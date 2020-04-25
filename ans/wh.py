from collections import Counter
from itertools import groupby

import spacy
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tag import StanfordNERTagger
from nltk.tree import Tree


class WHQ():
    def __init__(self, question, qtype, top_sentences):
        self.question = question
        self.qtype = qtype
        self.top_sentences = top_sentences
        self.ner = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz',
                                     'stanford-ner.jar')
        self.spacy_nlp = spacy.load('en_core_web_lg')


    def who_question(self,sentences_ner,sentences_tag,sp_ner,sentences):
        answer_list ={}
        for sentence in sentences:
            answer_list[sentence] = []
            tag_list = sentences_tag[sentence]
            for (tag,chunk) in tag_list.items():
                if tag == 'PERSON':
                    answer_list[sentence].append(chunk)
            ner_dict = sentences_ner[sentence]
            for (ner, item) in ner_dict.items():
                if ner == 'PERSON':
                    for i in item:
                        answer_list[sentence].append(i)
            sp_st_ner = sp_ner[sentence]
            for ner_item in sp_st_ner.ents:
                if ner_item.label_ == 'PER' or ner_item.label_ == 'PERSON':
                    answer_list[sentence].append(ner_item.text)
        return answer_list
    
    def where_question(self,sentences_ner,sentences_tag,sp_ner,sentences):
        answer_list ={}
        for sentence in sentences:
            answer_list[sentence] = []
            tag_list = sentences_tag[sentence]
            for (tag,chunk) in tag_list.items():
                if tag == 'LOCATION' or tag =='CITY' or tag =='GPE':
                    answer_list[sentence].append(chunk)
            ner_dict = sentences_ner[sentence]
            for (ner, item) in ner_dict.items():
                if ner == 'ORGANIZATION' or ner =='LOCATION' or ner == 'GPE':
                    for i in item:
                        answer_list[sentence].append(i)
            sp_st_ner = sp_ner[sentence]
            for ner_item in sp_st_ner.ents:
                if ner_item.label_ == 'LOC' or ner_item.label_ =='GPE' or ner_item.label_ =='FAC':
                    answer_list[sentence].append(ner_item.text)
        return answer_list
    
    def when_question(self,sentences_ner,sentences_tag,sp_ner,sentences):
        answer_list ={}
        for sentence in sentences:
            answer_list[sentence] = []
            tag_list = sentences_tag[sentence]
            for (tag,chunk) in tag_list.items():
                if tag == 'TIME' or tag =='DATE':
                    answer_list[sentence].append(chunk)
            ner_dict = sentences_ner[sentence]
            for (ner, item) in ner_dict.items():
                if ner == 'TIME' or ner =='DATE':
                    for i in item:
                        answer_list[sentence].append(i)
            sp_st_ner = sp_ner[sentence]
            for ner_item in sp_st_ner.ents:
                if ner_item.label_ == 'TIME' or ner_item.label_ =='DATE':
                    answer_list[sentence].append(ner_item.text)
        return answer_list
            
    def find_answers(self):
        '''
            Find the correct phrase in a sentence's ner dictionary to answer
            the question of type 'type'
            Output:
            - answer: a string phrase to answer the question
        '''
        default_answer = "Sorry, I don't know."
        sentences_ner = self.sentence_ner(self.top_sentences)
        sentences_tag = self.sentence_tag(self.top_sentences)
        sp_ner = self.spacy_ner(self.top_sentences)
        answer_list = {}
        if self.qtype == 'PERSON':
            answer_list = self.who_question(sentences_ner,sentences_tag,sp_ner,self.top_sentences)
        elif self.qtype =='LOCATION':
            answer_list = self.where_question(sentences_ner,sentences_tag,sp_ner,self.top_sentences)
        elif self.qtype =='TIME':
            answer_list = self.when_question(sentences_ner,sentences_tag,sp_ner,self.top_sentences)
        total_list=[]
        for sentence, answer in answer_list.items():
            total_list.extend(answer)
        if len(total_list) ==0:
            return self.top_sentences[0]
        occurence_count = Counter(total_list)
        most_common_answer = occurence_count.most_common(1)[0][0]
        if type(most_common_answer)!=str or len(most_common_answer) ==0:
            return self.top_sentences[0]
        return most_common_answer

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
    
    def sentence_tag(self,sentences):
        sentence_tag = {}
        for sentence in sentences:
            tag_dict = {}
            tokens = word_tokenize(sentence)
            tagged_words = self.ner.tag(tokens)
            for tag, chunk in groupby(tagged_words, lambda x: x[1]):
                tag_dict[tag] = " ".join(w for w, t in chunk)
            sentence_tag[sentence] = tag_dict
        return sentence_tag

    def spacy_ner(self,sentences):
        sp_ner = {}
        for sentence in sentences:
            sp_ner[sentence] = self.spacy_nlp(sentence)
        return sp_ner
