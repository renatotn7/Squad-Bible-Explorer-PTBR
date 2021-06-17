import transformers
from transformers import pipeline
import re
from wordcloud import STOPWORDS, WordCloud
from argparse import ArgumentParser, Namespace
from decimal import Decimal
import requests
import os
import matplotlib.pyplot as plt






f = open('livrosbiblia.txt')
texto = f.read()
linhas = texto.split("\n")
f.close()
versoes = ['acf','rc69','vc']
for versao in versoes:
    todotexto=""
    todotexto1=""

    todotextovalid=""
    todotexto1valid=""


    todotextotest=""
    todotexto1test=""

    listrandom=[]
    listrandom1=[]
    import random

    for i in range(0,930):
        value=  random.randint(0, 31103)
        value1 = random.randint(0, 31103)
        if value not in listrandom:
            listrandom.append( value )#31103 3% para valid 3% para
        else:
            i-=1
        if value1 not in listrandom1:
            listrandom1.append( value1 )#31103 3% para valid 3% para
        else:
            i-=1

    numeroversiculo=0
    for i in range(0, len(linhas)):  # 30):
        content = ""
        content1 = ""
        linha = linhas[i]
        coluna = linha.split("\t")
        try:
            for j in range(1,int(coluna[2])+1):
                try:
                    f = open("biblia" + "/" + "nvt" + "/" + coluna[1] + "/"+str(j)+".txt", "r") #vai dar errado, apenas para descer por enquanto, preciso decidir como fazer isso
                    conteudo = f.read()
                    conteudo = re.sub(r'’|“|‘|”', '', conteudo)
                    conteudo = re.sub(r'\d', '', conteudo)
                    conteudo = re.sub(r'\n\.', '\n', conteudo)
                    conteudo = re.sub(r'\n ', '\n', conteudo)
                    conteudo = re.sub(r'\r\n', '\n', conteudo)
                    conteudo = re.sub(r'\n\n', '\n', conteudo)
                    conteudo = re.sub(r'\r\n', '\n', conteudo)
                    while '  ' in conteudo:
                        conteudo = re.sub(r'  ', ' ', conteudo)
                    while '\n\n' in conteudo:
                        conteudo = re.sub(r'\n\n', '\n', conteudo)
                    while '\r\n\r\n' in conteudo:
                        conteudo = re.sub(r'\r\n\r\n', '\n', conteudo)
                    conteudo = re.sub(r'\n ', '\n', conteudo)
                    conteudo = re.sub(r'^\n', '\n', conteudo)
                    conteudo = re.sub(r'^\r\n', '', conteudo)
                    content = conteudo
                    f.close()

                    f = open("biblia" + "/" + versao + "/" + coluna[1] + "/" + str(j) + ".txt",
                             "r")  # vai dar errado, apenas para descer por enquanto, preciso decidir como fazer isso #vc
                    conteudo = f.read()
                    conteudo = re.sub(r'’|“|‘|”', '', conteudo)
                    conteudo = re.sub(r'\d', '', conteudo)
                    conteudo = re.sub(r'\n\.', '\n', conteudo)
                    conteudo = re.sub(r'\n ', '\n', conteudo)
                    conteudo = re.sub(r'\r\n', '\n', conteudo)
                    conteudo = re.sub(r'\n\n', '\n', conteudo)
                    conteudo = re.sub(r'\r\n', '\n', conteudo)
                    while '  ' in conteudo:
                        conteudo = re.sub(r'  ', ' ', conteudo)
                    while '\n\n' in conteudo:
                        conteudo = re.sub(r'\n\n', '\n', conteudo)
                    while '\r\n\r\n' in conteudo:
                        conteudo = re.sub(r'\r\n\r\n', '\n', conteudo)
                    conteudo = re.sub(r'\n ', '\n', conteudo)
                    conteudo = re.sub(r'^\n', '\n', conteudo)
                    conteudo = re.sub(r'^\r\n', '', conteudo)
                    content1 = conteudo
                    f.close()
                    linhascontent = content.split("\n")
                    linhascontent1=content1.split("\n")
                    if len(linhascontent) != len(linhascontent1):


                        print(str(len(linhascontent ))+" - "+str(len(linhascontent1)))
                        print("retirar "+coluna[1] + "/" + str(j) + ".txt")
                    else:
                        for nlinha in range(0,len(linhascontent)):
                            if len(linhascontent[nlinha])>0:
                                if numeroversiculo in listrandom:
                                    todotextotest+="\n"+linhascontent[nlinha]
                                    todotexto1test += "\n" + linhascontent1[nlinha]
                                elif numeroversiculo in listrandom1:
                                    todotextovalid += "\n" + linhascontent[nlinha]
                                    todotexto1valid += "\n" + linhascontent1[nlinha]
                                else:
                                    todotexto +="\n" + linhascontent[nlinha]
                                    todotexto1 +="\n" + linhascontent1[nlinha]
                                numeroversiculo+=1

                except:
                    print("pulou1")
        except:
            print("erro")

    fg = open("biblia" + "/" + "train.tags.ot-nvt.nvt.txt", "a", encoding="utf8")
    print("----------")
    fg.write(todotexto.strip())
    fg.close()
    fg = open("biblia" + "/" + "train.tags.ot-nvt.ot.txt", "a", encoding="utf8")
    print("----------")
    fg.write(todotexto1.strip())
    fg.close()

    fg = open("biblia" + "/" + "test.tags.ot-nvt.nvt.txt", "a", encoding="utf8")
    print("----------")
    fg.write(todotextotest.strip())
    fg.close()
    fg = open("biblia" + "/" +"test.tags.ot-nvt.ot.txt", "a", encoding="utf8")
    print("----------")
    fg.write(todotexto1test.strip())
    fg.close()


    fg = open("biblia" + "/" + "valid.tags.ot-nvt.nvt.txt", "a", encoding="utf8")
    print("----------")
    fg.write(todotextovalid.strip())
    fg.close()
    fg = open("biblia" + "/" + "valid.tags.ot-nvt.ot.txt", "a", encoding="utf8")
    print("----------")
    fg.write(todotexto1valid.strip())
    fg.close()