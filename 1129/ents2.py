"""
name:ents

usage:
description: Ler ficheiro, escrever as entidades e as suas frequencias
    -m n         print just top n
    -a           print alfabeticamente
    -p pessoa -m  print top n da pessoa
"""

# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy
from collections import Counter
from jjcli import *
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("pt_core_news_sm")

cl=clfilter(opt="m:ap:", man=_doc_)
freqs=Counter()
# Process whole documents
for text in cl.text():
    livro=text.splitlines()

    # Find named entities, phrases and concepts
    for linha in livro:
        doc=nlp(linha)

        for ent1 in doc.ents:
            for ent2 in doc.ents:
                if ent1.text!=ent2.text:
                    if "-p" in cl.opt:
                        if ent1.text == cl.opt["-p"]:
                            freqs[ent2.text]+=1
                    else:
                        freqs[(ent1.text,ent2.text)]+=1

def dic_pp(dic):
    for ent, ocorr in dic:
        if "-a" in cl.opt:
            print(f'{ent}\t{ocorr}')
        else:
            print(f"{ocorr}\t{ent}")

m=int(cl.opt.get("-m",10000))
if "-a" in cl.opt:
    dic_pp(sorted(freqs.most_common(m)))
else:
    dic_pp(freqs.most_common(m))