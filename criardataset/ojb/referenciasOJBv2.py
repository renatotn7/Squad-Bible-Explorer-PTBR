from docx import Document
import json

from openpyxl import Workbook
import openpyxl
from openpyxl.styles import Alignment
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

import requests
import pandas as pd

# Make a GET request to the Sefaria API to retrieve all related texts to Genesis 2:2
url = 'https://www.sefaria.org/api/texts/Genesis.2.2?commentary=1&context=0&versions=all&sheets=0&wrapLinks=1&language=en'
response = requests.get(url)
df = pd.read_json(json.dumps(response.json()))
pring(df)
# Filter out texts that do not have the fields 'text', 'collectiveTitle', 'title', 'chapter', 'verse'
filtered_texts = [text for text in response.json() if all(key in text for key in ('text', 'collectiveTitle', 'title', 'chapter', 'verse'))]

# Load the filtered texts into a pandas DataFrame
df = pd.DataFrame(filtered_texts)
print(df)
# Add the columns 'Text', 'Comentator', 'Book', 'Chapter', 'Verse' if they are not None or NaN
df['Text'] = df.text
df['Comentator'] = df.collectiveTitle.map(lambda x: x.get("en"))
df['Book'] = df.title
df['Chapter'] = df.chapter
df['Verse'] = df.verse

# Display the DataFrame
print(df)

exit()
dfra_csv = pd.read_csv("../Rashi_ot.csv")
dfrb_csv = pd.read_csv("../Ramban_ot.csv")
dfsf_csv = pd.read_csv("../Sforno_ot.csv")
dfibn_csv = pd.read_csv("../Ibn_Ezra_ot.csv")

# Função para extrair o texto de uma passagem específica da Bíblia
def extrair_passagemnvi(livro, cap, ver):
    # URL da passagem a ser extraída
    url = f'https://www.bibliaonline.com.br/nvi/{livro}/{cap}/{ver}'

    # Fazendo a requisição
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extrair o texto da passagem
    passagem = soup.find('p', class_='jss35')
    if passagem is None:
        print(f"Não foi possível encontrar a passagem {livro}/{cap}/{ver}")
        return None
    return passagem.get_text()
def extrair_passagem(livro, cap, ver,livroreduzido,url):

    # URL da passagem a ser extraída
    url = f'https://www.biblegateway.com{url}'
    print(url)
    # Fazendo a requisição
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extrair o texto da passagem
    print(f'Extraindo passagem {livroreduzido}.{cap}.{ver}...')
    passagem2 = soup.find('span', class_=f'{livroreduzido}-{cap}-{ver}')
    if passagem2 is None:
        print(f"Não foi possível encontrar a passagem {livroreduzido}.{cap}.{ver}")
        return None
    return passagem2.get_text().replace(';', '.,')

# Função para salvar o texto de todas as passagens em um único arquivo
#def salvar_passagens(nome_arquivo, passagens):
#    with open(nome_arquivo, 'w') as f:
#        for passagem in passagens:
#            f.write(passagem + '\n')
#        print(f'Todas as passagens foram salvas com sucesso no arquivo {nome_arquivo}')

# Função para ler as passagens a serem extraídas de um arquivo
#def ler_passagens(arquivo):
#    passagens = []
#    print(arquivo)
#    with open(arquivo, 'r') as f:
#        for linha in f:
#            passagens.append(linha.strip())
#    return passagens

# Função principal
def melhoraxlsx(file):

    wb = openpyxl.load_workbook(file+'.xlsx')
    ws = wb['Sheet1']

    # Setando largura de coluna e altura de linha
    for col in ws.columns:

        max_length = 0
        column = col[0].column  # Get the column name
        for cell in col:
            try:  # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[col[0].column_letter].width = adjusted_width




    # Setando formatação rowrap nas células
    for row in ws.iter_rows():
        ws.row_dimensions[row[0].row].height = 6.82*10
        for cell in row:
            cell.alignment = Alignment(wrap_text=True)

    # Salvando o arquivo modificado
    wb.save(file+'_output.xlsx')
