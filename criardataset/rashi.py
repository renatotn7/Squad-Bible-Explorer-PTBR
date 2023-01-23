import csv
import requests

import re


# ...
#rabinos=['Rashi','Ramban','Ibn_Ezra','Sforno']
rabinos=['Onkelos','Targum_Jonathan']
# Inicialize o objeto tradutor
from translate import Translator

translator = Translator(to_lang="pt")
# Inicie a iteração
ot_books = [ 'Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1_Samuel', '2_Samuel', '1_Kings', '2_Kings', '1_Chronicles', '2_Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song_of_songs', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']
for rabino in rabinos:
    for book in ot_books:
        book = book
        chapter = 1
        verse = 1
        #url = f"https://www.sefaria.org/api/texts/{rabino}_on_{book}.1.1?commentary=0&context=1&pad=0&wrapLinks=1&wrapNamedEntities=1&multiple=0&stripItags=0&transLangPref=&firstAvailableRef=1&fallbackOnDefaultVersion=1"
        url = f"https://www.sefaria.org/api/texts/{rabino}_on_{book}.1?commentary=0&context=1&pad=0&wrapLinks=1&wrapNamedEntities=1&multiple=0&stripItags=0&transLangPref=&firstAvailableRef=1&fallbackOnDefaultVersion=1"

        while True:
            # Faça a requisição e carregue o json

            response = requests.get(url)
            data = response.json()

            # Verifique se o json contém dados de texto
            if "text" in data:
                # Traduza o texto do inglês para o português


                text = data["text"]
                print(text)
                # Salve os dados no arquivo csv
                with open(rabino+'_ot.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([book, chapter, verse, text])

            # Verifique se há uma próxima referência
            if "next" in data and data["next"] is not None:
                # Extraia a próxima referência
                print(data["next"])


                text =  data["next"]

                match = re.search(r'('+rabino+' on )([A-Za-z ]+)( [0-9]+):([0-9]+)', text)
                if match:
                    book = match.group(2)
                    chapter = match.group(3)
                    verse = match.group(4)
                    print(book)
                    print(chapter)
                    url = f"https://www.sefaria.org/api/texts/{rabino}_on_{book}.{chapter}.{verse}?commentary=0&context=1&pad=0&wrapLinks=1&wrapNamedEntities=1&multiple=0&stripItags=0&transLangPref=&firstAvailableRef=1&fallbackOnDefaultVersion=1"
                else:
                    print("Não foi possível encontrar o padrão.")
                    break


            else:
                # Se não houver próxima referência, saia do loop
                break