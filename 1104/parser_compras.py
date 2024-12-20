from lark import Lark,tree
from lark import Transformer,v_args
from jjcli import *

@v_args(inline=True)
class pp(Transformer):
    def mkitem(self, num, nome, preco, quantidade):
        return f"{nome} - Preço: {preco}; Quantidade {quantidade}"
    
    def mksection(self,tipo, *linhas):
        titulo = tipo
        lista_items = "\n".join(linhas)
        return f"{titulo}{lista_items}"
    
    def mklatex(self, *s):
        return "\n".join(s)

@v_args(inline=True)
class total(Transformer):
    def lc(self, *s): return sum(s)
    def sec(self, id, *linhas): return sum(linhas)
    def item(self, i,c,p,q): return p*q
    def numero(self, n): return float(n)
    def quantidade(self,q): return float(q)

gramatica = r"""
    lc: sec+

    sec: NOME ":" linha* ->mksection
    linha: "-" NUM "::" NOME "::" preco "::" quantidade ";" ->mkitem

    preco: NUM
    quantidade: NUM
    NUM.4: /\d+(\.\d+)?/ 
    NOME.2:/\w[\w ]*\w/
    // NOME: [a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ ]*[a-zA-ZÀ-ÿ]/

    %ignore /\s+|#.*/                           //Remover headers do tipo f e espaços extras

"""

p = Lark(gramatica, start='lc', parser='lalr')

with open('exemplo.txt', encoding='utf-8') as f:
    txt = f.read()


tree = p.parse(txt)
v=total().transform(tree)

print(v.pretty())
