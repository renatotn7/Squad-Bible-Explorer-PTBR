import csv
import requests

import re


# ...
#rabinos=['Rashi','Ramban','Ibn_Ezra','Sforno']
rabinos=['Targum_Jerusalem']
# Inicialize o objeto tradutor
from translate import Translator

translator = Translator(to_lang="pt")
# Inicie a iteração
ot_books = [ 'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1_Samuel', '2_Samuel', '1_Kings', '2_Kings', '1_Chronicles', '2_Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song_of_songs', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']
for rabino in rabinos:
    with open(rabino + '_ot.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Livro", "Capitulo", "Versiculo", "Onkelos"])
    for book in ot_books:
        book = book
        chapter = 1

        #url = f"https://www.sefaria.org/api/texts/{rabino}_on_{book}.1.1?commentary=0&context=1&pad=0&wrapLinks=1&wrapNamedEntities=1&multiple=0&stripItags=0&transLangPref=&firstAvailableRef=1&fallbackOnDefaultVersion=1"
        url = f"https://www.sefaria.org/api/texts/{rabino}, {book}.1?commentary=0&context=1&pad=0&wrapLinks=1&wrapNamedEntities=1&multiple=0&stripItags=0&transLangPref=&firstAvailableRef=1&fallbackOnDefaultVersion=1"
        print(url)
        while True:
            # Faça a requisição e carregue o json

            response = requests.get(url)
            data = response.json()

            # Verifique se o json contém dados de texto
            if "text" in data:
                # Traduza o texto do inglês para o português


                text = data["text"]
                #print(text)
                # Salve os dados no arquivo csv
                with open(rabino+'_ot.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)


                    verse = 1
                    for text in data["text"]:
                        #print(text)
                        #print(translator.translate(text))
                        if len(text.strip()) >0:
                            writer.writerow([book.strip(), str(chapter).strip(), str(verse).strip(), text.strip()])
                        verse += 1
                    #writer.writerow([book, chapter, verse, text])

            # Verifique se há uma próxima referência
            if "next" in data and data["next"] is not None:
                # Extraia a próxima referência
                print(data["next"])


                text =  data["next"]

                match = re.search(r'(Targum Jerusalem, )([A-Za-z ]+)( [0-9]+)', text)

                if match:
                    book = match.group(2)
                    print(book)
                    chapter = match.group(3)
                    print(chapter)
                    #verse = match.group(4)
                    print(book)
                    print(chapter)
                    url = f"https://www.sefaria.org/api/texts/{rabino}, {book}.{str(chapter).strip()}?commentary=0&context=1&pad=0&wrapLinks=1&wrapNamedEntities=1&multiple=0&stripItags=0&transLangPref=&firstAvailableRef=1&fallbackOnDefaultVersion=1"
                    print(url)
                else:
                    print("Não foi possível encontrar o padrão.")
                    break


            else:
                # Se não houver próxima referência, saia do loop
                break