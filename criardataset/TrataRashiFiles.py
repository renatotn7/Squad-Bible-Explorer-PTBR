import pandas as pd
import re
# carregando o arquivo CSV existente

rabinos=['Rashi','Ramban','Ibn_Ezra','Sforno']
siglas = {
    "Genesis": "Gn",
    "Exodus": "Êx",
    "Leviticus": "Lv",
    "Numbers": "Nm",
    "Deuteronomy": "Dt",
    "Joshua": "Js",
    "Judges": "Jz",
    "Ruth": "Rt",
    "1_Samuel": "1Sm",
    "2_Samuel": "2Sm",
    "1_Kings": "1Rs",
    "2_Kings": "2Rs",
    "1_Chronicles": "1Cr",
    "2_Chronicles": "2Cr",
    "Ezra": "Es",
    "Nehemiah": "Ne",
    "Esther": "Et",
    "Job": "Jó",
    "Psalms": "Sl",
    "Proverbs": "Pv",
    "Ecclesiastes": "Ec",
    "Song_of_songs": "Ct",
    "Isaiah": "Is",
    "Jeremiah": "Jr",
    "Lamentations": "Lm",
    "Ezekiel": "Ez",
    "Daniel": "Dn",
    "Hosea": "Os",
    "Joel": "Jl",
    "Amos": "Am",
    "Obadiah": "Ob",
    "Jonah": "Jn",
    "Micah": "Mq",
    "Nahum": "Na",
    "Habakkuk": "Hc",
    "Zephaniah": "Sf",
"Haggai": "Hg",
"Zechariah": "Zc",
"Malachi": "Ml"
}
for rabino in rabinos:
    print(rabino)
    df = pd.read_csv(rabino+"_ot.csv",sep=",")
    df["sigla"] = ""
    for index, row in df.iterrows():
        # recuperando o nome do livro
        livro = row["livro"]
        # adicionando a sigla correspondente na coluna "sigla"
        df.at[index, "sigla"] = siglas[livro]
        texto = row["texto"]
        texto = re.sub("<[^>]*>", "", texto)
        df.at[index, "texto"] = texto
        df.to_csv(rabino+"_ot.csv_siglas.csv", index=False)

        # Exibindo o dataframe
        print(df)