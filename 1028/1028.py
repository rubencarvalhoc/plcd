from lark import Lark,tree
from lark import Transformer,v_args
from jjcli import *

@v_args(inline=True)
class toLatex(Transformer):
    def ts(self, l):
        return str(l)
    def juntalinhas(self,item,*linhas):
        return f"{str(item)} {' '.join(linhas)}"
    def mksection(self,si,st,*sis):
        n="\n\n".join(sis)
        return f"\section {{{si} {st}}}\n{n}"
    def mklatex(self, *s):
        return "\n".join(s)



gramatica = r"""
    txt: sec+                                   ->mklatex

    sec: SECID titulo item*                     -> mksection

    titulo: SECTIT LINHA*                       ->juntalinhas

    item: ITEM LINHA*                           ->juntalinhas

    linha: LINHA                                ->ts

    elemento: LINHA
            |ITEM
            |SECTIT
            |SECID

    LINHA.2: /\S.*/ 
    ITEM.5: /• .*/
    SECTIT.5: /[–-] .*/
    SECID.5: /Secção [A-Z](?= [–-])/
    HEADER.5:/ {40}.*/
    %ignore HEADER
    %ignore /\f.*| +|\n/                           //Remover headers do tipo f e espaços extras

"""

p = Lark(gramatica, start='txt', parser='lalr')

with open('SIC-PT_seccao.txt', encoding='utf-8') as f:
    txt = f.read()


tree = p.parse(txt)
v=toLatex().transform(tree)

print(v)

#save to file
with open('out.latex', "w", encoding='utf-8') as f:
    f.write(v)
