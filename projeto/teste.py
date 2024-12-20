from lark import Lark,tree
from lark import Transformer
from jjcli import *
import json
import re

class organizer(Transformer):
    fulldict = {}
    name = None
    def mkdict(self,args): 
        if len(args[1].split(":", maxsplit=2)) > 1:
            nome =args[1].split(":", maxsplit=2)[1]
            self.fulldict[nome] = {}
            self.name = nome
        else:
            self.fulldict[args[1]] = {}
            self.name = args[1]

        return self.fulldict
    def mkalcunha(self,args):
        if 'Alcunha' not in self.fulldict[self.name]:
            self.fulldict[self.name]['Alcunha'] = args[1]
        return str(args[0]),args[1]
    def mknascimento(self,args):
        if 'Nascimento' not in self.fulldict[self.name]:
            self.fulldict[self.name]['Nascimento'] = args[1]
        return str(args[0]),args[1]
    def mkfalecimento(self,args):
        if 'Falecimento' not in self.fulldict[self.name]:
            self.fulldict[self.name]['Falecimento'] = args[1]
        return str(args[0]),args[1]
    def mkcasamento(self,args):
        if 'Casamento' not in self.fulldict[self.name]:
            self.fulldict[self.name]['Casamento'] = [args[0],args[1]]
        return self.fulldict
    def mkrelacao(self, args):
        dicta = {'Relacao': {'Tipo': args[0], 'Relacionado': args[1]}}
        def process_next_args(next_args, dicta):
            if isinstance(next_args, tuple):
                id, cont = next_args
                if id == "* ":
                    dicta['Relacao']['Nascimento'] = cont
                elif id == "#= ":
                    dicta['Relacao']['Alcunha'] = cont
                elif id == "+ ":
                    dicta['Relacao']['Falecimento'] = cont
                    if self.fulldict[self.name]['Falecimento'] == cont:
                        del self.fulldict[self.name]['Falecimento']
                else:
                    dicta['Relacao'].setdefault('Subrelacao', []).append(next_args)
            else:
                dicta['Relacao'].setdefault('Factos', []).append(next_args)
        for next_args in args[2:]:
            process_next_args(next_args, dicta)
        self.fulldict.setdefault(self.name, {}).setdefault('Relacoes', []).append(dicta)
        return self.fulldict
    def mkrelacao2(self,args):
        dicta = {'Relacao': {'Tipo': args[0], 'Relacionado': args[1]}}
        def process_next_args(next_args, dicta):
            if isinstance(next_args, tuple):
                id, cont = next_args
                if id == "* ":
                    dicta['Relacao']['Nascimento'] = cont
                elif id == "#= ":
                    dicta['Relacao']['Alcunha'] = cont
                elif id == "+ ":
                    dicta['Relacao']['Falecimento'] = cont
                else:
                    dicta['Relacao'].setdefault('Subrelacao', []).append(next_args)
            else:
                dicta['Relacao'].setdefault('Factos', []).append(next_args)
                if None in dicta['Relacao']['Factos']:
                    del dicta['Relacao']['Factos'] 
        for next_args in args[2:]:
            process_next_args(next_args, dicta)
        self.fulldict.setdefault(self.name, {}).setdefault('Relacoes', []).append(dicta)
        return self.fulldict
    def mkbullet(self,args):
        if 'Factos Lixo' not in self.fulldict[self.name]:
            self.fulldict[self.name]['Factos Lixo'] = []
            self.fulldict[self.name]['Factos Lixo'].append(args[0])
        else:
            self.fulldict[self.name]['Factos Lixo'].append(args[0])
    def mksubrelation(self,args):
        return args[0], str(args[1])
    def mkrelbul(self,args):
        return str(args[0])
    def mkrelfac(self,args):
        return str(args[0])
    def mkdoc_sec(self,args):
        self.fulldict[self.name]['Documentacao'] = {}
        pattern = re.match(r'[A-Za-z]{2,4}\d', args[1])
        if pattern:
            self.fulldict[self.name]['Documentacao']['Index'] = args[1]
            self.fulldict[self.name]['Documentacao']['Texto'] = args[2:]
        else:
            self.fulldict[self.name]['Documentacao']['Texto'] = args[1:]

        pattern2 = re.match(r'^=(.+)', self.fulldict[self.name]['Documentacao']['Texto'][0])
        if pattern2:
            self.fulldict[self.name]['Documentacao']['Título'] = str(pattern2.groups(1))[2:-3]
            del self.fulldict[self.name]['Documentacao']['Texto'][0]
    def mkcoisas(self,args):
        if 'Factos Importantes' not in self.fulldict[self.name]:
            self.fulldict[self.name]['Factos Importantes'] = []
            self.fulldict[self.name]['Factos Importantes'].append(args[0])
        else:
            self.fulldict[self.name]['Factos Importantes'].append(args[0])
    def mkbio_sec(self,args): 
        self.fulldict[self.name]['Bio'] = [arg.lstrip('-') for arg in args[1:-2]]


    def ABBRV(self,abreviacao):
        return str(abreviacao)
    def RELACAO2(self,relacao):
        if str(relacao) == "#MP ":
            relation = "Avô Materno"
        elif str(relacao) == "#MPI ":
            relation = "Tio Avô Materno"
        elif str(relacao) == "#PP ":
            relation = "Avô Paterno"
        elif str(relacao) == "#PM ":
            relation = "Avó Paterna"
        elif str(relacao) == "#MM ":
            relation = "Avó Materna"
        else:
            relation = str(relacao)
        return relation
    def RELACAO(self, relacao):
        relacao_str = str(relacao)
        if "#I" in relacao_str:
            relation = "Irmao"
        elif "#S" in relacao_str:
            relation = "Conjuge"
        elif "#F" in relacao_str:
            relation = "Filho"
        elif "#P" in relacao_str:
            relation = "Pai"
        elif "#M" in relacao_str:
            relation = "Mãe"
        else:
            relation = relacao_str
        return relation
    def ANO(self,ano):
        return int(ano)
    def LINHA(self,linha): 
        return str(linha)
    def HASH(self,hash):
        return str(hash)

