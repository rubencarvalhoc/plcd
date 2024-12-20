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
    
    elementos: anos|seccao|factos_int|CASA|PESSOA|ALCUNHA|doc_ref|bisneto|relacao|span|tag_por|tag_em|coisas

    anos: (ano_n|ano_m)+

    ano_n: "*" (LINHA) -> ano_n
    ano_m: "+" (LINHA) -> ano_m
    
    span: "CC" ANO ".." ANO -> span
    seccao: (doc_sec | bio_sec)+

    coisas: "#" LINHA* -> coisas
    doc_sec: "#doc" ABBRV? "{" (LINHA|coisas)* "}" -> doc_sec
    bio_sec: "#bio" "{" (LINHA|coisas)* "}" -> bio_sec

    factos_int: ("#dono" | "#mecenas_of" | "#tit" | "#morou" | "-") (BULLET|LINHA)* -> factos_int
    doc_ref: "#in-doc" ABBRV

    bisneto: "#bisneto" LINHA*

    tag_por: "#by" LINHA
    tag_em: "#in" LINHA

    DATE_RANGE: /\d{1,4}(\.\.\d{1,4})?/    
    relacao: "#I" "{" LINHA|DATE_RANGE* "}" 
           | "#S" "{" LINHA|DATE_RANGE* "}" 
           | "#F" "{" LINHA|DATE_RANGE* "}"
           | "#P" "{" LINHA|DATE_RANGE* "}"
           | "#I" LINHA
           | "#S" LINHA
           | "#F" LINHA
           | "#P" LINHA
    
    ANO.5: /\d{1,4}/
    CASA.5: /#=MHL\d+/
    DATA.5: /\d{1,2}\.\/\d{1,2}\.\/\d{1,4}/
    PESSOA.5: /#\/[^\n]+/
    ALCUNHA.5: /#= [^\n]+/ 
    ABBRV: /[^{}\n\-][^\{\}\n\-]*/
    LINHA.2: /\S.*/
    NOTAS: /Notas sobre a fam.+/  
    REF: /Ref:.+/
    BULLET: "-" LINHA


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
