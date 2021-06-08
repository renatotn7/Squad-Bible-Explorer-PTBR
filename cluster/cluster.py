import re
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('D:\\0000python\\squadbert\\distiluse-base-multilingual-cased-v1')
#kiri-ai/distiluse-base-multilingual-cased-et

mylistMateus = ["Mateus1p1", "Mateus1p2", "Mateus2p1", "Mateus2p2", "Mateus2p3","Mateus3p1", "Mateus3p2","Mateus4p1", "Mateus4p2","Mateus5p1","Mateus5p2", "Mateus5p3",
           "Mateus6p1","Mateus6p2","Mateus7p1","Mateus7p2","Mateus7p3","Mateus7p4","Mateus7p5","Mateus7p6","Mateus7p7",
           "Mateus8p1","Mateus8p2","Mateus8p3","Mateus8p4","Mateus8p5","Mateus8p6","Mateus9p1","Mateus9p2","Mateus9p3","Mateus9p4","Mateus9p5","Mateus9p6",'Mateus10p1',
           'Mateus11p1','Mateus11p2','Mateus11p3',"Mateus12p1","Mateus12p2","Mateus12p3","Mateus12p4","Mateus12p5","Mateus12p6","Mateus13p1","Mateus13p2","Mateus13p3",
           "Mateus13p4","Mateus13p5","Mateus14p1","Mateus14p2","Mateus14p3"]
           

mylistJoao = ["Joao1p1", "Joao1p2", "Joao1p3","Joao2p1", "Joao2p2","Joao3p1", "Joao3p2","Joao4p1", "Joao4p2", "Joao4p3", "Joao5p1", "Joao5p2"]

mylistMarcos = ["Marcos1p1", "Marcos1p2", "Marcos1p3","Marcos1p4", "Marcos1p5","Marcos1p6","Marcos2p1", "Marcos2p2", "Marcos2p3","Marcos2p4",
"Marcos3p1", "Marcos3p2", "Marcos3p3","Marcos3p4","Marcos3p5",
"Marcos4p1", "Marcos4p2", "Marcos4p3","Marcos4p4","Marcos4p5","Marcos5p1", "Marcos5p2"]


mylistLucas = ["Lucas1p1", "Lucas1p2", "Lucas1p3","Lucas1p4", "Lucas1p5", "Lucas1p6",
          "Lucas2p1", "Lucas2p2", "Lucas2p3","Lucas2p4", "Lucas2p5",
          "Lucas3p1", "Lucas3p2", "Lucas3p3",
          "Lucas4p1", "Lucas4p2", "Lucas4p3","Lucas4p4"]
          
simvalue=0.65          
listamateusjoao=[]
listamateusmarcos=[]
listamateuslucas=[]
listajoaomarcos=[]   
listajoaolucas=[] 
listamarcoslucas=[] 
listaversiculos=[]
listaversiculosv2=[]
for mateus in mylistMateus:
    f = open(mateus, encoding="utf8")
    conteudo = re.sub(r'’|“|‘|”','',f.read())
    conteudo = re.sub(r'\d','',conteudo)
    conteudo = re.sub(r'\n\.','\n',conteudo)
    conteudo = re.sub(r'\n ','\n',conteudo)
    conteudo = re.sub(r'\r\n','\n',conteudo)
    conteudo = re.sub(r'\n\n','\n',conteudo)
    contextMateus = conteudo
    f.close()
    for joao in mylistJoao:
            f = open(joao, encoding="utf8")
            conteudo = re.sub(r'’|“|‘|”','',f.read())
            conteudo = re.sub(r'\d','',conteudo)
            conteudo = re.sub(r'\n\.','\n',conteudo)
            conteudo = re.sub(r'\n ','\n',conteudo)
            conteudo = re.sub(r'\r\n','\n',conteudo)
            conteudo = re.sub(r'\n\n','\n',conteudo)
            contextJoao=conteudo
            f.close()
            if (mateus+","+joao) not in listamateusjoao:
                similarity  = util.pytorch_cos_sim(model.encode(contextMateus), model.encode(contextJoao))
                listamateusjoao.append(mateus+","+joao)
                if similarity > simvalue:
                    print(mateus+","+joao+" -  Similarity:", similarity)
                    listaversiculos.append(mateus+","+joao)


