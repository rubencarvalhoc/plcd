"""
name:ents 

usage:
Ler ficheiro, escrever as entidades
"""

import spacy
from collections import Counter
from jjcli import *

nlp = spacy.load("pt_core_news_sm")

cl = clfilter(opt="", man=__doc__)

freq = Counter()

for text in cl.text():
    livro = text.splitlines()

    for linha in livro:
        doc = nlp(linha)
        for entity in doc.ents:
            freq[entity.text] += 1


def dic_pp(dic):
    for k, v in dic:
        print(f"{k}  {v}")


dic_pp(freq.most_common(100))
