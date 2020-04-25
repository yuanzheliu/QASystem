import spacy
from nltk import ne_chunk, word_tokenize, pos_tag
from nltk.tree import Tree

nlp = spacy.load('en_core_web_sm')


def extract_wh_answer(question, qtype, sentence):
    sentence_parsed = nlp(sentence)
    sentence_chunked = ne_chunk(pos_tag(word_tokenize(sentence)))

    type_list = set()
    for node in sentence_chunked:
        if type(node) == Tree and node.label() == qtype:
            phrase = ' '.join([token for token, _ in node.leaves()])
            type_list.add(phrase)

    if qtype == 'TIME':
        for token in sentence_parsed:
            if token.tag_ == 'CD' and token.text not in question:
                if token.dep_ == 'nummod':
                    return token.text + ' ' + token.head.text
                return token.text
        return sentence

    question_parsed = nlp(question)
    question_noun_chunk = []
    sentence_noun_chunk = []
    for chunk in question_parsed.noun_chunks:
        question_noun_chunk.append(chunk.text)
    for chunk in sentence_parsed.noun_chunks:
        sentence_noun_chunk.append(chunk.text)

    if qtype == 'PERSON':
        sentence_noun_chunk = sentence_noun_chunk[::-1]
    for noun_chunk in sentence_noun_chunk:
        if noun_chunk not in question_noun_chunk and noun_chunk in type_list:
            return noun_chunk
    return sentence
