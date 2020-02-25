from nltk import word_tokenize, pos_tag
from TopKsentence import *

class QuestionType():
    def __init__(self,questions):
        self.questions = questions

    def wh_type(self,q_pos):
        list = []
        # be careful for whom->NNP and whose->JJ questions!!
        if q_pos[0][0].lower() =='whom':
            list.append('whom')
        elif q_pos[0][0].lower() =='whose':
            list.append('whose')
        wh_set ={'who','what','where','why','when','which','how'}
        pos_set={'WP','WRB','WDT'}
        for pos in q_pos:
            if pos[1] in pos_set:
                wh = pos[0].lower()
                if wh not in wh_set:
                    list.append('None')
                else:
                    list.append(wh)
        return list

    def q_type(self):
        dic_type = {}
        for q in self.questions:
            q_token = word_tokenize(q)
            q_pos = pos_tag(q_token)
            dic_type[q] = self.wh_type(q_pos)
        return dic_type


if __name__ == '__main__':
    article_file, questions_file = sys.argv[1:]
    GS = GetSentences(article_file, questions_file, 3)
    article_sentence = GS.read_article()
    questions = GS.read_questions()
    QT = QuestionType(questions)
    print(QT.q_type())