for mateus in mylistMateus:
    f = open(mateus, encoding="utf8")
    conteudo = re.sub(r'’|“|‘|”','',f.read())
    conteudo = re.sub(r'\d','',conteudo)
    conteudo = re.sub(r'\n\.','\n',conteudo)
    conteudo = re.sub(r'\n ','\n',conteudo)
    conteudo = re.sub(r'\r\n','\n',conteudo)
    conteudo = re.sub(r'\n\n','\n',conteudo)
    contextMateus = conteudo
    f.close()
    for marcos in mylistMarcos:
                f = open(marcos, encoding="utf8")
                conteudo = re.sub(r'’|“|‘|”','',f.read())
                conteudo = re.sub(r'\d','',conteudo)
                conteudo = re.sub(r'\n\.','\n',conteudo)
                conteudo = re.sub(r'\n ','\n',conteudo)
                conteudo = re.sub(r'\r\n','\n',conteudo)
                conteudo = re.sub(r'\n\n','\n',conteudo)
                contextMarcos=conteudo
                f.close()
                if (mateus+","+marcos) not in listamateusmarcos:
                    similarity  = util.pytorch_cos_sim(model.encode(contextMateus), model.encode(contextMarcos))
                    listamateusmarcos.append(mateus+","+marcos)
                    if similarity > simvalue:
                        print(mateus+","+marcos+" -  Similarity:", similarity)
                        encontrou=0
                        for i in range(0,len(listaversiculos)):
                            if mateus in listaversiculos[i] and  marcos not in listaversiculos[i]:
                                listaversiculos[i]= listaversiculos[i]+","+marcos
                                encontrou=1
                            if marcos in listaversiculos[i]  and  mateus not in listaversiculos[i] :
                                listaversiculos[i]= listaversiculos[i]+","+mateus
                                encontrou=1
                        if encontrou==0:
                            listaversiculos.append(mateus+","+marcos)


for mateus in mylistMateus:
    f = open(mateus, encoding="utf8")
    conteudo = re.sub(r'’|“|‘|”','',f.read())
    conteudo = re.sub(r'\d','',conteudo)
    conteudo = re.sub(r'\n\.','\n',conteudo)
    conteudo = re.sub(r'\n ','\n',conteudo)
    conteudo = re.sub(r'\r\n','\n',conteudo)
    conteudo = re.sub(r'\n\n','\n',conteudo)
    contextMateus = conteudo
    f.close()
    for lucas in mylistLucas:
                    f = open(lucas, encoding="utf8")
                    conteudo = re.sub(r'’|“|‘|”','',f.read())
                    conteudo = re.sub(r'\d','',conteudo)
                    conteudo = re.sub(r'\n\.','\n',conteudo)
                    conteudo = re.sub(r'\n ','\n',conteudo)
                    conteudo = re.sub(r'\r\n','\n',conteudo)
                    conteudo = re.sub(r'\n\n','\n',conteudo)

                    #print(conteudo)
                    contextLucas = conteudo
                    f.close()
                    #if myItem in list:
                    if (mateus+","+lucas) not in listamateuslucas:
                        similarity  = util.pytorch_cos_sim(model.encode(contextMateus), model.encode(contextLucas))
                        listamateuslucas.append(mateus+","+lucas)
                        if similarity > simvalue:
                            print(mateus+","+lucas+" -  Similarity:", similarity)
                            for i in range(0,len(listaversiculos)):
                                if mateus in listaversiculos[i] and  lucas not in listaversiculos[i]:
                                    listaversiculos[i]= listaversiculos[i]+","+lucas
                                    encontrou=1
                                if lucas in listaversiculos[i] and  mateus not in listaversiculos[i]:
                                    listaversiculos[i]= listaversiculos[i]+","+mateus
                                    encontrou=1
                            if encontrou==0:
                                listaversiculos.append(mateus+","+lucas)



for joao in mylistJoao:
    f = open(joao, encoding="utf8")
    conteudo = re.sub(r'’|“|‘|”','',f.read())
    conteudo = re.sub(r'\d','',conteudo)
    conteudo = re.sub(r'\n\.','\n',conteudo)
    conteudo = re.sub(r'\n ','\n',conteudo)
    conteudo = re.sub(r'\r\n','\n',conteudo)
    conteudo = re.sub(r'\n\n','\n',conteudo)
    contextJoao=conteudo
    f.close()
    for marcos in mylistMarcos:
                f = open(marcos, encoding="utf8")
                conteudo = re.sub(r'’|“|‘|”','',f.read())
                conteudo = re.sub(r'\d','',conteudo)
                conteudo = re.sub(r'\n\.','\n',conteudo)
                conteudo = re.sub(r'\n ','\n',conteudo)
                conteudo = re.sub(r'\r\n','\n',conteudo)
                conteudo = re.sub(r'\n\n','\n',conteudo)
                contextMarcos=conteudo
                f.close()
                if (joao+","+marcos) not in listajoaomarcos:
                   similarity  = util.pytorch_cos_sim(model.encode(contextJoao), model.encode(contextMarcos))
                   listajoaomarcos.append(joao+","+marcos)
                   if similarity > simvalue:
                       print(joao+","+marcos+" -  Similarity:", similarity)
                       for i in range(0,len(listaversiculos)):
                           if joao in listaversiculos[i] and  marcos not in listaversiculos[i]:
                               listaversiculos[i]= listaversiculos[i]+","+marcos
                               encontrou=1
                           if marcos in listaversiculos[i] and  joao not in listaversiculos[i]:
                               listaversiculos[i]= listaversiculos[i]+","+joao
                               encontrou=1
                       if encontrou==0:
                           listaversiculos.append(joao+","+marcos)


