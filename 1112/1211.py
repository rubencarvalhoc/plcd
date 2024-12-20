from lark import Lark,tree
from lark import Transformer,v_args
from jjcli import *
import pandas as pd

#df = pd.read_csv('---.csv')

@v_args(inline=True)
class limpar(Transformer):
    tab_cod_5 = {} # mapear número da seccao com o titulo e com a descrição se aplicável
    tab_cod_1 = {}
    tabela_final = {}
    def SEC(self, seccao):  return tuple(str(seccao).split(maxsplit=1))
    def SEC1(self, seccao): return tuple(str(seccao).split(maxsplit=1))
    def SEC2(self, seccao): return tuple(str(seccao).split(maxsplit=1))
    def SEC3(self, seccao): return tuple(str(seccao).split(maxsplit=1))
    def SEC4(self, seccao): return tuple(str(seccao).split(maxsplit=1))
    def SEC5(self, seccao): return tuple(str(seccao).split(maxsplit=1))
    def sec5(self, sec, *desc): k = sec[0]; self.tab_cod_5[k] = {"Tit": sec[1], "Desc": desc};
    def sec1(self, sec, *desc): k = sec[1]; self.tab_cod_1[k] = {"Tit": sec[1], "Desc": desc};
    def ITEM(self, item):   return str(item)
    def LINHA(self, linha): return str(linha)
    def desc(self, *items): return list(items)
    def COMP(self, comp):   return str(comp)
    def comp(self, *items): return list(items)
    def N_INC(self, n_inc): return str(n_inc)
    def n_inc(self, *items):return list(items)
    def txt(self, *coisa):  return (self.tab_cod_5, self.tab_cod_1)

gramatica = r"""
    txt: coisa+

    coisa: sec1|sec2|sec3|sec4|sec5|SECV|desc

    sec1: SEC  (desc|SECV|sec5|sec2)*
    sec2: SEC2 (desc|SECV|sec5|sec4|sec3)*
    sec3: SEC3 (desc|SECV|sec5|sec4)*
    sec4: SEC4 (desc|SECV|sec5)*
    sec5: SEC5 (desc|SECV)*

    desc: (LINHA|comp|n_inc|ITEM)+
    n_inc: N_INC (ITEM|LINHA)*
    comp: COMP (ITEM|LINHA)*

    LINHA.2: /\S.*/
    N_INC.3: /Não inclui:/
    COMP.3: /Compreende.*/
    ITEM.5: /· .*/
    SEC.5: / *[A-Z]  .*/
    SEC2.5: /\d{2} +.*/
    SEC3.5: /\d{3} +.*/
    SEC4.5: /\d{4} +.*/
    SEC5.5: /\d{5} +.*/
    SECV.4: /\d{2,5}/
    
    HEADER.5:/ {40}.*\n/
    NUM_PAG: /\f.*\n *\d+\n/

    %ignore NUM_PAG
    %ignore HEADER
    %ignore / +|\n|\f/                           //Remover headers do tipo f e espaços extras

"""

p = Lark(gramatica, start='txt', parser='lalr')

with open('SIC-PT2.txt', encoding='utf-8') as f:
    txt = f.read()


tree = p.parse(txt)
v=limpar().transform(tree)
#print(v.pretty())
print(v)

#Construção do dicionario 







#save to file
with open('out.txt', "w", encoding='utf-8') as f:
    print(v[0],"\n---\n", v[1], file=f)
