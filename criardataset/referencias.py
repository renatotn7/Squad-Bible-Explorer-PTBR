from bs4 import BeautifulSoup
import requests



# Função para extrair o texto de uma passagem específica da Bíblia
def extrair_passagem(livro, cap, ver):
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

# Função para salvar o texto de todas as passagens em um único arquivo
def salvar_passagens(nome_arquivo, passagens):
    with open(nome_arquivo, 'w') as f:
        for passagem in passagens:
            f.write(passagem + '\n')
        print(f'Todas as passagens foram salvas com sucesso no arquivo {nome_arquivo}')

# Função para ler as passagens a serem extraídas de um arquivo
def ler_passagens(arquivo):
    passagens = []
    print(arquivo)
    with open(arquivo, 'r') as f:
        for linha in f:
            passagens.append(linha.strip())
    return passagens

# Função principal
def extrair_e_salvar(arquivo,arquivosalvar):
    passagens = ler_passagens(arquivo)
    if len(passagens) > 0:
        textos_passagens = []
        for passagem in passagens:
            try:
                livro, cap, ver = passagem.split('/')

                texto = extrair_passagem(livro, cap, ver)
                if texto is not None:
                    textos_passagens.append(texto + '( '+ passagem +' )')
            except ValueError:
                print(f'Passagem {passagem} não está no formato correto')
        salvar_passagens(arquivosalvar, textos_passagens)
    else:
        print("Não há passagens para processar")


def referencia(nomelivro,rangein):
    arquivofinal = nomelivro
    arquivoordenado=nomelivro+'od.txt'
    arquivofinalordenado = nomelivro + 'odF.txt'
    extensao='.txt'
    arquivointermediario=arquivofinal+'bf'
    arquivofinal=arquivofinal+extensao
    arquivointermediario=arquivointermediario+extensao
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


    # Cria uma lista vazia para armazenar as referências
    referencias = []
    referenciasfinal = []
    # Itera sobre os capítulos especificados
    nomelivropath=nomelivro.replace(' ','%20')
    for capitulo in rangein:
        url = f'https://www.biblegateway.com/passage/?search={nomelivropath}%20{capitulo}&version=OJB'
        print('url '+ url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Seleciona todas as tags <a> com a classe "bibleref" e a propriedade "data-bibleref"
        a_tags = soup.select('a.bibleref[data-bibleref]')

        # Armazena o valor da propriedade "data-bibleref" na lista
        for a_tag in a_tags:
            print(a_tag['data-bibleref'])
            referencias.append(a_tag['data-bibleref'])

    # Exibe a lista de referências
   # print(referencias)
    for i in range(len(referencias)):
        sigla = referencias[i].split('.')[0]
       # print(sigla)
        if sigla in traducoes:
            referenciasfinal.append(referencias[i].replace(sigla, traducoes[sigla]))

    referencias=referenciasfinal

    nome_arquivo = arquivointermediario

    # Itera sobre as referências e substitui os pontos por \
    referencias = [referencia.replace(".", "/") for referencia in referencias]
    #print (referencias)
    # Salva as referências no arquivo
    with open(nome_arquivo, "w") as arquivo:
      #  arquivo.write("\n".join(referencias))



        # Itera sobre as referências e substitui os pontos por \
        referencias_expandidas = []
        for referencia in referencias:
            if "-" in referencia:
                referencia1,referencia2 = referencia.split("-")
                verso1= referencia1.split("/")[2]
                verso2= referencia2.split("/")[2]
                cap = referencia2.split("/")[1]
                livro = referencia2.split("/")[0]

                inicio, fim = verso1,verso2
                for i in range(int(inicio), int(fim) + 1):
                    referencia_expandida = f"{livro}/{cap}/{i}"
                    referencias_expandidas.append(referencia_expandida)
            else:
                referencias_expandidas.append(referencia)

        referencias_expandidas= list(set(referencias_expandidas))
        versiculos =referencias_expandidas
        print(versiculos)

        # Cria uma lista com a ordem dos livros na Bíblia
        ordem_livros = ["Gn", "Ex", "Lv", "Nm", "Dt", "Js", "Jz", "Rt", "1Sm", "2Sm", "1Rs", "2Rs", "1Cr", "2Cr", "Ed",
                        "Ne", "Et", "Jó", "Sl", "Pv", "Ec", "Ct", "Is", "Jr", "Lm", "Ez", "Dn", "Os", "Jl", "Am", "Ob",
                        "Mq", "Na", "Hc", "Sf", "Ag", "Zc", "Ml"]

        # Ordena a lista de versículos usando a ordem dos livros

        versiculos_ordenados = []
        for v in versiculos:
            parts = v.split("/")

            if len(parts) != 3:
                print("Versiculo invalido: ", v)
                continue


            livro = parts[0]
            if livro not in ordem_livros:
                print("Livro invalido: ", livro)
                continue
            try:
                cap = int(parts[1])
                verso = int(parts[2])
            except ValueError:
                print("Capitulo ou versiculo invalido: ", v)
                continue
            versiculos_ordenados.append(f"{parts[0]}/{parts[1]}/{parts[2]}")

        #versiculos_ordenados = sorted(versiculos_ordenados, key=lambda x: (ordem_livros.index(x[0]), x[1], x[2]))
        versiculos_ordenados = sorted(versiculos_ordenados, key=lambda x: (ordem_livros.index(x.split("/")[0]), int(x.split("/")[1]), int(x.split("/")[2])))

        # Imprime a lista de versículos ordenada
        print(versiculos_ordenados)
        arquivo.write("\n".join(referencias_expandidas))
        with open(arquivoordenado, "w") as arquivood:
            arquivood.write("\n".join(versiculos_ordenados))
            arquivood.close()
        arquivo.close()
    extrair_e_salvar(arquivointermediario,arquivofinal)
    extrair_e_salvar(nomelivro+'od.txt', arquivofinalordenado+'')





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
referencia('Yochanan II',[1])
referencia('Yochanan III',[1])
referencia('Yehuda',[1])
referencia('Kefa II',[1,2,3])
referencia('Kefa I',[1,2,3,4,5])
referencia('Yaakov I',[1,2,3,4,5])
referencia('Gevurot',range(1,29))
referencia('Hisgalus',range(1,23))
#referencia('Yehudim in Moshiach',range(1,13))


