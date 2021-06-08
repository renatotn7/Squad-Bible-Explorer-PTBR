import transformers
from transformers import pipeline
import re
from argparse import ArgumentParser, Namespace
from decimal import Decimal
percentual = 0.8
parser = ArgumentParser("Squad portugues")
parser.add_argument("--questao",
                        required=True,
                        help="Digite aqui a pergunta.")
parser.add_argument("--precisao",
                        required=True,
                        help="digite aqui a precisão de tolerância, algo como 0.5 ou 0.7 algo assim.")
args = parser.parse_args()

percentual =Decimal(args.precisao)
model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
nlp = pipeline("question-answering", model=model_name)

# source: https://pt.wikipedia.org/wiki/Pandemia_de_COVID-19
mylist = ["Mateus1p1", "Mateus1p2", "Mateus2p1", "Mateus2p2", "Mateus2p3","Mateus3p1", "Mateus3p2","Mateus4p1", "Mateus4p2","Mateus5p1","Mateus5p2", "Mateus5p3",
           "Mateus6p1","Mateus6p2","Mateus7p1","Mateus7p2","Mateus7p3","Mateus7p4","Mateus7p5","Mateus7p6","Mateus7p7",
           "Mateus8p1","Mateus8p2","Mateus8p3","Mateus8p4","Mateus8p5","Mateus8p6","Mateus9p1","Mateus9p2","Mateus9p3","Mateus9p4","Mateus9p5","Mateus9p6",'Mateus10p1',
           'Mateus11p1','Mateus11p2','Mateus11p3',"Mateus12p1","Mateus12p2","Mateus12p3","Mateus12p4","Mateus12p5","Mateus12p6","Mateus13p1","Mateus13p2","Mateus13p3",
           "Mateus13p4","Mateus13p5","Mateus14p1","Mateus14p2","Mateus14p3"]
           
print ('*Mateus ->  Judeus\n')
for filename in mylist:
    f = open(filename, encoding="utf8")
    conteudo = re.sub(r'’|“|‘|”','',f.read())
    conteudo = re.sub(r'\d','',conteudo)
    conteudo = re.sub(r'\n\.','\n',conteudo)
    conteudo = re.sub(r'\n ','\n',conteudo)
    conteudo = re.sub(r'\r\n','\n',conteudo)
    conteudo = re.sub(r'\n\n','\n',conteudo)

    #print(conteudo)
    context = conteudo
    f.close()

    question = args.questao #"Quem é Jesus?"

    result = nlp(question=question, context=context)
    if round(result['score'], 4)>percentual:
        posfinalstart = result['start']-30
        posfinalfim=result['end']+30
        conteudo2 = re.sub(r'\n','',conteudo[posfinalstart:posfinalfim])
        print(f"{filename}: \t\t-->*'{result['answer']}'*\t\t, score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']} \n\t(...{conteudo2}...)\n")

# Answer: '1 de dezembro de 2019', score: 0.713, start: 328, end: 349
mylist = ["Joao1p1", "Joao1p2", "Joao1p3","Joao2p1", "Joao2p2","Joao3p1", "Joao3p2","Joao4p1", "Joao4p2", "Joao4p3", "Joao5p1", "Joao5p2"]
print ('*João ->  Igreja\n')
for filename in mylist:
    f = open(filename, encoding="utf8")
    conteudo = re.sub(r'’|“|‘|”','',f.read())
    conteudo = re.sub(r'\d','',conteudo)
    conteudo = re.sub(r'\n\.','\n',conteudo)
    conteudo = re.sub(r'\n ','\n',conteudo)
    conteudo = re.sub(r'\r\n','\n',conteudo)
    conteudo = re.sub(r'\n\n','\n',conteudo)

    #print(conteudo)
    context = conteudo
    f.close()

    question = args.questao #"Quem é Jesus?"

    result = nlp(question=question, context=context)
    if round(result['score'], 4)>percentual:
        posfinalstart = result['start']-30
        posfinalfim=result['end']+30
        conteudo2 = re.sub(r'\n','',conteudo[posfinalstart:posfinalfim])
        print(f"{filename}: \t\t-->*'{result['answer']}'*\t\t, score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']} \n\t(...{conteudo2}...)\n")


mylist = ["Marcos1p1", "Marcos1p2", "Marcos1p3","Marcos1p4", "Marcos1p5","Marcos1p6","Marcos2p1", "Marcos2p2", "Marcos2p3","Marcos2p4",
"Marcos3p1", "Marcos3p2", "Marcos3p3","Marcos3p4","Marcos3p5",
"Marcos4p1", "Marcos4p2", "Marcos4p3","Marcos4p4","Marcos4p5","Marcos5p1", "Marcos5p2"]
print ('*Marcos ->  Romanos\n')
for filename in mylist:
    f = open(filename, encoding="utf8")
    conteudo = re.sub(r'’|“|‘|”','',f.read())
    conteudo = re.sub(r'\d','',conteudo)
    conteudo = re.sub(r'\n\.','\n',conteudo)
    conteudo = re.sub(r'\n ','\n',conteudo)
    conteudo = re.sub(r'\r\n','\n',conteudo)
    conteudo = re.sub(r'\n\n','\n',conteudo)

    #print(conteudo)
    context = conteudo
    f.close()

    question = args.questao #"Quem é Jesus?"

    result = nlp(question=question, context=context)
    if round(result['score'], 4)>percentual:
        posfinalstart = result['start']-30
        posfinalfim=result['end']+30
        conteudo2 = re.sub(r'\n','',conteudo[posfinalstart:posfinalfim])
        print(f"{filename}: \t\t-->*'{result['answer']}'*\t\t, score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']} \n\t(...{conteudo2}...)\n")




mylist = ["Lucas1p1", "Lucas1p2", "Lucas1p3","Lucas1p4", "Lucas1p5", "Lucas1p6",
          "Lucas2p1", "Lucas2p2", "Lucas2p3","Lucas2p4", "Lucas2p5",
          "Lucas3p1", "Lucas3p2", "Lucas3p3",
          "Lucas4p1", "Lucas4p2", "Lucas4p3","Lucas4p4"]
print ('*Lucas ->  Gentios\n')
for filename in mylist:
    f = open(filename, encoding="utf8")
    conteudo = re.sub(r'’|“|‘|”','',f.read())
    conteudo = re.sub(r'\d','',conteudo)
    conteudo = re.sub(r'\n\.','\n',conteudo)
    conteudo = re.sub(r'\n ','\n',conteudo)
    conteudo = re.sub(r'\r\n','\n',conteudo)
    conteudo = re.sub(r'\n\n','\n',conteudo)

    #print(conteudo)
    context = conteudo
    f.close()

    question = args.questao #"Quem é Jesus?"

    result = nlp(question=question, context=context)
    if round(result['score'], 4)>percentual:
        posfinalstart = result['start']-30
        posfinalfim=result['end']+30
        conteudo2 = re.sub(r'\n','',conteudo[posfinalstart:posfinalfim])
        print(f"{filename}: \t\t-->*'{result['answer']}'*\t\t, score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']} \n\t(...{conteudo2}...)\n")
