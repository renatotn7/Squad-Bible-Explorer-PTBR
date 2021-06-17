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

try:
    fg = open("48-Dois endemoninhados gadarenos Os.graph","r")
    print("1")
    proximdadePorContexto=fg.read()
    print("2")
    fg.close();
    encontrougraphfile = True
except:


    if encontrougraphfile==False:


        for la in range(0, len(linhas)):
            linha:str = linhas[la]
            frasesa: Any = nltk.sent_tokenize(linha, language='portuguese')
            for frasea in frasesa:
                for lb in range(0, len(linhas)):
                    linhab:str = linhas[lb]
                    frasesb:Any = nltk.sent_tokenize(linhab, language='portuguese')
                    encontroumatchb:bool = False
                    for fraseb in frasesb:
                        achou:bool = False
                        for i in range(0, len(encontradosa)):
                            if encontradosa[i] == fraseb + str(lb) and encontradosb[i] == frasea + str(la):
                                achou = True
                                break
                        if fraseb + str(lb) == frasea + str(la):
                            achou = True

                        if achou == False:

                            sentences = [frasea, fraseb]

                            paraphrases = util.paraphrase_mining(model, sentences)

                            for paraphrase in paraphrases[0:10]:
                                score, i, j = paraphrase
                                proximdadePorContexto+=f"{frasea}\t{fraseb}\t{str(score)}\n"
                                sys.stdout.write('.')
                                encontradosa.append(frasea + str(la))
                            encontradosb.append(fraseb + str(lb))
                    if encontroumatchb == False:

                        if frasea not in jainseridos and frasea not in jainseridosmatched:
                            textonaorepetidofinala.append(frasea)
                            textonaorepetidofinal = textonaorepetidofinal + frasea
                            jainseridos.append(frasea)
        fg = open("48-Dois endemoninhados gadarenos Os.graph", "w")
        print("----------")
        fg.write(proximdadePorContexto)
        fg.close()
linhasgr = proximdadePorContexto.split("\n")

for la in range(0, len(linhasgr)):
    linha = linhasgr[la]
    colunas = linha.split("\t")

    encontroumatchb = False
   #for lc in range(0, len(colunas)):
   # coluna = colunas[lc]
    #print(colunas)
    
    if(la==1431):
        print(colunas)
    frasea = colunas[0]
    fraseb = colunas[1]
    score = colunas[2]
    if (float(score) > 0.73):

        encontroumatch = True
        print("frase a : " + " - " + frasea + "... frase b: - " + fraseb + "..." + "Score: {:.4f}".format(float(score)))
        jainseridosmatched.append(frasea)
        jainseridosmatched.append(fraseb)
        textorepetidofinala.append(frasea)
        textorepetidofinala.append(fraseb)
        if len(frasea) > len(fraseb):
            if textorepetidofinal.find(frasea) == -1:
                textorepetidofinal = textorepetidofinal + " " + frasea
                textorepetidoverificacao.append(frasea)
                listadicionario[fraseb.strip()] =frasea

        else:
            if textorepetidofinal.find(fraseb) == -1:
                textorepetidofinal = textorepetidofinal + " " + fraseb
                textorepetidoverificacao.append(fraseb)
                listadicionario[frasea.strip()] = fraseb

        listadicionariocode[frasea.strip()] = countadded
        listadicionariocode[fraseb.strip()] = countadded
        countadded += 1
    if encontroumatchb == False:

        if frasea not in jainseridos and frasea not in jainseridosmatched:
            textonaorepetidofinala.append(frasea)
            textonaorepetidofinal = textonaorepetidofinal + frasea
            jainseridos.append(frasea)

for key, value in listadicionariocode.items():
    print(key+" "+str(value))
print("----------")
for frase1 in textorepetidoverificacao:
    for frase2 in textorepetidoverificacao:

        sentences = [frase1, frase2]

        paraphrases = util.paraphrase_mining(model, sentences)

        for paraphrase in paraphrases[0:10]:
            score, i, j = paraphrase
            if (score > 0.7):
                print(
                    "****frase 1 : " + " - " + frase1 + "... frase 2: " + " - " + frase2 + "..." + "Score: {:.4f}".format(
                        score))
                if len(frase1) > len(frase2):
                    textorepetidoverificacao.remove(frase2)
                   # listadicionariocode[frase2]=listadicionariocode.get(frase1)
                  #  listadicionariocode.remove()
                else:
                    textorepetidoverificacao.remove(frase1)
                   # listadicionariocode[frase1] = listadicionariocode.get(frase2)


textofiltrado=""
for frase1 in textorepetidoverificacao:
    textofiltrado = textofiltrado + "|" + frase1

print("----------")
print(context + str(len(context)))
print("----------")
print()
print(textofiltrado + str(len(textofiltrado)))
print()
conteudofinal = ""
for sent in textonaorepetidofinala:
    if sent not in textorepetidofinala:
        conteudofinal = conteudofinal + " " + sent
