
# Importamos las librerías necesarias
import requests
from bs4 import BeautifulSoup
import json

# Función para extraer datos de una página web
def crawl_website(url): 
    try:
        response = requests.get(url)
        response.raise_for_status()  # manejo de errores HTTP
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = soup.find_all('a', href=True)[:100]  # encontrar todas las etiquetas <a> con enlaces
        
        data = {}
        
        for link in links:
            href = link['href']
            if href.startswith('http'):  # solo procesar enlaces HTTP
                try:
                    page_response = requests.get(href)
                    page_response.raise_for_status()
                    page_soup = BeautifulSoup(page_response.text, 'html.parser')
                    h1_tags = page_soup.find_all('h1')
                    p_tags = page_soup.find_all('p')
                    if h1_tags or p_tags:
                        data[href] = [str(tag) for tag in h1_tags + p_tags]
                    else:
                        data[href] = []
                except requests.exceptions.RequestException as e:
                    print(f"Error al acceder a {href}: {e}")
                except Exception as e:
                    print(f"Error inesperado al procesar {href}: {e}")
                    
        return data
    
    except requests.exceptions.RequestException as e:
        print("Error al realizar la solicitud:", e)
        return {}

def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    url = 'https://es.wikipedia.org/wiki/Wikipedia:Portada'
    output_filename = 'website_data.json'
    
    website_data = crawl_website(url)
    save_to_json(website_data, output_filename)
