from lark import Lark

# Grammar
gramatica = r"""
    anb: elementos*
    
    elementos: bio_sec | coisas | bullet
    
    coisas.3: "#" LINHA*

    doc_sec: "#doc" ABBRV "{" doc_content RBRACE
    doc_content: (LINHA | coisas)*

    bio_sec.3: "#bio" "{" bio_content RBRACE
    bio_content: (LINHA | coisas)*

    bullet.3: "- " LINHA+
    RBRACE: /}/
    LBRACE: /{/
    LINHA: /[^\n\-].+/ 
    ABBRV: /[A-Za-z]{2}\d/

    %ignore /Notas sobre a fam.+/
    %ignore /Ref:.+/
    %ignore "==="
    %ignore / +|\n|\t/
"""

# Initialize parser
ANB_parser = Lark(gramatica, start='anb', parser='lalr')

# Input text
txt = """
- Foi funcionário da Fábrica de Curtumes do Bessa de seu tio-avô
  Eduardo Honório de Lima.

- Ola

#bio{
ola
}
"""

# Tokenize the input
tokens = list(ANB_parser.lex(txt))
print("Tokens:")
for token in tokens:
    print(f"Token(type={token.type}, value={token.value})")

# Parse the input
tree = ANB_parser.parse(txt)
print("\nParse Tree:")
print(tree.pretty())