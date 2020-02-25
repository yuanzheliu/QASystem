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

    def person(self,question,sentences):
        ans = 'Sorry, I don\'t know'
        q_chunk = ne_chunk(pos_tag(word_tokenize(question)))
        print(q_chunk)
        tmp=[]
        for st in sentences:
            st_chunk = ne_chunk(pos_tag(word_tokenize(st)))
            print(st_chunk)
        return ans if len(tmp)==0 else ' '.join(tmp)

    def checkType(self):
        res = {}
        for i,(key,v) in enumerate(self.search_q.items()):
            ans = 'Sorry, I don\'t know'
            for type in v:
                if type =='PERSON':
                    ans = self.person(key,self.q_s_pair[key])
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
    print(whq.checkType())
