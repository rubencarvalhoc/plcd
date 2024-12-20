from lark import Lark,tree
from lark import Transformer
from jjcli import *

class dot(Transformer):
    def elementos(self, args): return args[0]
    def PESSOA(self, args): return ''.join(args)
    def ALCUNHA(self, args): return ''.join(args)
    def ano_n(self, args): return args[0]
    def ano_m(self, args): return args[0]
    def DATAS(self, args): return ''.join(args)
    def doc_section(self, args): return {"tipo": "doc_section", "valor": args}
    def bio_section(self, args): return {"tipo": "bio_section", "valor": args}
    def factos_int(self, args): return {"tipo": "factos_int", "valor": args}
    def doc_ref(self, args): return {"tipo": "doc_ref", "valor": args}
    def linhas(self, args): return args
    def relacao(self, args): return args
    
gramatica = r"""
    anb: elementos+
    
    elementos: anos|seccao|factos_int|pessoa|ALCUNHA|doc_ref|bisneto|relacao|BULLET

    anos: (ano_n|ano_m)+

    pessoa: PESSOA LINHA*

    ano_n: "*" DATAS -> ano_n
    ano_m: "+" DATAS -> ano_m

    seccao: doc_sec | bio_sec
    doc_sec: "#doc" ABBRV? "{" LINHA* "}" -> doc_sec

    bio_sec: "#bio" "{" LINHA* "}"? -> bio_sec

    factos_int: ("#dono" | "#mecenas_of" | "#tit" | "#morou") LINHA -> factos_int
    doc_ref: "#in-doc" ABBRV

    bisneto: "#bisneto" LINHA*
    
    relacao: "#I" "{" conteudo_relacao* "}"
    conteudo_relacao: relacao_f | LINHA
    relacao_f: ("#S" | "#F") LINHA

    PESSOA.5: /#\//
    ALCUNHA.5: /#= [^\n]+/ 
    DATAS.5: /\d{1,4}/
    ABBRV: /[^\{\}\n\-]+/
    NOVA_LINHA: "\n"    
    LINHA.2: /[^\n]+/
    BULLET: "-" LINHA
    NOTAS: /Notas sobre a fam.+/  
    REF: /Ref:.+/

    %ignore NOTAS
    %ignore REF
    %ignore "==="
    %ignore / +|\n/
    %ignore " "
"""

ANB_parser = Lark(gramatica, start='anb', parser='lalr', transformer=dot())

with open('exemplo.txt', encoding='utf-8') as f:
    txt = f.read()


tree = ANB_parser.parse(txt)
v = dot().transform(tree)

print(v.pretty())
