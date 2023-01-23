import requests
from bs4 import BeautifulSoup

# Função para extrair o texto de uma passagem específica da Bíblia
def extrair_passagem(livro, cap, ver):
    # URL da passagem a ser extraída
    url = f'https://www.bibliaonline.com.br/nvi/{livro}/{cap}/{ver}'

    # Fazendo a requisição
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extrair o texto da passagem
    passagem = soup.find('p', class_='jss35')
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
    with open(arquivo, 'r') as f:
        for linha in f:
            passagens.append(linha.strip())
    return passagens

# Função principal
def extrair_e_salvar(arquivo):
    passagens = ler_passagens(arquivo)
    textos_passagens = []
    for passagem in passagens:
        livro, cap, ver = passagem.split('/')
        texto = extrair_passagem(livro, cap, ver)
        textos_passagens.append(texto)
    salvar_passagens("Pedro.txt", textos_passagens)

# Executando a função principal
extrair_e_salvar('pedro1.txt')
