import spacy
from nltk import ne_chunk, word_tokenize, pos_tag
from nltk.tree import Tree

nlp = spacy.load('en_core_web_lg')


def extract_wh_answer(question, qtype, sentence):
    sentence_parsed = nlp(sentence)
    sentence_chunked = ne_chunk(pos_tag(word_tokenize(sentence)))

    ner_dict = {}
    for node in sentence_chunked:
        if type(node) == Tree:
            phrase = ' '.join([token for token, _ in node.leaves()])
            ner_dict[node.label()] = ner_dict.get(node.label(), []) + [phrase]

    type_list = []

    if qtype == 'PERSON':
        for (ner, item) in ner_dict.items():
            if ner == 'PERSON':
                for i in item:
                    type_list.append(i)
        for ner_item in sentence_parsed.ents:
            if ner_item.label_ == 'PER' or ner_item.label_ == 'PERSON':
                if ner_item.text not in type_list:
                    type_list.append(ner_item.text)

    elif qtype == 'GPE':
        for (ner, item) in ner_dict.items():
            if ner == 'ORGANIZATION' or ner == 'LOCATION' or ner == 'GPE':
                for i in item:
                    type_list.append(i)
        for ner_item in sentence_parsed.ents:
            if ner_item.label_ == 'LOC' or ner_item.label_ == 'GPE' or ner_item.label_ == 'FAC':
                if ner_item.text not in type_list:
                    type_list.append(ner_item.text)

    elif qtype == 'TIME':
        for (ner, item) in ner_dict.items():
            if ner == 'TIME' or ner == 'DATE':
                for i in item:
                    type_list.append(i)
        for ner_item in sentence_parsed.ents:
            if ner_item.label_ == 'TIME' or ner_item.label_ == 'DATE':
                if ner_item.text not in type_list:
                    type_list.append(ner_item.text)

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
        if noun_chunk not in question_noun_chunk:
            if qtype == 'WHAT':
                return noun_chunk
            elif noun_chunk in type_list:
                return noun_chunk
    return sentence
