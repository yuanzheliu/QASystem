import nltk
import spacy
nlp = spacy.load("en_core_web_sm")



def ask_sentence(text):
    question = ''
    answer = ''
    t = nltk.word_tokenize(text)
    doc = nlp(text)
    if nltk.pos_tag(t)[0][1] in {"NN", "NNS", "NNP", "NNPS"}: 
        if doc[0].ent_type_ == "PERSON": 
            question = "Who "
        elif doc[0].ent_type_ in {"GPE", "LOC"}: 
            question = "Where "
        else: 
            question = "What "
        answer = t[0]
        question += " ".join(t[1:-1]) + "?"
    elif nltk.pos_tag(t)[0][1] == 'PRP': 
        answer = t[0]
        if t[0] in {'He', 'She', 'I', 'You'}:   
            question = "Who "
        elif t[0] == 'It': 
            question = 'What '
        else: 
            return None #TODO: "They"?
        question += " ".join(t[1:-1]) + "?"
    else:
        return None
    return (1, question, answer)

