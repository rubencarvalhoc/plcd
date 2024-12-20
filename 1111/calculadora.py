from math import sqrt, factorial
from lark import Lark,tree,v_args,Transformer
from jjcli import *

@v_args(inline=True)
class calc(Transformer):
    mem = {}
    def exps(self,*n): return n
    def at(self, id, n): return n
    def exp1(self,n): return n
    def exp2(self, n1, n2): return n1+n2
    def exp3(self, n1, n2): return n1-n2
    def exp4(self, n1, n2): return n1*n2
    def exp5(self, n1, n2): return n1/n2
    def exp6(self, n1, n2): return n1**n2
    def exp7(self, n): return -n
    def exp8(self, n): return self.mem.get(n,0) 
    def exp9(self, n):return sqrt(n)
    def exp10(self, n): return factorial(n)
    def ID(self,i): return str(i)
    def NUM(self,n): return float(n)


gramatica = r"""
    exps: (exp _NL|_NL)*      

    at: ID "=" exp                             ->at

    exp: p                                      ->exp1
        | exp "+" p                             ->exp2
        | exp "-" p                             ->exp3

    p: f                                      ->exp1
        | p "*" f                             ->exp4
        | p "/" f                             ->exp5

    f: NUM                                    ->exp1
        | NUM "^" f                           ->exp6
        | "-" f                               ->exp7
        | "(" exp ")"                         ->exp1
        |ID                                   ->exp8
        | "sqrt" "(" exp ")"                  ->exp9
        | f "!"                               ->exp10
        | ID "("  ")"

    NUM.5: /-?\d+(\.\d+)?/
    _NL.5: /\n/
    ID.-1: /\w+:/
    QUANTIDADE: /\d+/

    %ignore /\s+|#.*/
"""

p = Lark(gramatica, start='exps', parser='lalr')
with open("exemplo.txt", encoding="utf-8") as f:
    text = f.read()

tree = p.parse(text)
print(tree)
v=calc().transform(tree)
print(v) 