gramatica = r"""
    anb: elementos*
    
    elementos: seccao|coisas|bullet|nome|alcunha|nascimento|falecimento|relacao|relacao2|sub_rel|casamento
    
    nascimento.4: NASCIMENTO LINHA                                                                  -> mknascimento
    falecimento.4: FALECIMENTO LINHA                                                                -> mkfalecimento
    nome.4: NOME LINHA                                                                              -> mkdict
    alcunha.4: ALCUNHA LINHA                                                                        -> mkalcunha
    bullet.4: ("- " LINHA)                                                                          -> mkbullet
    coisas.4: "#" LINHA+                                                                            ->mkcoisas
    casamento.4: "CC" ANO ".." ANO                                                                  -> mkcasamento

    seccao.4: (doc_sec | bio_sec)+
    doc_sec.4: SEC_DOC ABBRV? "{" (LINHA|coisas)* "}"                                               -> mkdoc_sec

    bio_sec.4: SEC_BIO "{" (LINHA|HASH)* "}"                                                        -> mkbio_sec

    relacao.4: RELACAO "{" LINHA (sub_rel|nascimento|falecimento|bullet_rel|alcunha|facto_rel)* "}" -> mkrelacao
    relacao2.3: RELACAO2 LINHA (nascimento|falecimento|bullet|alcunha)*                             -> mkrelacao2
    sub_rel: RELACAO LINHA                                                                          -> mksubrelation
    bullet_rel: ("- " LINHA)                                                                        -> mkrelbul
    facto_rel: ("#" LINHA2)                                                                         -> mkrelfac

    
    HASH: /#/
    RELACAO2.3: /#[A-Z]{2,3} ?/
    LINHA2.1: /[^\n{}#\*\+\-]+/
    LINHA.2: /[^\n{}#]+/
    NOTAS: /Notas sobre a fam.+/  
    REF: /Ref:.+/
    ABBRV.3: /[A-Za-z]{2,4}\d/
    NOME.3: /#\/ ?/
    ALCUNHA.3: /#= ?/
    NASCIMENTO.3: /\* ?/
    FALECIMENTO.3: /\+ ?/
    SEC_DOC.3: /#doc ?/
    SEC_BIO.3: /#bio ?/
    RELACAO.3: /#[A-Z] ?/
    ANO: /\d{1,4}/
    IGN_TIO: /=== Tio Frederico/
    %ignore NOTAS
    %ignore REF
    %ignore "==="
    %ignore IGN_TIO
    %ignore / +|\n|\t/
    %ignore "Era filho de"
    %ignore "e de sua mulher"
    %ignore "Neto paterno de"
    %ignore "Neto materno de"
    %ignore "que era irmão de"
"""

