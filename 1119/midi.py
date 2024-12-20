from MIDI import MIDIFile
from sys import argv
from lark import Lark, Transformer,v_args
import re

@v_args(inline=True)
class limpar(Transformer): # mapear número da seccao com o titulo e com a descrição se aplicável
    tabela = {}
    notas=[]
    def NOTA_ON(self, n):  return re.findall(r'\w\d+',n)
    def NOTA_OFF(self, n):  return re.findall(r'\w\d+',n)
    def nota1(self,n): self.tabela[n[1]]=n
    def nota2(self,n): self.notas.append(self.tabela[n[1]]+n)
    def txt(self,*s): return self.notas

def parse(file):
    out=""
    c=MIDIFile(file)
    c.parse()
    print(str(c))
    for idx, track in enumerate(c):
        track.parse()
        out+=f'Track {idx}:'
        out+=str(track)
    return out


txt=parse(argv[1])


gramatica = r"""
    txt: nota+
    
    nota: NOTA_ON           ->nota1 
        | NOTA_OFF          ->nota2 

    LINHA.2: /\S.*/
    NOTA_ON.3:/MIDI@\d+ NOTE_ON\[0\] \w+ ON velocity := \d+/
    NOTA_OFF.3: /MIDI@\d+ NOTE_OFF\[0\] \w+ OFF velocity := 0/

    %ignore LINHA
    %ignore / +|\n|\f/                           //Remover headers do tipo f e espaços extras

"""

p = Lark(gramatica, start='txt', parser='lalr')

tree = p.parse(txt)
print(tree.pretty())
v=limpar().transform(tree)
print(v)