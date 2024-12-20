from lark import Lark,tree,v_args,Transformer
from jjcli import *



@v_args(inline=True)
class tolatex(Transformer):
    def item(self, item, conteudo, numero, quantidade):
        return f"{conteudo} - Preço: {numero}€ - Quantidade: {quantidade}"
    
    def sec(self, tipo, *itens):
        titulo = tipo
        lista_itens = '\n'.join(itens)
        return f"{titulo}{lista_itens}"
    
    def lc(self, *seccoes):
        return '\n\n'.join(seccoes)

@v_args(inline=True)
class total(Transformer):
    def lc(self, *s): return sum(s)
    def sec(self, id, *items): return sum(items)
    def item(self, i,c,p,q): return p*q
    def NUMERO(self,n): return float(n)
    def QUANTIDADE(self,q): return float(q)

@v_args(inline=True)
class dicionario(Transformer):
    def lc(self, *s): return dict(s)
    def sec(self, id, *items): return(id,sum(items))
    def item(self, i,c,p,q): return p*q
    def NUMERO(self,n): return float(n)
    def QUANTIDADE(self,q): return float(q)
    def ID(self,id): return id.value

@v_args(inline=True)
class mais_caro(Transformer):
    def lc(self, *s): return max(sum(s,start=[]),key=lambda x:x[0])
    def sec(self, id, *items): return list(items)
    def item(self, i,c,p,q): return (p*q,c)
    def NUMERO(self,n): return float(n)
    def QUANTIDADE(self,q): return float(q)
    def ID(self,id): return id.value
    def CONTEUDO(self,c): return c.value

@v_args(inline=True)
class mais_caro2(Transformer):
    mais_caroP = 0
    mais_caroN = "nada"
    def lc(self, *s): return (self.mais_caroP,self.mais_caroN)
    #def sec(self, id, *items): return list(items)
    def item(self, i,c,p,q): 
        if p*q > self.mais_caroP:
            self.mais_caroP = p*q
            self.mais_caroN = c
    def NUMERO(self,n): return float(n)
    def QUANTIDADE(self,q): return float(q)
    def ID(self,id): return id.value
    def CONTEUDO(self,c): return c.value

gramatica = r"""
    lc: sec+                                                            //->mklatex
    sec: ID item+                                                       //->mkseccao                      //_ -> diz para  não criar carimbo na arvore com o nome do token
    item: ITEM "::" CONTEUDO "::" NUMERO "::" QUANTIDADE ";"            //->mkitem
    
    NUMERO: /\d+(\.\d+)?/
    CONTEUDO.2: /[a-zçãá][a-zçãá ]*[a-zçãá](?= *::)/
    ITEM.5: /-\d+/
    ID.5: /\w+:/
    //SPECIAL: "::"
    QUANTIDADE: /\d+/

    %ignore /\f.*| +|\n/                                 //remover header do tipo f e espaços extra
"""

p = Lark(gramatica, start='lc', parser='lalr')#transformer=txt())

#text = open("1028/seccao.txt").read()
with open("exemplo.txt", encoding="utf-8") as f:
    text = f.read()

tree = p.parse(text)
v=tolatex().transform(tree)
#print(tree) 
t=total().transform(tree)
print(t)
d=dicionario().transform(tree)
print(d)
m=mais_caro().transform(tree)
print(m)
m2=mais_caro2().transform(tree)
print(m2)
#print(v)

with open("exemplo.tex", "w", encoding="utf-8") as f:
   print(v,f"\n total={t}",file=f)

#item mais caro