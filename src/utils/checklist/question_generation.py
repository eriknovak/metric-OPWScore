import random
import nltk
from nltk.tokenize import word_tokenize
from checklist.editor import Editor
from checklist.perturb import Perturb
from src.utils.checklist.base import BaseTemplate


class QuestionGenTemplates(BaseTemplate):
    def __init__(self):
        super(QuestionGenTemplates, self).__init__()

    def remove_question_word(self, sent):
        q = ["what", "when", "where", "why", "how", "whose", "whom", "who", "which"]
        wor = word_tokenize(sent)
        sen = [w for w in wor if not w.lower() in q]
        out = " ".join(i for i in sen)
        return out if out != sent else sent

    def change_question_word(self, sent):
        q = ["what", "when", "where", "why", "how", "whose", "whom", "who", "which"]
        sen = []
        wor = word_tokenize(sent)
        for w in wor:
            if w.lower() in q:
                x = random.randint(0, len(q) - 1)
                while q[x] == w.lower():
                    x = random.randint(0, len(q) - 1)
                sen.append(q[x])
            else:
                sen.append(w)
        out = " ".join(wo for wo in sen)
        return out if out != sent else sent

    def change_names(self, sent):
        text = self.nlp(sent)
        x = Perturb.perturb([text], Perturb.change_names, n=1).data
        return sent if x == [] else x[0][1]

    def change_question_to_assetion(self, sent):
        q = ["what", "when", "where", "why", "how", "whose", "whom", "who", "which"]
        toks = nltk.word_tokenize(sent)
        sent = []
        sent2 = []
        l = len(toks)
        for w in toks:
            if w.lower() in q:
                sent.append("{mask}")
            else:
                sent.append(w)
            sent2.append(w)
        ss = " ".join(x for x in sent)
        ss2 = " ".join(x for x in sent2)
        temp = Editor().template(ss, remove_duplicates=True, nsamples=1)
        out = temp["data"][0]
        if out.lower() != ss2.lower():
            out = out.replace("?", ".")
        return out if out != sent else sent
