"""
name:ents

usage:
    -m n         print just top n
    -a           print alfabeticamente
    -p pessoa -m  print top n da pessoa
description: Ler ficheiro, escrever as entidades e as suas frequencias
"""

####################
#1. dado um corpus de documento
#2. calcular um corpus de ocorrência de verbos
#3. dado uma notícia indicar os verbos que mais se distanciam do padrão
#4. calcular as entidades que mais se distanciam do padrão
###################
#1 dado um texto calcular um padrão
#2 dado uma noticia calcular um padrão a nivel de verbos e entidades
####################
# Carregar verbopt.freqREL 
# Percorrer os verbos do verbopt.freqREL e comparar com os verbos do lemapos.totalpt.txt
# racio[v1] = *verbo[v1]*/totalpt[v1]
# se o racio for um counter podemos obter os most commons

# pip install -U spacy
# python -m spacy download en_core_web_sm
import spacy
from collections import Counter
from jjcli import *

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("pt_core_news_lg")

verbo_freq = Counter()
cl=clfilter(opt="m:ap:", man=__doc__)
freqs=Counter()
# Process whole documents
import spacy

#class EntityRetokenizeComponent:
#    def __init__(self, nlp):
#        pass
#    def __call__(self, doc):
#        with doc.retokenize() as retokenizer:
#            for ent in doc.ents:
#                retokenizer.merge(doc[ent.start:ent.end], attrs={"LEMMA": str(doc[ent.start:ent.end])})
#        return doc

#retokenizer = EntityRetokenizeComponent(nlp) 
#nlp.add_pipe(retokenizer, name='merge_phrases', last=True)
nlp.add_pipe("merge_entities")

def processa_paragrafo(linha):
    documento = nlp(linha)
    for sentence in documento.sents:
        print("#",sentence.text)
        for token in sentence:
            word = token.text
            lema = token.lemma_
            pos = token.pos_
            print(f"{word}|{lema}|{pos}")
            if pos == "VERB":
                verbo_freq[lema] += 1


def processa_noticia(meta,texto):
    for linha in texto.splitlines():
        processa_paragrafo(linha)
    #print(texto,"\n#")

meta = texto = ""
estado = 1
for linha in cl.input():
    if estado == 1 and linha == "<body>":
        estado = 2
        texto = ""
    elif estado == 1:
        meta += linha
    elif estado == 2 and linha == "</pub>":
        processa_noticia(meta,texto)
        meta = ""
        estado = 1
    elif estado == 2 and "#DATE:" in linha:
        meta += linha
    elif estado == 2 and linha == "":
        texto += "\n"                
    elif estado == 2:
        texto += linha + " "
    if cl.filelineno() > 1000:
        break



    # Find named entities, phrases and concepts
    # for linha in linha:
    #     doc=nlp(linha)
    #     for ent1 in doc.ents:
    #         for ent2 in doc.ents:
    #             if ent1.text!=ent2.text:
    #                 if "-p" in cl.opt:
    #                     if ent1.text == cl.opt["-p"]:
    #                         freqs[ent2.text]+=1
    #                 else:
    #                     freqs[(ent1.text,ent2.text)]+=1


def dic_verbo_freq(verbo_freq):
    for verbo, freq in verbo_freq:
        if "-a" in cl.opt:
            print(f'{verbo}\t{freq}')
        else:
            print(f"{freq}\t{verbo}")

def dic_freq_rel(frequenc):
    freq_rel = Counter()
    total = frequenc.total()
    for palavra, freq in frequenc.items():
        freq_rel[palavra] = (freq/total)*10**6
    print(total)
    return freq_rel

n = int(cl.opt.get("-m", 100))
# if "-a" in cl.opt:
#     dic_verbo_freq(sorted(verbo_freq.most_common(n)))
# else:
#     dic_verbo_freq(verbo_freq.most_common(n))

freq_rel = dic_freq_rel(verbo_freq)
print(freq_rel)

#def dic_pp(dic):
#    for ent, ocorr in dic:
#        if "-a" in cl.opt:
#            print(f'{ent}\t{ocorr}')
#        else:
#            print(f"{ocorr}\t{ent}")
#
#m=int(cl.opt.get("-m",10000))
#if "-a" in cl.opt:
#    dic_pp(sorted(freqs.most_common(m)))
#else:
#    dic_pp(freqs.most_common(m))