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

nlp = spacy.load("pt_core_news_lg")


cl=clfilter(opt="m:ap:", man=__doc__)
