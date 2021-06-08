import transformers
from transformers import pipeline
import re
from wordcloud import STOPWORDS, WordCloud
from argparse import ArgumentParser, Namespace
from decimal import Decimal
import requests
import pandas as pd
import matplotlib.pyplot as plt
resultados=""
model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
nlp = pipeline("question-answering", model=model_name)
parser = ArgumentParser("Squad portugues")
parser.add_argument("--questao",
                        required=True,
                        help="Digite aqui a pergunta.")
parser.add_argument("--precisao",
                        required=True,
                        help="digite aqui a precisão de tolerância, algo como 0.5 ou 0.7 algo assim.")
args = parser.parse_args()
STOPWORDS = ['ver','principal','essa','vez','nas','mas','qual','principal','ele','ter','doença','pois','este','vez','ver principal','artigo principal','já','aos','pode','outro','artigo','desse','alguns','meio','entre','das','podem','esse','seu','também','são','quando','de', 'que','em','os','as','da','como','dos','ou','se','um','uma','para','na','ao','mais','por','não','ainda','muito','sua'] + list(STOPWORDS)
def parseHbibonlineHtml2txt(siglivro,cap,de,ate):
    if len(ate)>0:
        ate="-"+ate
    #print("https://www.bibliaonline.com.br/nvi/"+siglivro+"/"+cap+"/"+de+ate)
    
    response = requests.post("https://www.bibliaonline.com.br/acf/"+siglivro+"/"+cap+"/"+de+ate)#,headers=my_headers,json=my_body)
    conteudo = response.text.split("<div class=\"jss32 jss27\">")[1].split("<div class=\"jss39 jss28\">")[0]
    conteudo=re.sub('<[^>]+?>', '', conteudo)
    conteudo=re.sub('\&(lt|gt|quot)\;', '', conteudo)
    
    conteudo=re.sub(r'\d', '', conteudo)
    return conteudo

def resposta(questao, conteudo,identificador):
    percentual =Decimal(args.precisao)
    result = nlp(question=questao, context=conteudo)
    if round(result['score'], 4)>percentual:
        posfinalstart = result['start']-30
        posfinalfim=result['end']+30
        conteudo2 = re.sub(r'\n','',conteudo[posfinalstart:posfinalfim])
        print(f"{identificador}: \t\t-->*'{result['answer']}'*\t\t, score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']} \n\t(...{conteudo2}...)\n")
        return [result['answer'].strip() , round(result['score']*10)];
    else:
        return "",0
def extraicapitulo(coluna):
    valor=coluna.split(":")[0]
    return valor.strip()
def extraiverp1(coluna):
    valor=coluna.split(":")[1].split("-")[0]
    return valor.strip()
def extraiverp2(coluna):
    valor=coluna.split(":")[1]
    parte = valor.split("-")
    if len(parte)>1:
        valor= parte[1]
    else:
        valor=""
   
    return valor.strip()
f = open('passagensEv.csv', encoding="utf8")
texto = f.read()
linhas=texto.split("\n")

for i in range(1,len(linhas)): #30):
    
    content=""
    linha = linhas[i]
    coluna = linha.split(";")
    if len(coluna[3]) !=0:
        content = content+"\n"+parseHbibonlineHtml2txt("mt",extraicapitulo(coluna[3]),extraiverp1(coluna[3]),extraiverp2(coluna[3]))
    if len(coluna[4]) !=0:
        content = content+"\n"+parseHbibonlineHtml2txt("mc",extraicapitulo(coluna[4]),extraiverp1(coluna[4]),extraiverp2(coluna[4]))
    if len(coluna[5]) !=0:
        content =content+"\n"+parseHbibonlineHtml2txt("lc",extraicapitulo(coluna[5]),extraiverp1(coluna[5]),extraiverp2(coluna[5]))
    if len(coluna[6]) !=0:
        content =content+"\n"+parseHbibonlineHtml2txt("jo",extraicapitulo(coluna[6]),extraiverp1(coluna[6]),extraiverp2(coluna[6]))     
    #print(coluna[0] + " - " + coluna[1])
    
    f = open("acf/"+coluna[0] + "-" + re.sub('[^\w\s]', '', coluna[1]), "w")
    f.write(content)
    f.close()
    
    question = args.questao 
    #try:
    retorno, score = resposta(question,content,coluna[0] + " - " + coluna[1])
    #print('*'+str(score))
    for j in range(0,score):
        retorno= retorno + " "+ retorno
    
    resultados = resultados +" "+ retorno
    #except:
     #   print("An exception occurred")

wc = WordCloud(stopwords=STOPWORDS,background_color="white", max_words=2000,
               max_font_size=256,
               random_state=42, width=1000, height=1000,collocations=False)
wc.generate(resultados) #ajuste do tamanho das palavras
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
plt.show()