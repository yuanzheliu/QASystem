import nltk
import spacy

init_score = 0
type_list = ['who', 'where', 'what', 'how', 'which', 'that', 'when']
nlp = spacy.load("en_core_web_lg")

'''
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
'''


def analyze_structure(s):
    parsed_text = nlp(s)

    subject = None
    subject_word = None
    verb = None

    # get token dependencies
    for text in parsed_text:
        # subject would be
        #print(str(text) + ',' + str(text.dep_))
        if text.dep_ == "nsubj":
            if text.orth_ in type_list:
                continue
            subject_word = text.orth_
            if verb != None:
                break
        elif text.dep_ == "ROOT":
            verb = text.orth_
            if subject_word != None:
                break

    if subject_word == None:
        return None, None, None

    for chunk in parsed_text.noun_chunks:
        if  subject_word in chunk.text:
            subject =  chunk.text
            break

    return subject_word, subject, verb

def get_subject_type(subject):
    question = ''
    answer = ''
    t = nltk.word_tokenize(subject)
    doc = nlp(subject)
    if nltk.pos_tag(t)[0][1] in {"NN", "NNS", "NNP", "NNPS"}:
        if doc[0].ent_type_ == "PERSON":
            question = "Who"
        elif doc[0].ent_type_ in {"GPE", "LOC"}:
            question = "Where"
        else:
            question = "What"
        answer = t[0]

    elif nltk.pos_tag(t)[0][1] == 'PRP':
        answer = t[0]
        if t[0] in {'He', 'She', 'I', 'You'}:
            question = "Who"
        elif t[0] == 'It':
            question = 'What'
        else:
            return None  # TODO: "They"?

    else:
        return None
    return question

def construct_question(subject, verb, sentence, type):
    question = type
    pos = sentence.find(subject)
    pre_sentence = sentence[0:pos]

    if len(pre_sentence) > 0:
        t = nltk.word_tokenize(pre_sentence)
        if nltk.pos_tag(t)[0][1] not in {"NN", "NNS", "NNP", "NNPS"}:
            pre_sentence = pre_sentence.lower()

        if ',' in pre_sentence:
            question += ','

    post_sentence = sentence[pos + len(subject) + 1:len(sentence) - 1]
    question = "{} {}{}?".format(question, pre_sentence,post_sentence)
    return question


def pre_check_sentence(text):
    omit_list = ['?', '\n']
    for o in omit_list:
        if o in text:
            return False
    return True

def ask_suject_question(text):
    subject_word, subject, verb = analyze_structure(text)
    if subject_word == None or subject == None:
        return None
    type = get_subject_type(subject_word)
    if type == None:
        return None
    question = construct_question(subject, verb, text, type)
    return (1, question, subject, type)

def ask_time_question(text):
    time_list = ['in', 'at']
    text = text.lower()
    exist = False
    key = None
    for t in time_list:
        if t in text:
            exist = True
            key = t
            break
    if not exist:
        return None

    pos = text.find()
def ask_sentence(text):
    if not pre_check_sentence(text):
        return None
    res = ask_suject_question(text)
    if res != None:
        return res

