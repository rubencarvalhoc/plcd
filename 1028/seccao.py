from lark import Lark,tree
from lark import Transformer
from jjcli import *
from lark import v_args

#class txt(Transformer):
#    relacoes = {}
#    def sujeito(self,args):
#        (v1,)=args
#        self.relacoes["/"] = v1
#        return v1
#    def pessoa(self, args):
#        (v1,) = args 
#        return f"{v1};"
#    def id(self, args): (v1,) = args ;return f'"{v1}"'
#    def rel(self, args): (v1,) = args ;return str(v1)
#    def anb(self, args): args_str = [str(arg) for arg in args] ;return f"digraph anb{{\n" + "\n".join(args_str) + "\n}"
#    def par(self, args):
#        (v1,v2) = args 
#        self.relacoes[v1] = v2
#        if v1 == "M": return f"{v2} -> {self.relacoes['/']};"
#        if v1 == "P": return f"{v2} -> {self.relacoes['/']};"
#        if v1 == "PP": return f"{v2} -> {self.relacoes['P']};"
#        if v1 == "PM": return f"{v2} -> {self.relacoes['P']};"
#        if v1 == "F": return f"{self.relacoes['/']} -> {v2};"
#    def nada(self,args): return""
#    def junta_par(self,args):
#        (v1,*v2) = args
#        return "\n".join(v2)

@v_args(inline=True)
class tolatex (Transformer):
    def tostring(self,l):
        return str(l)
    
    def junta_linhas(self,item, *linhas):
        return f"{str(item)}{' '.join(linhas)}"

    def mksecc(self,si,st,*sis):
        n = '\n'.join(sis)
        x = f"\section{{{si} {st}}}\n{n}"
        return x
        #return f"\section{{{si} {st}}}\n{'\n\n'.join(sis)}"

    def mklatex(self, *s):
        return '\n\n'.join(s)


gramatica = r"""
    txt: sec+                               ->mklatex
    sec: SECCID titulo item*                ->mksecc                      //_ -> diz para  não criar carimbo na arvore com o nome do token
    item: SECCITEM LINHA*                   ->junta_linhas
    linha: LINHA                            ->tostring
    titulo: SECCTIT LINHA*                  ->junta_linhas
    ?elemento:LINHA
        |SECCID
        |SECCITEM
        |SECCTIT
    

    LINHA.2: /\S.*/
    SECCITEM.5: /• .*/
    SECCTIT.5: /[–-] .*/
    SECCID.5: /Secção [A-Z] (?=[–-])/
    HEADER.5: / {40}.*/

    %ignore HEADER
    %ignore /\f.*| +|\n/                                 //remover header do tipo f e espaços extra
"""

p = Lark(gramatica, start='txt', parser='lalr') #transformer=txt())

#text = open("1028/seccao.txt").read()
with open("SIC-pt.txt.seccao.txt", encoding="utf-8") as f:
    text = f.read()

# Parse the input
tree = p.parse(text)
v=tolatex().transform(tree)
#print(tree) 
print(v)

with open("SIC-pt.txt.seccao.tex", "w", encoding="utf-8") as f:
   f.write(v)



"""for text in cl.text():
    rsi = csv.parse(text.strip()+"\n")
    #a=rsi["esquema"]
    #rfinal= [dict(zip(a,t)) for t in rsi["tuples"]]
    #print(rsi)
    print(json.dumps(rsi,indent=3))"""