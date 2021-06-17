import transformers
from transformers import pipeline
import re
from wordcloud import STOPWORDS, WordCloud
from argparse import ArgumentParser, Namespace
from decimal import Decimal
import requests
import os
import matplotlib.pyplot as plt

resultados = ""
model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
nlp = pipeline("question-answering", model=model_name)
parser = ArgumentParser("downloader portugues")

parser.add_argument("--versao",
                    required=True,
                    help="por enquanto acf ou nvi.")
args = parser.parse_args()
versao = args.versao
textointeiro = ""

if os.path.isdir("biblia"):
    print("diretorio biblia existe.")
else:
    os.mkdir("biblia")
if os.path.isdir("biblia\\"+versao):
    print("biblia\\"+versao+" existe.")
else:
    os.mkdir("biblia\\"+versao)

def getCapitulo(siglivro, cap):

    # print("https://www.bibliaonline.com.br/"+versao+"/"+siglivro+"/"+cap+"/"+de+ate)

    response = requests.post(
        "https://www.bibliaonline.com.br/" + versao + "/" + siglivro + "/" + cap )  # ,headers=my_headers,json=my_body)
    parte1=response.text.split("<div class=\"jss40\">")[1].split("</div>")[0]
    if "MuiTypography-root" in parte1:
        conteudo=parte1.split("MuiTypography-root")[0]+">"
    else:
        conteudo = parte1

    #conteudo = response.text.split("<div class=\"jss40\">")[1].split("</div>")[0]

    conteudo = re.sub(r'<sup[^>]+?>\d+', '\n', conteudo)
    conteudo = re.sub('<[^>]+?>', '', conteudo)
    conteudo = re.sub('\&(lt|gt|quot)\;', '', conteudo)
    conteudo = re.sub(r'\r\n', '\n', conteudo)
    while '  ' in conteudo:
        conteudo = re.sub(r'  ', ' ', conteudo)
    while '\n\n' in conteudo:
        conteudo = re.sub(r'\n\n', '\n', conteudo)
    while '\r\n\r\n' in conteudo:
        conteudo = re.sub(r'\r\n\r\n', '\n', conteudo)
    conteudo = re.sub(r'\n ', '\n', conteudo)
    conteudo = re.sub(r'^\n', '\n', conteudo)
    conteudo = re.sub(r'^\r\n', '\n', conteudo)
    return conteudo


f = open('livrosbiblia.txt')
texto = f.read()
linhas = texto.split("\n")
f.close()
for i in range(0, len(linhas)):  # 30):

    content = ""
    linha = linhas[i]
    coluna = linha.split("\t")
    for j in range(1,int(coluna[2])+1):
        try:
            if os.path.isdir("biblia\\" + versao+"\\"+coluna[1]):
                print("biblia\\" + versao+"\\"+coluna[1] + " existe.")
            else:
                os.mkdir("biblia\\" + versao+"\\"+coluna[1])
            f = open("biblia" + "/" + versao + "/" + coluna[1] + "/"+str(j)+".txt", "r") #vai dar errado, apenas para descer por enquanto, preciso decidir como fazer isso
            content = f.read()
            conteudo = re.sub(r'’|“|‘|”', '', content)
            conteudo = re.sub(r'\d', '', conteudo)
            conteudo = re.sub(r'\n\.', '\n', conteudo)
            conteudo = re.sub(r'\n ', '\n', conteudo)
            conteudo = re.sub(r'\r\n', '\n', conteudo)
            content = re.sub(r'\n\n', '\n', conteudo)
            f.close()
        except:

            try:
                conteudo = getCapitulo(coluna[1],str(j))
                print (conteudo)
                fg = open("biblia" + "/" + versao + "/" + coluna[1] + "/"+str(j)+".txt", "w")
                print("----------")
                fg.write(conteudo)
                fg.close()
            except:
                print("pulou1")