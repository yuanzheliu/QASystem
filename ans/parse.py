import spacy
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

nlp = spacy.load('en_core_web_sm')


def get_who_answer(question, sentence):
    answer = None
    question_parsed = nlp(question)
    sentence_parsed = nlp(sentence)
    sentence_chunked = ne_chunk(pos_tag(word_tokenize(sentence)))
    dictionary = dict(pos_tag(word_tokenize(sentence)))
    root_verb = ''
    for token in question_parsed:
        if token.dep_ == 'ROOT':
            root_verb = token.text

    for token in sentence_parsed:
        children = [child.text for child in token.children]
        if root_verb in children:
            for child in token.children:
                if child.text in dictionary and dictionary[child.text] == 'NNP':
                    return child.text
    if answer is None:
        for node in sentence_chunked:
            if type(node) == Tree and node.label() == 'PERSON':
                phrase = ' '.join([token for token, _ in node.leaves()])
                if phrase not in question:
                    return phrase
    return sentence


def get_where_answer(question, sentence):
    sentence_parsed = ne_chunk(pos_tag(word_tokenize(sentence)))
    for node in sentence_parsed:
        if type(node) == Tree and node.label() == 'GPE':
            phrase = ' '.join([token for token, _ in node.leaves()])
            if phrase not in question:
                return phrase
    return sentence


def get_when_answer(question, sentence):
    # for token in sentence_parsed:
    #     print(token.text, token.tag_, token.head.text, token.dep_)
    sentence_parsed = nlp(sentence)
    for token in sentence_parsed:
        if token.tag_ == 'CD'and token.text not in question:
            if token.dep_ == 'nummod':
                return token.text + ' ' + token.head.text
            return token.text
    return sentence
