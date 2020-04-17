import sys
import nltk.data
import nltk
from nltk import word_tokenize, pos_tag
from top_k_sentences import ArticleQuestions


def yes_no_answer(top_sentences, question):
    prev = "No"
    question = pos_tag(word_tokenize(question.lower()))
    answer = "No"
    keyword = ""
    for (token, pos) in question:
        if pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS':
            keyword = token.lower()
    for sentence in top_sentences:
        if answer == "Yes":
            return answer
        sentence_words = word_tokenize(sentence.lower())
        if keyword in sentence_words:
            answer = "Yes"
            for (token, pos) in question:
                if answer == 'No':
                    break
                if pos != '.' and token.lower() not in sentence_words and pos != 'DT' and token != 'do' and token != 'does':
                    answer = 'No'
                    if pos[0] == 'V':
                        tempword = nltk.stem.wordnet.WordNetLemmatizer().lemmatize(token, 'v')
                        for (w, p) in pos_tag(sentence_words):
                            if p[0] == 'V':
                                tempword2 = nltk.stem.wordnet.WordNetLemmatizer().lemmatize(w, 'v')
                                if tempword == tempword2:
                                    answer = 'Yes'
                    elif token in top_sentences[0]:
                        answer = "Yes"
                if prev == "Yes":
                    if token == "no" or token == "not":
                        answer = "No"
                if pos[0] == 'V':
                    prev = "Yes"
                else:
                    prev = "No"

    return answer


if __name__ == "__main__":
    article_file, questions_file = sys.argv[1:]

    # Process article and questions
    article_questions = ArticleQuestions(article_file, questions_file, 1)

    # Narrow down search range
    questions_top_sentences = article_questions.question_article_similarity()

    ans = {}
    for question, top_sentences in questions_top_sentences.items():
        ans[question] = yes_no_answer(questions_top_sentences[question], question)

    for i, (q, a) in enumerate(ans.items()):
        print('Question {}: {}'.format(i+1, q))
        print('Answer: {}\n'.format(a))
