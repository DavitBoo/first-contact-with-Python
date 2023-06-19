import requests
from bs4 import BeautifulSoup
from collections import Counter
from nltk import ngrams
from textblob import TextBlob


# Obtener el contenido de la web
url = "https://www.elmundo.es/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}



try:
    r = requests.get(url, headers=headers)
    estadoWeb = r.status_code
    if estadoWeb == 200:
        print(f"La web {url} está en perfecto estado y respondiendo\n")
    else:
        print(f"La web {url} tiene problemas\n")
    
    # Extraer el texto
    soup = BeautifulSoup(r.content, "html.parser")
    text = soup.get_text()
    # Contar la frecuencia de las palabras
    words = text.split()
    counter = Counter(words)
    # Mostrar la frecuencia de una palabra específica
    word = "Sánchez"
    
    print(f"La palabra '{word}' aparece {counter[word]} veces en la web {url}")
    #palabras que se filtras, artículos, etc.
    stop_words = ["el", "la", "los", "las", "de", "del", "a", "ante", "con", "en", "entre", "por", "para", "sin", "sobre", "y", "o"]
    
    filtered_words = [(word, count) for word, count in counter.items() if word.lower() not in stop_words]
    filtered_counter = Counter(dict(filtered_words))
    most_common_words = filtered_counter.most_common(10)  # Obtener las 10 palabras más frecuentes

    print("Las palabras más frecuentes (excluyendo preposiciones, artículos y conectores) son:")
    for word, count in most_common_words:
        print(f"{word}: {count}")

    # enlaces encontrados
    links = soup.find_all("a")
    print("Enlaces encontrados:")
    for link in links:
        href = link.get("href")
        print(href)

    # Generar frases de 3 palabras
    n = 3
    phrases = ngrams(words, n)

    # Contar la frecuencia de las frases
    phrase_counter = Counter(phrases)

    # Mostrar las frases más frecuentes
    most_common_phrases = phrase_counter.most_common(10)
    print("Las frases más frecuentes son:")
    for phrase, count in most_common_phrases:
        phrase_str = " ".join(phrase)
        print(f"{phrase_str}: {count}")


    # Analisis de sentimientos
    # Análisis de sentimientos
    text_blob = TextBlob(text)
    sentiment = text_blob.sentiment
    polarity = sentiment.polarity
    subjectivity = sentiment.subjectivity
    
    print(f"\nAnálisis de sentimientos del texto:")
    print(f"Polaridad: {polarity:.2f}")
    print(f"Subjetividad: {subjectivity:.2f}")


except:
    print("Algo falla con esa web")
