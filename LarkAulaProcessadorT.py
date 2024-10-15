from lark import Lark, Transformer


class somalista(Transformer):
    def inteiro(self, args):
        return int(args[0])

    def lv1(self, args):
        return args[0]

    def lv2(self, args):
        return args[0] + args[1]

    pass


class maxlista(Transformer):
    def inteiro(self, args):
        return int(args[0])

    def lv1(self, args):
        return args[0]

    def lv2(self, args):
        lista = []
        lista.append(args[0])
        lista.append(args[1])
        return max(lista)

    pass


class html(Transformer):
    def inteiro(self, args):
        return f"<li> {args[0]} </li>"

    def lv1(self, args):
        return args[0]

    def lv2(self, args):
        return f"{args[0]}\n {args[1]}"

    def listafinal(self, args):
        return f"<ul {args[0]} </ul>"

    pass

class somalista2(Transformer):
    def inteiro(self, args): (v1,) = args  ; return int(v1)
    
    def lista(self, args)  : (v1,) = args  ; return v1

    def lv1(self, args)    : (v1,) = args  ; return int(v1)
    
    def lv2(self, args)    : (v1,v2) =args ; return v1 + v2
    pass

class html2(Transformer):
    def lm(self, args)      : (v1,)      = args   ; return f"<li> {v1} </li>"

    def lv1(self, args)     :    (v1,)   = args   ; return v1

    def lv2(self, args)     :    (v1,v2) = args   ; return f"{v1}\n {v2}"

    def lista(self, args)   :  (v1,)     = args   ; return f"<ul {v1} </ul>"

    def fi(self, args)      :    (v1,)   = args   ; return v1
    pass

gramatica = r"""
    listag: "(" lv ")"      -> lista
                 
    lv: elemento            -> lv1
      | elemento "," lv     -> lv2

    ?elemento: num          -> lm
            | listag        -> lm

    num : INT               -> fi
                    
    INT: /-?\d+/
    
    %ignore /\s+/
"""
li_parser = Lark(grammar=gramatica, start="listag", parser="lalr")


text = "( (99, (52, 35)), 98, 91 )"
tree = li_parser.parse(text)
r1 = html2().transform(tree)
#r2 = somalista2().transform(tree)
print(r1)
#print(tree.pretty())