for joao in mylistJoao:
    f = open(joao, encoding="utf8")
    conteudo = re.sub(r'’|“|‘|”','',f.read())
    conteudo = re.sub(r'\d','',conteudo)
    conteudo = re.sub(r'\n\.','\n',conteudo)
    conteudo = re.sub(r'\n ','\n',conteudo)
    conteudo = re.sub(r'\r\n','\n',conteudo)
    conteudo = re.sub(r'\n\n','\n',conteudo)
    contextJoao=conteudo
    f.close()
    for lucas in mylistLucas:
                    f = open(lucas, encoding="utf8")
                    conteudo = re.sub(r'’|“|‘|”','',f.read())
                    conteudo = re.sub(r'\d','',conteudo)
                    conteudo = re.sub(r'\n\.','\n',conteudo)
                    conteudo = re.sub(r'\n ','\n',conteudo)
                    conteudo = re.sub(r'\r\n','\n',conteudo)
                    conteudo = re.sub(r'\n\n','\n',conteudo)

                    #print(conteudo)
                    contextLucas = conteudo
                    f.close()
                    #if myItem in list:
                    if (joao+","+lucas) not in listajoaolucas:
                        similarity  = util.pytorch_cos_sim(model.encode(contextJoao), model.encode(contextLucas))
                        listajoaolucas.append(joao+","+lucas)
                        if similarity > simvalue:
                            print(joao+","+lucas+" -  Similarity:", similarity)
                            for i in range(0,len(listaversiculos)):
                                if joao in listaversiculos[i] and  lucas not in listaversiculos[i]:
                                    listaversiculos[i]= listaversiculos[i]+","+lucas
                                    encontrou=1
                                if lucas in listaversiculos[i] and  joao not in listaversiculos[i]:
                                    listaversiculos[i]= listaversiculos[i]+","+joao
                                    encontrou=1
                            if encontrou==0:
                                listaversiculos.append(joao+","+lucas)



for marcos in mylistMarcos:
    f = open(marcos, encoding="utf8")
    conteudo = re.sub(r'’|“|‘|”','',f.read())
    conteudo = re.sub(r'\d','',conteudo)
    conteudo = re.sub(r'\n\.','\n',conteudo)
    conteudo = re.sub(r'\n ','\n',conteudo)
    conteudo = re.sub(r'\r\n','\n',conteudo)
    conteudo = re.sub(r'\n\n','\n',conteudo)
    contextMarcos=conteudo
    for lucas in mylistLucas:
                    f = open(lucas, encoding="utf8")
                    conteudo = re.sub(r'’|“|‘|”','',f.read())
                    conteudo = re.sub(r'\d','',conteudo)
                    conteudo = re.sub(r'\n\.','\n',conteudo)
                    conteudo = re.sub(r'\n ','\n',conteudo)
                    conteudo = re.sub(r'\r\n','\n',conteudo)
                    conteudo = re.sub(r'\n\n','\n',conteudo)

                    #print(conteudo)
                    contextLucas = conteudo
                    f.close()
                    #if myItem in list:
                    if (marcos+","+lucas) not in listamarcoslucas:
                        similarity  = util.pytorch_cos_sim(model.encode(contextMarcos), model.encode(contextLucas))
                        listamarcoslucas.append(marcos+","+lucas)
                        if similarity > simvalue:
                            print(marcos+","+lucas+" -  Similarity:", similarity) 
                            for i in range(0,len(listaversiculos)):
                                if marcos in listaversiculos[i] and  lucas not in listaversiculos[i]:
                                    listaversiculos[i]= listaversiculos[i]+","+lucas
                                    encontrou=1
                                if lucas in listaversiculos[i] and  marcos not in listaversiculos[i]: 
                                    listaversiculos[i]= listaversiculos[i]+","+marcos
                                    encontrou=1
                            if encontrou==0:
                                listaversiculos.append(marcos+","+lucas)
                                
for palavra in listaversiculos:
    print(palavra)
