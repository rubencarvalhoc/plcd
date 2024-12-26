"""
name:ents

usage:
    -m n         print just top n
    -a           print alfabeticamente
    -p pessoa -m  print top n da pessoa
description: Ler ficheiro, escrever as entidades e as suas frequencias
"""

import spacy
from collections import Counter
from jjcli import *

cont = Counter()
nlp = spacy.load("pt_core_news_lg")
cl = clfilter(opt="v", man=__doc__)

def get_standard(text):
    doc = nlp(text)

    for sent in doc.sents:
        verbs = [token.text for token in sent if token.pos_ == 'VERB']
        ents = [(ent.text, ent.label_) for ent in sent.ents]
        noun = [token.text for token in sent if token.pos_ == 'NOUN']
        adjective = [token.text for token in sent if token.pos_ == 'ADJ']

    feats = {
        'verb': Counter(verbs),
        'ents': Counter(ents),
        'noun': Counter(noun),
        'adj': Counter(adjective)
    }
    return feats

with open('mini.txt', 'r', encoding='utf-8') as teste:
    texto = teste.read()

print(get_standard(texto))