print(conteudofinal + str(len(conteudofinal)))
percentualdoinicial = ((len(textofiltrado) + len(conteudofinal)) / len(context)) * 100
print("reducaofinal:" + str(100 - percentualdoinicial))
#'linha' 'destino' 'ponto'
#for la in range(0, len(linhas)):
#    linha = linhas[la]
#    frasesa = nltk.sent_tokenize(linha, language='portuguese')

#    for lf in range(0, len( frasesa)):
#        code = ''
#        textocode = ''
#        frasea =frasesa[lf]
#        if ""==listadicionario.get(frasea, ""):

#           textocode = str(la)+' 80'+ str(la)+ str(lf)  +' ' +  str(lf)
#        else:
#            textocode = str(la) + ' 90' + str(listadicionariocode.get(frasea)) +' ' +  str(lf)
#        print (textocode)
        #print(frasea + " -> " + listadicionario.get(frasea, ""))
listacodesadicionados=[]
countrepetidosusados=0
g= Graph()
contedges=1
dicionariografo={}
for la in range(0, len(linhas)):
    linha = linhas[la]
    frasesa = nltk.sent_tokenize(linha, language='portuguese')
#1 if True else 2
    listacodesadicionados = []
    for lf in range(0, len( frasesa)):
        code = ''
        textocode = ''
        frasea =frasesa[lf]
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
        print (f'{str(listacodesadicionados[(lf-1)]) if len(listacodesadicionados) else "00000"}\t{textocode}\t"{textocode}"\t"{listadicionario.get(frasea, frasea)}"')
        listacodesadicionados.append(textocode)
        dicionariografo[textocode]=f'{listadicionario.get(frasea, frasea)}'
        #print(frasea + " -> " + listadicionario.get(frasea, ""))
print("----------")
g.topologicalSort()

dicionariografo
listadelinhasgrafoconsolidado:list[str]=[]
for key, value in dicionariografo.items():
    print(f'{key} {dicionariografo[key]}')
    listadelinhasgrafoconsolidado.append(dicionariografo[key])

for key, value in listadicionariocode.items():
    print(key+" "+str(value))
print("----------")
#https://towardsdatascience.com/topic-modeling-with-bert-779f7db187e6

embeddings = model.encode(listadelinhasgrafoconsolidado, show_progress_bar=True)
umap_embeddings = umap.UMAP(n_neighbors=5,
                            n_components=2,
                            metric='cosine').fit_transform(embeddings)
cluster = hdbscan.HDBSCAN(min_cluster_size=2,
                          metric='euclidean',
                          cluster_selection_method='eom').fit(umap_embeddings)

import matplotlib.pyplot as plt
import pandas as pd
# Prepare data
umap_data = umap.UMAP(n_neighbors=15, n_components=2, min_dist=0.0, metric='cosine').fit_transform(embeddings)
result = pd.DataFrame(umap_data, columns=['x', 'y'])
result['labels'] = cluster.labels_

# Visualize clusters
#fig, ax = plt.subplots(figsize=(20, 10))
#outliers = result.loc[result.labels == -1, :]
#clustered = result.loc[result.labels != -1, :]
#plt.scatter(outliers.x, outliers.y, color='#BDBDBD', s=0.05)
#plt.scatter(clustered.x, clustered.y, c=clustered.labels, s=0.05, cmap='hsv_r')
#plt.colorbar()
#plt.show()
print('tam:'+ str(len(listadelinhasgrafoconsolidado)))

docs_df = pd.DataFrame(listadelinhasgrafoconsolidado, columns=["Doc"])
docs_df['Topic'] = cluster.labels_
docs_df['Doc_ID'] = range(len(docs_df))
docs_per_topic = docs_df.groupby(['Topic'], as_index = False).agg({'Doc': ' '.join})

print(docs_per_topic)


def c_tf_idf(documents, m, ngram_range=(1, 1)):
    count = CountVectorizer(ngram_range=ngram_range, stop_words="english").fit(documents)
    t = count.transform(documents).toarray()
    w = t.sum(axis=1)
    tf = np.divide(t.T, w)
    sum_t = t.sum(axis=0)
    idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
    tf_idf = np.multiply(tf, idf)

    return tf_idf, count


tf_idf, count = c_tf_idf(docs_per_topic.Doc.values, m=len(listadelinhasgrafoconsolidado))

def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=20):
    words = count.get_feature_names()
    labels = list(docs_per_topic.Topic)
    tf_idf_transposed = tf_idf.T
    indices = tf_idf_transposed.argsort()[:, -n:]
    top_n_words = {label: [(words[j], tf_idf_transposed[i][j]) for j in indices[i]][::-1] for i, label in enumerate(labels)}
    return top_n_words

def extract_topic_sizes(df):
    topic_sizes = (df.groupby(['Topic'])
                     .Doc
                     .count()
                     .reset_index()
                     .rename({"Topic": "Topic", "Doc": "Size"}, axis='columns')
                     .sort_values("Size", ascending=False))
    return topic_sizes

top_n_words = extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=20)
topic_sizes = extract_topic_sizes(docs_df); topic_sizes.head(10)

print(topic_sizes)
print(top_n_words[0])
print(docs_df)
print(docs_df.loc[(docs_df['Topic']==1)])
