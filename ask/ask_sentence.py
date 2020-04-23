import nltk
import spacy

init_score = 0
type_list = ['who', 'where', 'what', 'how', 'which', 'when', 'while', 'why']
nlp = spacy.load("en_core_web_lg")

def analyze_structure(s):
    parsed_text = nlp(s)

    subject = None
    subject_word = None
    verb = None

    # get token dependencies
    for text in parsed_text:
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
        return None, None, None, None

    score = 0
    for chunk in parsed_text.noun_chunks:
        score -= 1
        if  subject_word in chunk.text:
            subject =  chunk.text
            break

    return subject_word, subject, verb, score

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

    post_sentence = sentence[pos + len(subject) + 1:len(sentence)-1]
    question = "{} {}{}?".format(question, pre_sentence,post_sentence)
    return question


def pre_check_sentence(text):
    omit_list = ['?', '\n']
    for o in omit_list:
        if o in text:
            return False
    return True

'''
def remove_clause(text):
    doc = nlp(text)
    body = ""
    exist = False
    for token in doc:
        t = token.text
        t = t.lower()
        if t in type_list:
            exist = True
            break
        body += t
        body += " "

    if not exist:
        return text
    if len(body) > 0:
        body = body[0:len(body)-1]
        if body[len(body)-1] == ',':
            body = body[0:len(body)-1]
    pos_end = text.find(',', len(body))
    if pos_end != None:
        body += text[pos_end+2:len(text)]

    return body
'''

def ask_bool_question(text):
    if ',' in text:
        return None
    bool_text = ['is','are']
    doc = nlp(text)
    exist = False
    key = ""
    body = ""
    for token in doc:
        t = token.text
        t_lower = t.lower()
        if t_lower in bool_text:
            exist = True
            key = t
            break
        body += t
        body += ' '

    if not exist:
        return None

    __, subject, __, score = analyze_structure(text)

    if subject == None:
        return None

    if text.find(subject) != 0:
        score -=1

    if len(body) > 0:
        body = body[0:len(body)-1]

    pos = len(body) + len(key) + 1
    if pos != None:
        body += text[pos:len(text)]

    if len(body) == 0:
        return None


    key = key[0].upper()+ key[1:]

    # process the body
    body = body[0].lower() + body[1:]

    if body[len(body) - 1] == '.':
        body = body[0:len(body) - 1]

    question = "{} {}?".format(key, body)
    return (score, question,"", "yesno")

def ask_suject_question(text):
    subject_word, subject, verb, score = analyze_structure(text)
    if subject_word == None or subject == None:
        return None
    type = get_subject_type(subject_word)
    if type == None:
        return None
    question = construct_question(subject, verb, text, type)
    return (score, question, subject, type)

'''
def ask_time_question(text):
    question = ""
    answer = ""
    time_key_list = ['in', 'at']
    time_type_list = ['DATE', 'TIME']
    exist = False
    key = ""

    doc_text = nlp(text)
    body = ""
    for token in doc_text:
        t = token.text
        t_lower = t.lower()
        if t_lower in time_key_list:
            key = t
            exist = True
            break
        body += t
        body += ' '

    if not exist:
        return None

    if len(body) > 0:
        body = body[0:len(body)-1]

    pos_start = len(body)
    pos_end = text.find(',',pos_start+len(key)+1)
    if pos_end == -1:
        pos_end = text.find('.',pos_start+1)

    if pos_end != -1:
        if len(body) > 0 and body[len(body) - 1] == ',':
            body = body[0:len(body) - 1]

        body = body.strip()
        if len(body) == 0:
            body = text[pos_end+2:len(text)]
        else:
            body += text[pos_end+1:len(text)]

    time_str = text[pos_start+len(key)+1:pos_end]
    doc = nlp(time_str)
    is_time = False

    for token in doc:
        if token.ent_type_ in time_type_list:
            answer =time_str
            is_time = True

    if not is_time:
        return None

    question += 'When '

    # process the body
    body = body[0].lower() + body[1:]

    if body[len(body)-1] == '.' or ',':
        body = body[0:len(body)-1]

    body = body.strip()

    if body.split(' ')[0] in type_list:
        question += ','

    question += body
    question += '?'
    return (1, question, answer, 'when')
'''

def ask_sentence(text):
    res = []
    if not pre_check_sentence(text):
        return res
    q = ask_bool_question(text)
    if q != None:
        res.append(q)
    q = ask_suject_question(text)
    if q != None:
        res.append(q)
    return res

