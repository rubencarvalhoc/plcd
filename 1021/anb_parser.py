from lark import Lark,tree
from lark import Transformer
import json


gramatica = r"""
    anb: pessoa+

    pessoa: "#" id
          | "#" id "{" par* info* "}"

    par: "#" rel id
       | "*" id
       | "{" id "}" 

    info: id id -> attribute    

    id : ID

    value: /\d+/

    rel: REL

    REL: /M|P|PP|PM/

    ID: /\w[\w ]*\w/

    %ignore /[\r\f\t\n ]+/

"""

anb_parser = Lark(gramatica, start='anb', parser='lalr')


text = """
# Martim {
# M     Paula
# P     carlos

# PP     cantiflas
# PM     maria da piedade {
           ano_nascimento  1940}
}
"""
rsi = anb_parser.parse(text)
print(rsi)
print(rsi.pretty())

# permitir aninhamento
# imprimir em formato DOT