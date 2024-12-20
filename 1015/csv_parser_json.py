from lark import Lark,tree
from lark import Transformer

#1) criar um conversor que recebe comma separated values aninhados e gera json
#nome:altura:notas
#Rui:1.80:17,18,19
#sรณ inteiros e strings

gramatica = Lark(r"""
    csv : linha*

    linha : valor (":" valor)* "\n"

    valor: lista
         | word 
         | float

    lista: num ("," num)* 

    word: STRING

    num: INT

    float: FLOAT
    
    STRING: /[a-zA-Z]+/

    INT : /-?\d+/

    FLOAT: /-?\d+\.\d+/

    %ignore /[\r\f\t]+/
    %ignore /[.]+/
""", start='csv', parser='lalr',)


text = 'nome:altura:notas\nRui:1.80:10,18,19\n'
parsed_tree = gramatica.parse(text)
print(parsed_tree.pretty())