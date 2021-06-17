from collections import defaultdict
import re
import umap
import hdbscan
from typing import Any
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from utils.regex_clean_bib_files import regex_clean_file
from utils.GraphSentencesNLP import Graph
import sys
import nltk
from sentence_transformers import SentenceTransformer, util

#Python program to print topological sorting of a DAG
from collections import defaultdict

#Class to represent a graph





#This code is contributed by Neelam Yadav


model = SentenceTransformer('distiluse-base-multilingual-cased-v1')


# kiri-ai/distiluse-base-multilingual-cased-et
# tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
nltk.download("punkt")

f = open("48-Dois endemoninhados gadarenos Os")

context=regex_clean_file(f.read())
#conteudo = re.sub(r'’|“|‘|”', '', f.read())
#conteudo = re.sub(r'\d', '', conteudo)
#conteudo = re.sub(r'\n\.', '\n', conteudo)
#conteudo = re.sub(r'\n ', '\n', conteudo)
#conteudo = re.sub(r'\r\n', '\n', conteudo)
#conteudo = re.sub(r'\n\n', '\n', conteudo)

# print(conteudo)
#context = conteudo

f.close()
encontradosa = ['']
encontradosb = ['']
jainseridos = []
jainseridosmatched = []
textorepetidofinal = ""
textonaorepetidofinal = ""
textonaorepetidofinala = []
textorepetidofinala = []
textorepetidoverificacao = []
linhas = context.split("\n")
listadicionario = dict()
listadicionariocode = dict()
countadded=0
proximdadePorContexto=""
encontrougraphfile=False

parafrases=[]
frasesretorno = []
def tokenisealem(frasesa):
    retornos = []

    for frasea in frasesa:
        subfrases = []
        if ";" in frasea:
            subfrases = frasea.split(";")
            countfrasesreais = 0

            for i in range(0, len(subfrases) - 1):

                retornos.append(subfrases[i] + ";")
            retornos.append(subfrases[len(subfrases) - 1])

        elif ":" in frasea:
            subfrases = frasea.split(":")

            for i in range(0, len(subfrases) - 1):
                retornos.append(subfrases[i] + ":")
            retornos.append(subfrases[len(subfrases) - 1])
        else:
            retornos.append(frasea)
    return retornos

def getParafrases(linhas):
    retorno=[]
    for la in range(0, len(linhas)):

        linha: str = linhas[la]
        frasesa: Any = nltk.sent_tokenize(linha, language='portuguese')
        if len(frasesa) == 0:
            continue
        frasesa = tokenisealem(frasesa)

        for frasea in frasesa:
            retorno.append(frasea)
            sys.stdout.write('.')

    paraphrases = util.paraphrase_mining(model, retorno)
    return paraphrases, retorno

paraphrases, frasesretorno=    getParafrases(linhas)
for paraphrase in paraphrases:
    score, i, j = paraphrase
    if (float(score) > 0.75):
       if len(frasesretorno[i])>len(frasesretorno[j]):#crossover
           frasesretorno[j]=frasesretorno[i]

       else:
           frasesretorno[i] = frasesretorno[j]

paraphrases, frasesretorno=    getParafrases(frasesretorno)

for paraphrase in paraphrases:
    score, i, j = paraphrase
    if (float(score) > 0.75):
       if len(frasesretorno[i])>len(frasesretorno[j]):#crossover
           frasesretorno[j]=frasesretorno[i]
           listadicionariocode[frasesretorno[i].strip()] = i
       else:
            frasesretorno[i] = frasesretorno[j]
            listadicionariocode[frasesretorno[j].strip()] = j


for key, value in listadicionariocode.items():
    print('--'+key+" "+str(value))


print("----------")
for la in range(0, len(frasesretorno)):
    linha = frasesretorno[la]
    print(linha)
print("----------")
listacodesadicionados=[]
countrepetidosusados=0
g= Graph()
contedges=1
dicionariografo={}
for la in range(0, len(frasesretorno)):
    linha = frasesretorno[la]
    frasesa = nltk.sent_tokenize(linha, language='portuguese')
#1 if True else 2
    listacodesadicionados = []
    for lf in range(0, len( frasesretorno)):
        code = ''
        textocode = ''
        frasea =frasesretorno[lf]
        if len(str(listadicionariocode.get(frasea.strip(), "")))==0:

            textocode =  f'{str(la)}8{str(lf).zfill(3)}' # {str(lf).zfill(3)}' # {lf}' #str((lf/len( frasesa))*10)
        else:
            #print (listadicionariocode.get(frasea))
            textocode = f'09{str(listadicionariocode.get(frasea.strip())).zfill(3)}'#{str(lf).zfill(3)}'
           # textocode = str(la) + ' 90' + str(
             #listadicionariocode.get(frasea.strip())) + ' ' + lf  # str((lf/len( frasesa))*10)
            #textocode = str(la) + ' 90' + str(listadicionariocode.get(frasea.strip())) +' ' +  lf #str((lf/len( frasesa))*10)
       # print(textocode)
        contedges+=1
        g.addEdge(int(str(listacodesadicionados[(lf-1)]) if len(listacodesadicionados) else "00000"), int(textocode));
#        print (f'{str(listacodesadicionados[(lf-1)]) if len(listacodesadicionados) else "00000"}\t{textocode}\t"{textocode}"\t"{listadicionario.get(frasea, frasea)}"')
        listacodesadicionados.append(textocode)
        dicionariografo[textocode]=f'{listadicionario.get(frasea, frasea)}'
        #print(frasea + " -> " + listadicionario.get(frasea, ""))
print("----------")
stack = g.topologicalSort()


listadelinhasgrafoconsolidado:list[str]=[]
for key, value in dicionariografo.items():
    print(f'{key} -> {dicionariografo[key]}')
    listadelinhasgrafoconsolidado.append(dicionariografo[key])

#for key, value in listadicionariocode.items():
#    print(key+" "+str(value))
print("----------")
print("----------")
