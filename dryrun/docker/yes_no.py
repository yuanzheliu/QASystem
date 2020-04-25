from nltk import word_tokenize, pos_tag


def yes_no_answer(top_sentences, question):
    question_parsed = pos_tag(word_tokenize(question))
    keywords = set()
    for (token, pos) in question_parsed:
        if pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS':
            keywords.add(token.lower())
    yes = True
    for sentence in top_sentences:
        for keyword in keywords:
            if keyword not in sentence.lower():
                yes = False
                break
    if "'t" in question[0]:
        yes = not yes
    return "Yes" if yes else "No"
