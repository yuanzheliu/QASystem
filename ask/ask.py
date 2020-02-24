import nltk
import spacy
nlp = spacy.load("en_core_web_sm")





def ask_sentence(text):
    result = ''
    t = nltk.word_tokenize(text)
    doc = nlp(text)
    if nltk.pos_tag(t)[0][1] in {"NN", "NNS", "NNP", "NNPS"}: 
                if doc[0].ent_type_ == "PERSON": 
                    result = "Who "
                elif doc[0].ent_type_ in {"GPE", "LOC"}: 
                    result = "Where "
                else: 
                    result = "What "
                result += " ".join(t[1:-1]) + "?"
    elif nltk.pos_tag(t)[0][1] == 'PRP': 
        if t[0] in {'He', 'She', 'I', 'You'}:   #TODO: "They"?
            result = "Who "
        elif t[0] == 'It': 
            result = 'What '
        result += " ".join(t[1:-1]) + "?"
    else:
        print(nltk.pos_tag(t)[0][1])
    return result


text = "Pittsburgh has no nCov."
print(text, "============>",ask_sentence(text))
text = "Thomas is writing code."
print(text, "============>",ask_sentence(text))
text = "He is writing code."
print(text, "============>",ask_sentence(text))
text = "It has no effect on the run."
print(text, "============>",ask_sentence(text))
text = "CNN performs better than MLP on image classification."
print(text, "============>",ask_sentence(text))
text = "Apple tasts better."
print(text, "============>",ask_sentence(text))
text = "Apples are better than peaches."
print(text, "============>",ask_sentence(text))
# text = "The house is on the run."   #TODO
# print(text, "============>",ask_sentence(text))
# doc = nlp(text)
# print(nltk.pos_tag(nltk.word_tokenize(text)))
# for token in doc: 
#     print(token.text, token.ent_type_)