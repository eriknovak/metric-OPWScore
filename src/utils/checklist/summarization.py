import random
import nltk
from nltk.tokenize import sent_tokenize
from checklist.perturb import Perturb
from src.utils.checklist.base import BaseTemplate


class SummTemplates(BaseTemplate):
    def __init__(self):
        super(SummTemplates, self).__init__()

    def sentence_reorder(self, sent):
        text_split = [i.text for i in self.nlp(sent).sents]
        random.shuffle(text_split)
        return " ".join(text_split)

    def change_names(self, sent):
        text = self.nlp(sent)
        x = Perturb.perturb([text], Perturb.change_names, n=1).data
        return sent if x == [] else x[0][1]

    def replace_nouns_prouns(self, sent):
        toks = sent_tokenize(sent)
        flag = 0
        sen = []
        for c in toks:
            pos = nltk.pos_tag(nltk.word_tokenize(c))
            l = len(pos)
            i = 0
            w, p = pos[0]
            if p in ["NNS", "NNPS"]:
                sen.append("They")
                flag = 1
                i = 1
            elif p in ["DT"]:
                w1, p1 = pos[1]
                if p1 in ["NNS", "NNPS"]:
                    sen.append("They")
                    flag = 1
                    i = 2
                if p1 == "NN":
                    sen.append("It")
                    flag = 1
                    i = 2
            while i < l:
                w, p = pos[i]
                sen.append(c)
                i += 1
        if flag == 1:
            out = " ".join(w for w in sen)
            return out
        return sent

    def drop_phrases(self, sent):
        pos = nltk.pos_tag(nltk.word_tokenize(sent))
        sen = []
        l = len(pos)
        flag = 0
        le = round(l * 0.2)
        x = random.randint(0, le - 1)
        y = 0
        for i in range(l - 1):
            w, p = pos[i]
            if x <= i and y < round(l * 0.2):
                y += 1
                flag = 1
                continue
            else:
                sen.append(w)
        sen.append(pos[l - 1][0])
        if flag == 1:
            out = " ".join(w for w in sen)
            return out
        return sent

    def repeat_sentences(self, sent):
        toks = sent_tokenize(sent)
        sent = []
        l = len(toks)
        i = 0
        while i < l:
            sent.append(toks[i])
            i += 1
        sent.append(toks[0])
        out = " ".join(x for x in sent)
        return out if out != sent else sent
