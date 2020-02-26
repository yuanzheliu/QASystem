from nltk import word_tokenize, pos_tag,ne_chunk
from nltk.tag import StanfordNERTagger
from TopKsentence import *
from Qtype import *
from nltk.tree import Tree as Tree


class WHQ():
    def __init__(self,search_q,q_s_pair):
        self.search_q = search_q
        self.q_s_pair = q_s_pair
        self.ner = StanfordNERTagger(
            'english.muc.7class.distsim.crf.ser.gz',
            'stanford-ner.jar')
    '''
    reference: https://stackoverflow.com/questions/24398536/named-entity-recognition-with-regular-expression-nltk
    '''
    def get_continuous_chunks(self,text):
        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        continuous_chunk = []
        current_chunk = []
        for i in chunked:
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk and len(named_entity)!=0:
                    continuous_chunk.append(named_entity)
                    current_chunk = []
            else:
                continue
        if continuous_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk and len(named_entity)!=0:
                continuous_chunk.append(named_entity)

        return continuous_chunk

    '''
    return the NER for each sentence
    '''
    def sentence_ner(self,sentences):
        st_ner = {}
        for st in sentences:
            ner={}
            st_chunk = ne_chunk(pos_tag(word_tokenize(st)))
            for i in st_chunk:
                if type(i) == Tree:
                    current_chunk = (' '.join([token for token, pos in i.leaves()]))
                    if i.label() in ner:
                        ner[i.label()].append(current_chunk)
                    else:
                        ner[i.label()] = [current_chunk]
            st_ner[st] = ner
        return st_ner


    def ans_each_type(self,type,st_ner):
        ans = 'Sorry, I don\'t know'
        for j, (st, ner_list) in enumerate(st_ner.items()):
            for (ner, item) in ner_list.items():
                if type =='PERSON' and ner =='PERSON':
                    ans = item[0]
                elif type == 'ORGANIZATION' and (ner =='ORGANIZATION' or ner =='GPE'):
                    ans = item[0]
        return ans

    def checkType(self):
        '''
        :search_q: question, type
        :q_s_pair: question->sentences_pair

        :return: answer for each question
        '''
        res = {}
        for i,(key,v) in enumerate(self.search_q.items()):
            ans = 'Sorry, I don\'t know'
            st_ner = self.sentence_ner(self.q_s_pair[key])
            for type in v:
                ans = self.ans_each_type(type,st_ner)
            res[key] = ans
        return res

if __name__ == '__main__':
    article_file, questions_file = sys.argv[1:]
    GS = GetSentences(article_file, questions_file, 1)
    article_sentence = GS.read_article()
    questions = GS.read_questions()
    dic = GS.question_article_similarity()
    QT = QuestionType(questions)
    dic_type = QT.q_type()
    search_word = QT.search_word(dic_type)
    whq = WHQ(search_word,dic)
    ans = whq.checkType()
    for i,(q,a) in enumerate(ans.items()):
        print('Question: {0}'.format(q))
        print('Answer: {0}'.format(a))
