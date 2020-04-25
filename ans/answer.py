import sys

from question_type import QuestionType
from top_k_sentences import ArticleQuestions
from wh import WHQ
from yes_no import yes_no_answer

if __name__ == '__main__':
    article_file, questions_file = sys.argv[1:]

    # Process article and questions
    article_questions = ArticleQuestions(article_file, questions_file, 1)

    # Narrow down search range
    questions_top_sentences = article_questions.question_article_similarity()

    # Figure out the type of each question
    qt = QuestionType(article_questions.questions)

    answer = {}
    for question, qtype in qt.questions_type_dict.items():
        if qtype == 'YESNO':
            answer[question] = yes_no_answer(questions_top_sentences[question], question)
        else:
            whq = WHQ(question, qtype, questions_top_sentences[question])
            answer[question] = whq.find_answers()

    for i, (q, a) in enumerate(answer.items()):
        a = "A{} {}\n".format(i+1, a)
        sys.stdout.buffer.write(a.encode('utf8'))