ANB_parser = Lark(gramatica, start='anb', parser='lalr')#, transformer=organizer())
with open('exmini.txt', encoding='utf-8') as f:
    txt = f.read()

# tokens = list(ANB_parser.lex(txt))
# print("Tokens:")
# for token in tokens:
#     print(f"Token(type={token.type}, value={token.value})")

tree = ANB_parser.parse(txt)
organizer_instance = organizer()
v=organizer_instance.transform(tree)


dictfinal = organizer_instance.fulldict
#print(tree.pretty())

def triplos_rel(dictfinal):
    triplos = []
    for section, details in dictfinal.items():
        if 'Factos Importantes' in details:
            for fact in details['Factos Importantes']:
                if "bisneto" in fact:
                    after_bisneto = fact.split("bisneto", 1)[1].strip()
                    triplo_bis = (section,"Bisneto", after_bisneto)
                    triplos.append(triplo_bis)

        if 'Relacoes' in details:
            for rel in details['Relacoes']:
                relation = rel['Relacao']
                main_triplo = (section, relation['Tipo'], relation['Relacionado'])
                triplos.append(main_triplo)
                if 'Subrelacao' in relation:
                    for subrel in relation['Subrelacao']:
                        sub_triplo = (relation['Relacionado'], subrel[0], subrel[1])
                        triplos.append(sub_triplo)
    return triplos

triplos = triplos_rel(dictfinal)
#print(triplos)

relationship_rules = {
    "Bisneto": "Bisavô/Bisavó",
    "Bisavô": "Bisneto",
    "Bisavó": "Bisneto",
    "Neto": "Avô/Avó",
    "Avô": "Neto",
    "Avó": "Neto",
    "Filho": "Pai/Mãe",
    "Pai": "Filho",
    "Mãe": "Filho",
    "Irmao": "Irmao",
    "Conjuge": "Conjuge",
    "Tio": "Sobrinho",
    "Tia": "Sobrinho",
    "Sobrinho": "Tio/Tia",
}

def invert_relationship(triplo):
    person1, relationship, person2 = triplo
    if relationship in relationship_rules:
        reversed_relationship = relationship_rules[relationship]
    else:
        reversed_relationship = f"Reverse-{relationship}"
    return (person2, reversed_relationship, person1)

inverted_triplos = [invert_relationship(triplo) for triplo in triplos]
#print(inverted_triplos)

def json2html(json_data):
    index_html = "<ul>\n"
    body_html = ""

    for key, value in json_data.items():
        # Criar um ID baseado na chave
        section_id = key.replace(" ", "_").replace(":", "_")
        # Adicionar ao índice
        index_html += f'<li><a href="#{section_id}">{key}</a></li>\n'
        # Adicionar conteúdo da seção
        body_html += f'<h2 id="{section_id}">{key}</h2>\n'
        if isinstance(value, dict):
            body_html += process_dict(value)
        elif isinstance(value, list):
            body_html += process_list(value)

    index_html += "</ul>\n"
    return index_html, body_html

def process_dict(data, level=3):
    html = ""
    for key, value in data.items():
        if key in {"Texto"}:
            texto = ' '.join(value) if isinstance(value, list) else value
            texto = re.sub(r'-','\n-',texto)
            html += f"<h{level}>{key}</h{level}>\n<p>{texto}</p>\n"
        else:
            html += f"<h{level}>{key}</h{level}>\n"
            if isinstance(value, dict):
                html += process_dict(value, level + 1)
            elif isinstance(value, list):
                html += process_list(value, level + 1)
            else:
                html += f"<p>{value}</p>\n"
    return html

def process_list(data, level=3):
    html = "<ul>\n"
    for item in data:
        if isinstance(item, dict):
            html += f"<li>{process_dict(item, level + 1)}</li>\n"
        else:
            html += f"<li>{item}</li>\n"
    html += "</ul>\n"
    return html

index_html, body_html = json2html(dictfinal)
html_content = (
    "<!DOCTYPE html>\n<html>\n<head>\n<meta charset='UTF-8'>\n"
    "<title>Dados em HTML com Índice</title>\n</head>\n<body>\n"
    "<h1>Índice</h1>\n"
    f"{index_html}<hr>\n{body_html}</body>\n</html>"
)

with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
