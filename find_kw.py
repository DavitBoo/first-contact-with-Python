import requests
from bs4 import BeautifulSoup
from collections import Counter
from nltk import ngrams

from urllib.parse import urlparse, urljoin


def get_kw(url):
    # Obtener el contenido de la web
    # url = "https://www.elmundo.es/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    try:
        r = requests.get(url, headers=headers)
        # Extraer el texto
        soup = BeautifulSoup(r.content, "html.parser")
        text = soup.get_text()
        # Contar la frecuencia de las palabras
        words = text.split()
        counter = Counter(words)

        stop_words = ["\/", "\\", "|", "&", "sus", "tu", "se", "al", "más", "lo", "que", "un", "una", "su", "el",
                      "la", "los", "las", "de", "del", "a", "ante", "con", "en", "entre", "por", "para", "sin", "sobre", "y", "o"]

        filtered_words = [(word, count) for word, count in counter.items(
        ) if word.lower() not in stop_words]
        filtered_counter = Counter(dict(filtered_words))
        most_common_words = filtered_counter.most_common(1000)

        return most_common_words

    except:
        print("Algo falla con esa web")


def get_sentence(url):
    # url = "https://www.elmundo.es/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    try:
        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.content, "html.parser")
        text = soup.get_text()
        # Contar la frecuencia de las palabras
        words = text.split()
        n = 3
        phrases = ngrams(words, n)

        # Contar la frecuencia de las frases
        phrase_counter = Counter(phrases)

        print(phrase_counter)

        # # Mostrar las frases más frecuentes
        return phrase_counter.most_common(100)

    except:
        print("Algo falla con esa web")


def get_links(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        internal_links = []
        external_links = []
        domain = urlparse(url).netloc

        for link in soup.find_all('a'):
            href = link.get('href')
            parsed_href = urlparse(href)

            if parsed_href.netloc == domain or not parsed_href.scheme:
                # Internal link found
                internal_links.append(href)
            else:
                # External link found
                external_links.append(href)

        return internal_links, external_links

    except:
        print("Error al obtener los enlaces de la web")


def check_link_status(url):
    try:
        response = requests.head(url)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL {url}: {str(e)}")
        return None
