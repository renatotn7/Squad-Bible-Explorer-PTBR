import joblib
import transformers
import pickle
from transformers import pipeline,BertForTokenClassification, DistilBertTokenizerFast,BertModel, BertTokenizer,AutoModelForPreTraining
from transformers import AutoTokenizer,AutoModel,AutoModelForMaskedLM
import re
from wordcloud import STOPWORDS, WordCloud
from argparse import ArgumentParser, Namespace
from decimal import Decimal

import requests
from sklearn.feature_extraction.text import CountVectorizer
from _bertopic import BERTopic
import matplotlib.pyplot as plt
import sys
import nltk
from transformers import  BertForNextSentencePrediction
from alive_progress import alive_bar

from nltk import pos_tag,word_tokenize
from sentence_transformers import SentenceTransformer, util
from collections import defaultdict
model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
resultados=""
model_name = 'pierreguillou/bert-base-cased-squad-v1.1-portuguese'
nltk.download('averaged_perceptron_tagger')

#modelner = BertForTokenClassification.from_pretrained('./bertimbau-base_bert-crf_selective')
#tokenizerner = BertTokenizer.from_pretrained('neuralmind/bert-large-portuguese-cased', do_lower_case=False)
#tag_encoderner = NERTagsEncoder.from_label_file("./bertimbau-base_bert-crf_selective/classes.txt","BIO")






nlp = pipeline("question-answering", model=model_name)
parser = ArgumentParser("Squad portugues")
parser.add_argument("--questao",
                        required=True,
                        help="Digite aqui a pergunta.")
parser.add_argument("--precisao",
                        required=True,
                        help="digite aqui a precisão de tolerância, algo como 0.5 ou 0.7 algo assim.")
                        
parser.add_argument("--versao",
                        required=True,
                        help="por enquanto acf ou nvi.")
args = parser.parse_args()
versao=args.versao
#questaoner=nlpner(args.questao)
#print(questaoner)
folder = 'nltkpostagger/'
teste_tagger = joblib.load(folder+'POS_tagger_brill.pkl')
phrase = 'O rato roeu a roupa do rei de Roma'
print(teste_tagger.tag(word_tokenize(phrase)))
print(pos_tag(word_tokenize(args.questao, language='portuguese')))
percentual = Decimal(args.precisao)
textointeiro=""
STOPWORDS = ['ver','principal','essa','vez','nas','mas','qual','principal','ele','ter','doença','pois','este','vez','ver principal','artigo principal','já','aos','pode','outro','artigo','desse','alguns','meio','entre','das','podem','esse','seu','também','são','quando','de', 'que','em','os','as','da','como','dos','ou','se','um','uma','para','na','ao','mais','por','não','ainda','muito','sua'] + list(STOPWORDS)
listtextos = []
def parseHbibonlineHtml2txt(siglivro,cap,de,ate):
    if len(ate)>0:
        ate="-"+ate
    #print("https://www.bibliaonline.com.br/"+versao+"/"+siglivro+"/"+cap+"/"+de+ate)
    
    response = requests.post("https://www.bibliaonline.com.br/"+versao+"/"+siglivro+"/"+cap+"/"+de+ate)#,headers=my_headers,json=my_body)
    conteudo = response.text.split("<div class=\"jss32 jss27\">")[1].split("<div class=\"jss39 jss28\">")[0]
    conteudo=re.sub('<[^>]+?>', '', conteudo)
    conteudo=re.sub('\&(lt|gt|quot)\;', '', conteudo)
    
    conteudo=re.sub(r'\d', '', conteudo)
    return conteudo

def resposta(questao, conteudo,identificador):
    percentual =Decimal(args.precisao)
    result = nlp(question=questao, context=conteudo)
    posfinalstart = result['start'] - 100
    posfinalfim = result['end'] + 100
    conteudo2 = re.sub(r'\n', '', conteudo[posfinalstart:posfinalfim])
    if round(result['score'], 4)>percentual:

        print(f"{identificador}: \t\t-->*'{result['answer']}'*\t\t, score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']} \n\t(...{conteudo2}...)\n")
        return [result['answer'].strip() , round(result['score']*10)];

    else:
        #sys.stdout.write(f"(boas chances de erro:)\r{identificador}: \t\t-->*'{result['answer']}'*\t\t, score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']} \n\t(...{conteudo2}...)\n")
        #sys.stdout.flush()

        return "",0

def up():
    sys.stdout.write('\x1b[1A')
    sys.stdout.flush()

def down():
    sys.stdout.write('\n')
    sys.stdout.flush()
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

try:
    with alive_bar(4, "Loading modelos") as bar:
        infile = open("topic_modelBiblia", 'rb')
        topic_model = pickle.load(infile)
        infile.close()
        bar("loaded topic_modelBiblia")
        infile = open("topic_modelBiblia2", 'rb')
        topic_model2 = pickle.load(infile)
        infile.close()
        bar("loaded topic_modelBiblia2")
        infile = open("doc_modelBiblia", 'rb')
        doc = pickle.load(infile)
        infile.close()
        bar("loaded doc_modelBiblia")
        infile = open("doc_modelBiblia2", 'rb')
        doc2 = pickle.load(infile)
        infile.close()
        bar("loaded doc_modelBiblia2")