def extrair_e_salvar(arquivosalvar,df):
    for index, row in df.iterrows():

        df.at[index, "texto1"] = extrair_passagem(df.at[index, "Livro"] , df.at[index, "Capitulo"] , df.at[index, "Versiculo"] , df.at[index, "livroreduzido"], df.at[index, "url"])
        df.at[index, "nvi"] = extrair_passagemnvi(df.at[index, "siglaBr"], df.at[index, "Capitulo"],
                                                  df.at[index, "Versiculo"])
        # {'texto1', 'passagem', 'url', 'livroreduzido', 'Livro', 'Capitulo', 'Versiculo'})


        # Selecionando os campos desejados
        # dfra_csv = dfra_csv[['Livro','Capitulo','Versiculo','Rashi']]
        #df_psv = df_psv[['Livro', 'Capitulo', 'Versiculo', 'texto1']]
        df['Capitulo'] = df['Capitulo'].astype(int)

        match = re.search(r'\(([^)]+)\)',df.at[index, "texto1"] )
        if match:
            number_between_parentheses = match.group(1)
            df['Versiculo']=number_between_parentheses
        df['Versiculo'] = df['Versiculo'].astype(int)

        merged_df = pd.merge(df[['Livro', 'Capitulo', 'Versiculo', 'texto1', 'nvi']],
                             dfra_csv[['Rashi', 'Livro', 'Capitulo', 'Versiculo']],
                             on=['Livro', 'Capitulo', 'Versiculo'], how="left")
        merged_df2 = pd.merge(merged_df[['Livro', 'Capitulo', 'Versiculo', 'texto1',  'nvi','Rashi']],
                              dfrb_csv[['Ramban', 'Livro', 'Capitulo', 'Versiculo']],
                              on=['Livro', 'Capitulo', 'Versiculo'], how="left")
        merged_df3 = pd.merge(merged_df2[['Livro', 'Capitulo', 'Versiculo', 'texto1', 'nvi', 'Rashi', 'Ramban']],
                              dfsf_csv[['Sforno', 'Livro', 'Capitulo', 'Versiculo']],
                              on=['Livro', 'Capitulo', 'Versiculo'], how="left")
        merged_df4 = pd.merge(merged_df3[['Livro', 'Capitulo', 'Versiculo', 'texto1', 'nvi', 'Rashi', 'Ramban', 'Sforno']],
                              dfibn_csv[['Ibn', 'Livro', 'Capitulo', 'Versiculo']],
                              on=['Livro', 'Capitulo', 'Versiculo'], how="left")

        # Salvando o arquivo resultante´
        #merged_df4.to_csv("resultadoKefa1.csv", index=False)
        merged_df4.to_excel(arquivosalvar+'.xlsx', index=False)
        melhoraxlsx(arquivosalvar)
        merged_df4.sort_values(by=['Livro', 'Capitulo', 'Versiculo'], inplace=True)
        merged_df4.to_excel(arquivosalvar+'_ordenado.xlsx', index=False)
        melhoraxlsx(arquivosalvar+'_ordenado')

        #df.to_csv(arquivosalvar, sep=';', encoding='utf-8', index=False)


