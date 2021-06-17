import re
def regex_clean_file(conteudo):
    conteudo = re.sub(r'’|“|‘|”', '', conteudo)
    conteudo = re.sub(r'\d', '', conteudo)
    conteudo = re.sub(r'\n\.', '\n', conteudo)
    conteudo = re.sub(r'\n ', '\n', conteudo)
    conteudo = re.sub(r'\r\n', '\n', conteudo)
    conteudo = re.sub(r'\n\n', '\n', conteudo)
    return conteudo