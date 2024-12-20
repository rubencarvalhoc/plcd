from jjcli import *
import yaml

cl = clfilter()



def f2(l_filhos, p1, p2):
    b4 = ""
    b3 = ""
    b2 = ""
    b1 =""
    shape = "[shape = point]"
    for i,v in enumerate(l_filhos):
        b1+=f"F1{i} ->"
        b2+=f"F1{i} {shape}\n"
        b3+=f"F{i} [shape = box, label=\"{v}\"]\n"
        b4+= f"F1{i} -> F{i} [dir = none]\n"
    b1 = b1[:-2]

    return f"""
    digraph Familia{{
    subgraph Generation1 {{
    rank  =  same
    P1 [shape = box, label="{p1}", color = blue] 
    P2 [shape = box, label="{p2}", color = pink]  

    Familia [shape = point]
    P1 -> Familia -> P2 [dir = none]
  }}
    subgraph Generation1Sons {{
    rank  =  same
    {b2}
    
    {b1} [dir = none]
  }}
    Familia -> F10 [dir = none]
    subgraph Generation2 {{
    rank  =  same
    {b3}
  }}
  
  {b4}
}}"""

for txt in cl.text():
    v = yaml.safe_load(txt)
    dot = f2(v["f"], v["pai"], v["mae"])
    print(dot)

with open (f"{cl.filename()}.dot", 'w') as f:
    print(dot, file=f)

qxsystem(f"dot -Tpng {cl.filename()}.dot -o {cl.filename()}.png")