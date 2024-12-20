from lark import Lark,tree
from lark import Transformer
import json

#1) criar um conversor que recebe comma separated values aninhados e gera json
#nome:altura:notas
#Rui:1.80:17,18,19
#só inteiros e strings

class T_json(Transformer):
    def mkint(self,args)        : (v1,) =args        ;return int(v1)
    def mkfloat(self,args)      : (v1,) =args        ;return float(v1)
    def mkstr(self,args)        : (v1,) =args        ;return str(v1)
    def mklista(self,args)      :                     return args
    def propaga(self,args)      : (v1,) =args        ;return v1
    def mkcsv(self,args)        : (v1,*v2) = args    ;return {"esquema": v1, "tuples": v2}
    def mkesquema(self,args)    : (v1,)=args         ; self.esquema=v1       ;return v1
    def mktuplo(self,args)        : (v1,) = args       ;return dict(zip(self.esquema,v1))

gramatica = r"""
    csv : esquema tuplo*                    ->mkcsv
    
    esquema: linha                          ->mkesquema

    tuplo: linha                            -> mktuplo

    linha : valor (":" valor)* "\n"         ->mklista

   ?valor: lista
         | atomico

    atomico: word                           ->propaga
         | float                            ->propaga
         | int                              ->propaga

    lista: atomico ("," atomico)+           ->mklista

    word: STRING                            ->mkstr

    float: FLOAT                            ->mkfloat

    int: INT                                ->mkint 
    
    STRING: /[a-zA-Z]+/

    INT : /-?\d+/

    FLOAT: /-?\d+\.\d+/

    %ignore /[\r\f\t]+/
    // %ignore /[.]+/
"""

csv= Lark(gramatica, start='csv', parser='lalr',transformer=T_json())


text = 'nome:altura:notas\nRui:1.80:10,18,19\nVanessa:1.90:10,15,faltou\n'
rsi = csv.parse(text)
#a = rsi['esquema']
#rfinal= [dict(zip(a,t)) for t in rsi['tuples']]
#print(rsi)

print(json.dumps(rsi,indent=2))
