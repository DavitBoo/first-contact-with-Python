from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

from datetime import datetime

from find_kw import get_kw, get_sentence
import requests

def validate_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.head(url, headers=headers)
        
        if response.status_code == 200:
            return True
        else:
            print(f"La URL {url} no es accesible. Verifica la URL e intenta nuevamente.")
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL {url}: {str(e)}")
    
    return False

url = input('Inseta la URL para analizar las palabras clave. ej: www.google.com:\n')
query_url = 'https://' + url

if(validate_url(query_url)):
    

    wb = Workbook()
    ws = wb.active
    ws.title = "Keywords"

    headings = ['Keyword', 'Times Repeated']
    ws.append(headings)

    word_list = get_kw(query_url)
    print(word_list)

    coords = 1
    for word, count in word_list:
            print(f"{word}: {count}")
            coords += 1 
            ws.append([word, count])

    sentence_list = get_sentence(query_url)

    ws2 = wb.create_sheet(title='Sentences')
    ws2.append(['Sentence', 'Times Repeated'])

    for phrase, count in sentence_list:
                phrase_str = " ".join(phrase)
                ws2.append([phrase_str, count])

    current_timestamp = datetime.now()
    formatted_timestamp = current_timestamp.strftime('%Y%m%d%H%M%S')

    for col in range(1, 3):
        ws[get_column_letter(col) + '1'].font = Font(bold=True, color="0066AAFF")
        ws2[get_column_letter(col) + '1'].font = Font(bold=True, color="0066AAFF")

    if "/" in url:
        url = url.split("/", 1)[0]

    wb.save(f'{formatted_timestamp}-{url}.xlsx')
else:
    print("La URL proporcionada no es válida o no se puede acceder a ella. Verifica la URL e intenta nuevamente.")