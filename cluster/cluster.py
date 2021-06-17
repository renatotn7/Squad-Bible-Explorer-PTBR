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


embeddings = model.encode(listtextos, show_progress_bar=True)
umap_embeddings = umap.UMAP(n_neighbors=15,
                            n_components=5,
                            metric='cosine').fit_transform(embeddings)
cluster = hdbscan.HDBSCAN(min_cluster_size=5,
                          metric='euclidean',
                          cluster_selection_method='eom').fit(umap_embeddings)

import matplotlib.pyplot as plt
import pandas as pd
# Prepare data
umap_data = umap.UMAP(n_neighbors=15, n_components=2, min_dist=0.0, metric='cosine').fit_transform(embeddings)
result = pd.DataFrame(umap_data, columns=['x', 'y'])
result['labels'] = cluster.labels_

# Visualize clusters
fig, ax = plt.subplots(figsize=(20, 10))
outliers = result.loc[result.labels == -1, :]
clustered = result.loc[result.labels != -1, :]
plt.scatter(outliers.x, outliers.y, color='#BDBDBD', s=1)
plt.scatter(clustered.x, clustered.y, c=clustered.labels, s=1, cmap='hsv_r')
plt.colorbar()
plt.show()
print('tam:'+ str(len(listtextos)))

docs_df = pd.DataFrame(listtextos, columns=["Doc"])
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


tf_idf, count = c_tf_idf(docs_per_topic.Doc.values, m=len(listtextos))

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
pd.set_option('display.max_colwidth', None)
clear = lambda: os.system('cls')
inpt = "0"
while inpt!= "sair":
    if inpt=='':
        inpt="0"
    print(topic_sizes)
    print(top_n_words[int(inpt)])
    docfinal = docs_df.loc[(docs_df['Topic'] == int(inpt))]
    print(docfinal['Doc'])
    inpt = input("value ")
    clear()
clear()

from bertopic import BERTopic

topic_model = BERTopic(embedding_model=model, calculate_probabilities=True, verbose=True,nr_topics=20)
topics, probs = topic_model.fit_transform(listtextos)


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