def referencia(nomelivro,rangein):
    dfnorder = pd.DataFrame(
        {'texto1': [],'nvi':[], 'passagem': [], 'url': [], 'livroreduzido': [], 'Livro': [], 'Capitulo': [], 'Versiculo': [], 'siglaBr': []})
    dfcorder = pd.DataFrame(
        {'texto1': [], 'nvi':[], 'passagem': [], 'url': [], 'livroreduzido': [], 'Livro': [], 'Capitulo': [], 'Versiculo': [],'siglaBr': []})

    arquivofinal = nomelivro
    arquivoordenado=nomelivro+'od'
    arquivofinalordenado = nomelivro + 'odF'
    extensao='.txt'
    arquivointermediario=arquivofinal+'bf'

  #  arquivointermediario=arquivointermediario+extensao
    # Dicionário com as traduções das siglas em inglês para português
    traducoes = {
        'Gen': 'Gn',
        'Exod': 'Ex',
        'Lev': 'Lv',
        'Num': 'Nm',
        'Deut': 'Dt',
        'Josh': 'Js',
        'Judg': 'Jz',
        'Ruth': 'Rt',
        '1Sam': '1Sm',
        '2Sam': '2Sm',
        '1Kgs': '1Rs',
        '2Kgs': '2Rs',
        '1Chr': '1Cr',
        '2Chr': '2Cr',
        'Ezra': 'Ed',
        'Neh': 'Ne',
        'Esth': 'Et',
        'Job': 'Jó',
        'Ps': 'Sl',
        'Prov': 'Pv',
        'Eccl': 'Ec',
        'Song': 'Ct',
        'Isa': 'Is',
        'Jer' : 'Jr',
        'Lam': 'Lm',
        'Ezek': 'Ez',
        'Dan': 'Dn',
        'Hos': 'Os',
        'Joel': 'Jl',
        'Amos': 'Am',
        'Obad': 'Ob',
        'Jonah': 'Jn',
        'Mic': 'Mq',
        'Nah': 'Na',
        'Hab': 'Hb',
        'Zeph': 'Sf',
        'Hag': 'Hg',
        'Zech': 'Zc',
        'Mal': 'Ml',
        }
    traducoesinv = {
        'Gn': 'Gen',
        'Ex': 'Exod',
        'Lv': 'Lev',
        'Nm': 'Num',
        'Dt': 'Deut',
        'Js': 'Josh',
        'Jz': 'Judg',
        'Rt': 'Ruth',
        '1Sm': '1Sam',
        '2Sm': '2Sam',
        '1Rs': '1Kgs',
        '2Rs': '2Kgs',
        '1Cr': '1Chr',
        '2Cr': '2Chr',
        'Ed': 'Ezra',
        'Ne': 'Neh',
        'Et': 'Esth',
        'Jó': 'Job',
        'Sl': 'Ps',
        'Pv': 'Prov',
        'Ec': 'Eccl',
        'Ct': 'Song',
        'Is': 'Isa',
        'Jr': 'Jer',
        'Lm': 'Lam',
        'Ez': 'Ezek',
        'Dn': 'Dan',
        'Os': 'Hos',
        'Jl': 'Joel',
        'Am': 'Amos',
        'Ob': 'Obad',
        'Jn': 'Jonah',
        'Mq': 'Mic',
        'Na': 'Nah',
        'Hb': 'Hab',
        'Sf': 'Zeph',
        'Hg': 'Hag',
        'Zc': 'Zech',
        'Ml': 'Mal'
    }
    traducoes2 = {
        'Gen': 'Genesis',
        'Exod': 'Exodus',
        'Lev': 'Leviticus',
        'Num': 'Numbers',
        'Deut': 'Deuteronomy',
        'Josh': 'Joshua',
        'Judg': 'Judges',
        'Ruth': 'Ruth',
        '1Sam': '1 Samuel',
        '2Sam': '2 Samuel',
        '1Kgs': '1 Kings',
        '2Kgs': '2 Kings',
        '1Chr': '1 Chronicles',
        '2Chr': '2 Chronicles',
        'Ezra': 'Ezra',
        'Neh': 'Nehemiah',
        'Esth': 'Esther',
        'Job': 'Job',
        'Ps': 'Psalms',
        'Prov': 'Proverbs',
        'Eccl': 'Ecclesiastes',
        'Song': 'Song of Solomon',
        'Isa': 'Isaiah',
        'Jer': 'Jeremiah',
        'Lam': 'Lamentations',
        'Ezek': 'Ezekiel',
        'Dan': 'Daniel',
        'Hos': 'Hosea',
        'Joel': 'Joel',
        'Amos': 'Amos',
        'Obad': 'Obadiah',
        'Jonah': 'Jonah',
        'Mic': 'Micah',
        'Nah': 'Nahum',
        'Hab': 'Habakkuk',
        'Zeph': 'Zephaniah',
        'Hag': 'Haggai',
        'Zech': 'Zechariah',
        'Mal': 'Malachi',
    }

    # Cria uma lista vazia para armazenar as referências
    referencias = []
    referenciasfinal = []
    # Itera sobre os capítulos especificados
    nomelivropath=nomelivro.replace(' ','%20')
    strlinks = []
    siglas = []
    a_tags = []
    for capitulo in rangein:

        url = f'https://www.biblegateway.com/passage/?search={nomelivropath}%20{capitulo}&version=OJB'
        print('url '+ url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Seleciona todas as tags <a> com a classe "bibleref" e a propriedade "data-bibleref"https://www.biblegateway.com/passage/?search=Shemot%2024%3A7&version=OJB

        a_tags.extend( soup.select('a.bibleref[data-bibleref]'))

        links = soup.find_all("a", href=lambda value: value and value.startswith("/passage/?search="))

        # Iterar sobre cada link e imprimir o conteúdo href
        for link in links:
            stringln = link["href"]
            array = stringln.split(".")
            sigla1 = array[0]
            sigla1 = sigla1.replace("/passage/?search=", "")
            siglas.append(sigla1)
            if sigla1 in traducoes:
                strlinks.append(link["href"])
                #print(link["href"])




        # Armazena o valor da propriedade "data-bibleref" na lista
    for a_tag in a_tags:

        referencias.append(a_tag['data-bibleref'])

   # print("** "+str(referencias))
   # print("** "+str(strlinks))
   # print("** "+str(siglas))
    # Exibe a lista de referências
   # print(referencias)
 #   for i in range(len(referencias)):
#
 #       sigla = referencias[i].split('.')[0]
  ##
    #      referenciasfinal.append(referencias[i].replace(sigla, traducoes[sigla]) + ';'+ strlinks[i]+";" + siglas[i] +";"+sigla+";"+traducoes2[sigla]+","+referencias[i].split('.')[1]+","+referencias[i].split('.')[2]+",")

          #referenciasfinal.append(sigla + ";" + f"/passage/?search={traducoesinv[sigla.split('.')[0]] + '.' + sigla.split('.')[1] + '.' + sigla.split('.')[2]}&version=OJB" + ";" + traducoesinv[sigla.split('.')[0]] + ";" + traducoes2[traducoesinv[sigla.split('.')[0]]] + "," + sigla.split('.')[1] + ',' + sigla.split('.')[2] + ",")
     #   except:
      #   print( 'nao achou')
    #referencias=referenciasfinal
    #print(referencias)
    nome_arquivo = arquivointermediario

    # Itera sobre as referências e substitui os pontos por \
    #referencias = [referencia.split(";").replace(".", "/") for referencia in referencias]
    #print (referencias)
    # Salva as referências no arquivo
    #with open(nome_arquivo, "w") as arquivo:
      #  arquivo.write("\n".join(referencias))

    if True:

        # Itera sobre as referências e substitui os pontos por \
        referencias_expandidas = []
        for referencia in referencias:
            referenciaalfa = referencia
            referencia=referencia.split(";")[0]
            if "-" in referencia:
                referencia1,referencia2 = referencia.split("-")
                verso1= referencia1.split(".")[2]
                verso2= referencia2.split(".")[2]
                cap = referencia2.split(".")[1]
                livro = referencia2.split(".")[0]

                inicio, fim = verso1,verso2
                for i in range(int(inicio), int(fim) + 1):
                    referencia_expandida = f"{livro}.{cap}.{i}"

                    referencias_expandidas.append(referencia_expandida)
            else:
                referencias_expandidas.append(referencia)

        referencias_expandidas= list(set(referencias_expandidas))
       # print(referencias_expandidas)
        versiculos =referencias_expandidas
        referencias_expandidasfinal = []
        versiculosfinal= []
        for v in referencias_expandidas:
            try:
                traducoes2[v.split('.')[0]]
                versiculosfinal.append(v)
                dfnorder.loc[len(dfnorder)] = ['', '',v, f"/passage/?search={v.split('.')[0] + '.' + v.split('.')[1] + '.' + v.split('.')[2]}&version=OJB",v.split('.')[0] ,  traducoes2[v.split('.')[0]], v.split('.')[1], v.split('.')[2],traducoes[v.split('.')[0]]]
               # dfnorder   #{'texto1', 'passagem', 'url', 'livroreduzido', 'Livro', 'Capitulo', 'Versiculo'})
 #               dfnorder.append({'passagem': v, 'url': f"/passage/?search={v.split('.')[0] + '.' + v.split('.')[1] + '.' + v.split('.')[2]}&version=OJB" ,
  #                                    'livroreduzido':v.split('.')[0] , 'Livro': traducoes2[v.split('.')[0]], 'Capitulo': v.split('.')[1], 'Versiculo': v.split('.')[2]}, ignore_index=True)
                referencias_expandidasfinal.append(
                    v + ";" + f"/passage/?search={v.split('.')[0] + '.' + v.split('.')[1] + '.' + v.split('.')[2]}&version=OJB" + ";" +
                    v.split('.')[0] + ";" + traducoes2[v.split('.')[0]] + ";" + v.split('.')[
                        1] + ';' + v.split('.')[2] )
            except:
               print( 'nao achou')
        print(dfnorder) #print(referencias_expandidasfinal)


       # print(referencias_expandidasfinal)

        # Cria uma lista com a ordem dos livros na Bíblia
        ordem_livros = ["Gn", "Ex", "Lv", "Nm", "Dt", "Js", "Jz", "Rt", "1Sm", "2Sm", "1Rs", "2Rs", "1Cr", "2Cr", "Ed",
                        "Ne", "Et", "Jó", "Sl", "Pv", "Ec", "Ct", "Is", "Jr", "Lm", "Ez", "Dn", "Os", "Jl", "Am", "Ob",
                        "Mq", "Na", "Hc", "Sf", "Ag", "Zc", "Ml"]

        # Ordena a lista de versículos usando a ordem dos livros

        versiculos_ordenados = []
        for v in versiculosfinal:
            v1 = v
            v=v.split(";")[0]

            parts = v.split(".")
            livro = parts[0]
            if len(parts) != 3:
                print("Versiculo invalido: ", v)
                continue



            try:
                if traducoes[livro] not in ordem_livros:
                    print("Livro invalido: ", livro)
                    continue
            except:
                print("Livro invalido: ", livro)
                continue
            try:
                cap = int(parts[1])
                verso = int(parts[2])
            except ValueError:
                print("Capitulo ou versiculo invalido: ", v)
                continue
            versiculos_ordenados.append(f"{parts[0]}.{parts[1]}.{parts[2]}")
            #versiculos_ordenados.append(v1)
           # print(versiculos_ordenados)

        #versiculos_ordenados = sorted(versiculos_ordenados, key=lambda x: (ordem_livros.index(x[0]), x[1], x[2]))
        #print(versiculos_ordenados)
        versiculos_ordenados = sorted(versiculos_ordenados, key=lambda x: (ordem_livros.index(traducoes[x.split(".")[0]]), int(x.split(".")[1]), int(x.split(".")[2].split(";")[0])))
        versiculos_ordenadosfinal=[]
        for v in versiculos_ordenados:
         #   , dfcorder
            dfcorder.loc[len(dfcorder)] = ['', '',v, f"/passage/?search={v.split('.')[0]+'.'+v.split('.')[1]+'.'+v.split('.')[2]}&version=OJB",v.split('.')[0] ,  traducoes2[v.split('.')[0]], v.split('.')[1], v.split('.')[2],traducoes[v.split('.')[0]]]
         #{'texto1', 'passagem', 'url', 'livroreduzido', 'Livro', 'Capitulo', 'Versiculo'})
            versiculos_ordenadosfinal.append(v+";"+f"/passage/?search={v.split('.')[0]+'.'+v.split('.')[1]+'.'+v.split('.')[2]}&version=OJB"+";"+v.split('.')[0]+";"+traducoes2[v.split('.')[0]]+";"+v.split('.')[1]+';'+v.split('.')[2])

       # print(versiculos_ordenadosfinal)
        # Imprime a lista de versículos ordenada
        print(dfcorder)

        #arquivo.write("\n".join(referencias_expandidasfinal))

        #with open(arquivoordenado, "w") as arquivood:
        #    arquivood.write("\n".join(versiculos_ordenadosfinal))
        #    arquivood.close()
        #arquivo.close()

    extrair_e_salvar(arquivofinal,dfnorder)
   # extrair_e_salvar(arquivoordenado,dfcorder)





#Yaakov	1 2 3 4 5
#KKefa I	1 2 3 4 5
#Kefa I	1 2 3 4 5
#Kefa II	1 2 3
#Yochanan I	1 2 3 4 5
#Yochanan II	1
#Yochanan III	1
#Yehuda	1
##########################################################################

# Executando a função principal
#referencia('Kefa I',[1,2,3,4,5])
#exit()
# Carregando arquivos CSV e PSV

referencia('Yochanan II',[1])
referencia('Yochanan III',[1])
referencia('Yehuda',[1])
referencia('Kefa II',[1,2,3])

referencia('Yaakov I',[1,2,3,4,5])
referencia('Gevurot',range(1,29))
referencia('Hisgalus',range(1,23))
#referencia('Yehudim in Moshiach',range(1,13))


