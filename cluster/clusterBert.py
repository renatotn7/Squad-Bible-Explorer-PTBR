from argparse import ArgumentParser
from collections import defaultdict
import os
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
from transformers import  BertForNextSentencePrediction
from sentence_transformers import SentenceTransformer, util

#Python program to print topological sorting of a DAG
from collections import defaultdict

#Class to represent a graph


parser = ArgumentParser("Cluster Evangelhos")

parser.add_argument("--versao",
                    required=True,
                    help="por enquanto acf ou nvi.")
args = parser.parse_args()
versao = args.versao


#This code is contributed by Neelam Yadav


model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

#kiri-ai/distiluse-base-multilingual-cased-et
listtextos=[]
f = open('passagensEv.csv', encoding="utf8")
texto = f.read()
linhas = texto.split("\n")
f.close()
for i in range(1, len(linhas)):  # 30):

    content = ""
    linha = linhas[i]
    coluna = linha.split(";")

    f = open("evangCruzados" + "/" + versao + "/" + coluna[0] + "-" + re.sub('[^\w\s]', '', coluna[1]), "r")
    nome=re.sub('[^\w\s]', '', coluna[1])
    content = f.read()
    conteudo = re.sub(r'’|“|‘|”', '', content)
    conteudo = re.sub(r'\d', '', conteudo)
    conteudo = re.sub(r'\n\.', '\n', conteudo)
    conteudo = re.sub(r'\n ', '\n', conteudo)
    conteudo = re.sub(r'\r\n', '\n', conteudo)

    while '  ' in conteudo:
        conteudo = re.sub(r'  ', ' ', conteudo)
    content = re.sub(r'\n\n', '\n', conteudo)
    listtextos.append (f"{nome.strip()}-{content}")
    f.close()



from bertopic import BERTopic

topic_model = BERTopic(embedding_model=model, calculate_probabilities=True, verbose=True)
topics, probs = topic_model.fit_transform(listtextos)
cv = CountVectorizer(ngram_range=(1, 3))

topic_model.update_topics(  listtextos, topics,vectorizer_model=cv)

freq = topic_model.get_topic_info();
print(freq)

#topic_model.visualize_topics()
#topic_model.visualize_distribution(probs[200], min_probability=0.015)
#topic_model.visualize_hierarchy(top_n_topics=50)
#topic_model.visualize_barchart(top_n_topics=5)
#topic_model.visualize_heatmap(n_clusters='15', width=1000, height=1000)
#topic_model.visualize_term_rank()
similar_topics, similarity = topic_model.find_topics("pilatos", top_n=5)
print (similar_topics)
print (topic_model.get_topic(49))