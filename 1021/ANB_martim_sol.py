from lark import Lark,tree
from lark import Transformer
from jjcli import *

class dot(Transformer):
    relacoes ={}
    def sujeito(self, args):
        (v1,) = args
        self.relacoes["/"] = v1
        return v1
    def pessoa_simples(self, args): 
        (v1,) = args
        return v1+";"
    def id(self, args): (v1,) = args ;return f'"{v1}"'
    def rel(self, args): (v1,) = args ;return v1
    def mklist(self, args): n = "\n"; args_str = [str(arg) for arg in args] ;return f"""digraph anb{{{n.join(args_str)}}}"""
    def par(self, args): 
        (v1,v2)=args
        self.relacoes[v1] = v2
        if v1 == "M": return f"{v2} -> {self.relacoes['/']};"
        if v1 == "P": return f"{v2} -> {self.relacoes['/']};"
        if v1 == "PP": return f"{v2} -> {self.relacoes['P']};"
        if v1 == "PM": return f"{v2} -> {self.relacoes['P']};"
        if v1 == "F": return f"{self.relacoes['/']} -> {v2}"

    def nada(self, args): return ""
    def junta_par(self, args):
        (v1,*v2) = args
        return "\n".join(v2)
    

gramatica = r"""
    anb: pessoa+              -> mklist

    pessoa: sujeito              -> pessoa_simples
        | sujeito "{" par* "}" -> junta_par

    sujeito: "#" id              -> sujeito
        
    par: "#" rel id             -> par
        | "*" id                -> nada

    id: ID                      -> id

    rel: REL                    -> rel

    REL: /PP|PM|M|P|F/

    ID: /\w[\w ]*\w/

    %ignore /[\r\f\t\n ]+/
"""

ANB_parser = Lark(gramatica, start='anb', parser='lalr', transformer=dot())

text = """
# Martim{
#M Paula
#P Carlos

#PP Cantiflas
#PM Maria da Piedade
}
# PS
# Joana {#M Maria
#F Cantiflas}
"""

# Parse the input
tree = ANB_parser.parse(text)

print(tree) 


"""for text in cl.text():
    rsi = csv.parse(text.strip()+"\n")
    #a=rsi["esquema"]
    #rfinal= [dict(zip(a,t)) for t in rsi["tuples"]]
    #print(rsi)
    print(json.dumps(rsi,indent=3))"""


# Trabalho prático 
# 1) A realizar em grupos de dois: Linguagem tipo ANB | Definir a linguagem
# 2) Demonstrar com dois exemplos. O do professor e a nosso próprio