except:
    print("Unexpected error:", sys.exc_info()[0])

    f = open('livrosbiblia.txt')
    texto = f.read()
    linhas = texto.split("\n")
    f.close()

    for i in range(1,len(linhas)): #30):
        linha = linhas[i]
        coluna = linha.split("\t")

        content=""

        try:
            for j in range(1, int(coluna[2]) + 1):



                f = open("biblia"+"/"+versao+"/"+coluna[1] +"/"+str(j)+".txt" , "r")
                conteudo= f.read()

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
                listtextos.append(re.sub(r'^\r\n', '\n', conteudo).strip())
                f.close()
        except:

           print(len(listtextos))

    topic_model = BERTopic(embedding_model=model, calculate_probabilities=True, verbose=True,min_topic_size=3,top_n_words=5)
    topic_model2 = BERTopic(embedding_model=model, calculate_probabilities=True, verbose=True, min_topic_size=3,
                           top_n_words=5)
    topics, probs, doc = topic_model.fit_transform(listtextos)

    dfdoc = doc[doc.Topic.eq(-1)]
    doclist2=[]
    for docitem in dfdoc['Document']:
        doclist2.append(docitem)
    topics2, probs2, doc2 = topic_model2.fit_transform(doclist2)
    #topic_model
    #topic_model.get

    # topic_model.visualize_topics()
    # topic_model.visualize_distribution(probs[200], min_probability=0.015)
    # topic_model.visualize_hierarchy(top_n_topics=50)
    # topic_model.visualize_barchart(top_n_topics=5)
    # topic_model.visualize_heatmap(n_clusters='15', width=1000, height=1000)
    # topic_model.visualize_term_rank()
    #similar_topics, similarity = topic_model.find_topics("pilatos", top_n=5)
    #print(similar_topics)
    filename = 'topic_modelBiblia'
    outfile = open(filename,'wb')
    pickle.dump(topic_model,outfile)
    outfile.close()
    filename = 'topic_modelBiblia2'
    outfile = open(filename, 'wb')
    pickle.dump(topic_model2, outfile)
    outfile.close()
    filename = 'doc_modelBiblia'
    outfile = open(filename, 'wb')
    pickle.dump(doc, outfile)
    outfile.close()
    filename = 'doc_modelBiblia2'
    outfile = open(filename, 'wb')
    pickle.dump(doc2, outfile)
    outfile.close()


##
# {"Document": documents,
#                                  "ID": range(len(documents)),
#                                  "Topic": None}
##

print(type(doc))

#cv = CountVectorizer(ngram_range=(1, 3))

#topic_model.update_topics(listtextos, topics, vectorizer_model=cv)

freq = topic_model.get_topic_info();
print(freq)
freq2 = topic_model2.get_topic_info();
print(freq2)
print(topic_model.get_topic(5))
conteudotodo=""
question = args.questao
topics = topic_model.get_topics()
topics2 = topic_model2.get_topics()
print(topics.keys()) #dict_keys([-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
#print(topics.values())
#print(topics.items())
#print(len(topics))
#print(len(topic_model.get))
dfdoc = doc[doc.Topic.eq(0)]
print(dfdoc.head())
with alive_bar(len(topics.keys()),"Primeira classificação") as bar:

        for i in topics.keys():
            up()
            bar()
            if i == -1:
                continue
            conteudotodo = ""
            dfdoc = doc[doc.Topic.eq(i)]


            for doc1 in dfdoc['Document']:

                conteudotodo= conteudotodo+"\n"+doc1

            retorno, score = resposta(question,conteudotodo,"topico"+" "+str(i))
            if(score>percentual):
                print(str(i) + " top -> "+ str(topic_model.get_topic(i)))

with alive_bar(len(topics2.keys()),"Segunda classificação") as bar:
    for i in topics2.keys():
        bar()
        if i == -1:
            continue
        conteudotodo = ""
        dfdoc = doc2[doc2.Topic.eq(i)]

 #       print(i)
        for doc1 in dfdoc['Document']:
            conteudotodo = conteudotodo + "\n" + doc1

        retorno, score = resposta(question, conteudotodo, "topico2" + " " + str(i))
        if(score>percentual):
            print(str(i) + " top2 -> "+ str(topic_model2.get_topic(i)))


#topic_model
print("===")


#try:
#retorno, score = resposta(question,content,coluna[0] + " - " + coluna[1])
retorno = "renato"
score =0
#print('*'+str(score))
for j in range(0,score):
    retorno= retorno + " "+ retorno

resultados = resultados +" "+ retorno
textointeiro=textointeiro + "\n"+content
#except:
 #   print("An exception occurred")
#print(resultados)
wc = WordCloud(stopwords=STOPWORDS,background_color="white", max_words=2000,
               max_font_size=256,
               random_state=42, width=1550, height=1080,collocations=False)
wc.generate(resultados) #ajuste do tamanho das palavras
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
print('teste')
#plt.show()
retorno, score = resposta(question,textointeiro,"teste")
