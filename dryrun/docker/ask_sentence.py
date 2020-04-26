import nltk
import spacy

init_score = 0
type_list = ['who', 'where', 'what', 'how', 'which', 'when', 'while', 'why']
nlp = spacy.load("en_core_web_lg")


def analyze_structure(s):
    verb_type_list = ['VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
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
            if verb is not None:
                break
        elif text.dep_ == "ROOT":
            verb = text.orth_
            if subject_word is not None:
                break

    if verb is not None:
        type = nltk.pos_tag(nltk.word_tokenize(verb))[0][1]
        if type not in verb_type_list:
            verb = None

    if subject_word is None:
        return None, None, None, None

    score = 0
    for chunk in parsed_text.noun_chunks:
        score -= 1
        if subject_word in chunk.text:
            subject = chunk.text
            break
    return subject_word, subject, verb, score


def get_subject_type(subject):
    question = ''
    t = nltk.word_tokenize(subject)
    doc = nlp(subject)
    if nltk.pos_tag(t)[0][1] in {"NN", "NNS", "NNP", "NNPS"}:
        if doc[0].ent_type_ == "PERSON":
            question = "Who"
        elif doc[0].ent_type_ in {"GPE", "LOC"}:
            question = "Where"
        else:
            question = "What"

    elif nltk.pos_tag(t)[0][1] == 'PRP':
        if t[0] in {'He', 'She', 'I', 'You'}:
            question = "Who"
        elif t[0] == 'It':
            question = 'What'
        else:
            return None  # TODO: "They"?
    else:
        return None
    return question


def remove_clause_helper(text):
    doc = nlp(text)
    body = ""
    exist = False
    for token in doc:
        t = token.text
        t = t.lower()
        if t in type_list:
            exist = True
            break
        if len(t) == 1 and len(body) > 0:
            body = body[0:len(body)-1]
        body += t
        if len(t) > 1:
            body += " "

    if not exist:
        return False, text

    body = body.strip()

    if len(body) > 0:
        if body[len(body)-1] == ',':
            body = body[0:len(body)-1]
    pos_end = text.find(',', len(body))
    if pos_end != -1:
        body += text[pos_end+1:len(text)]
    return True, body


def remove_clause(text):
    exist, text = remove_clause_helper(text)
    while exist:
        exist, text = remove_clause_helper(text)
    return text


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
    question = "{} {}{}?".format(question, pre_sentence, post_sentence)
    return question


def pre_check_sentence(text):
    omit_list = ['?', '\n']
    for o in omit_list:
        if o in text:
            return False
    return True


def ask_bool_question(text):
    omit_list = ['and', 'or', 'but', ',']
    for o in omit_list:
        if o in text:
            return None
    bool_text = ['is', 'are', 'was', 'were']
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

    if subject is None:
        return None

    if text.find(subject) != 0:
        score -= 1

    if len(body) > 0:
        body = body[0:len(body)-1]

    pos = len(body) + len(key) + 1
    if pos is not None:
        body += text[pos:len(text)]

    if len(body) == 0:
        return None


    key = key[0].upper() + key[1:]

    # process the body
    body = body[0].lower() + body[1:]

    if body[len(body) - 1] == '.':
        body = body[0:len(body) - 1]

    question = "{} {}?".format(key, body)
    return (score, question, "", "yesno")


def ask_suject_question(text):
    subject_word, subject, verb, score = analyze_structure(text)
    if verb is None:
        return None
    if subject_word is None or subject is None:
        return None
    type = get_subject_type(subject_word)
    if type is None:
        return None
    question = construct_question(subject, verb, text, type)
    return (score, question, subject, type)


def ask_sentence(text):
    res = []
    if not pre_check_sentence(text):
        return res
    text = remove_clause(text)
    q = ask_bool_question(text)
    if q is not None:
        res.append(q)
    q = ask_suject_question(text)
    if q is not None:
        res.append(q)
    return res
