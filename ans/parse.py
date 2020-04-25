import spacy

nlp = spacy.load('en_core_web_sm')


def extract_wh_answer(question, qtype, sentence):
    sentence_parsed = nlp(sentence)
    if qtype == 'TIME':
        for token in sentence_parsed:
            if token.tag_ == 'CD'and token.text not in question:
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
        if noun_chunk not in question_noun_chunk:
            return noun_chunk
    return sentence
