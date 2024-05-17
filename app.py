import requests
from bs4 import BeautifulSoup
import json

def rastrear_sitio_web(url): 
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status() 
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        
        enlaces = soup.find_all('a', href=True)[:100]  
        
        datos = {}
        
        for enlace in enlaces:
            href = enlace['href']
            if href.startswith('http'):  
                try:
                    respuesta_pagina = requests.get(href)
                    respuesta_pagina.raise_for_status()
                    pagina_soup = BeautifulSoup(respuesta_pagina.text, 'html.parser')
                    etiquetas_h1 = pagina_soup.find_all('h1')
                    etiquetas_p = pagina_soup.find_all('p')
                    if etiquetas_h1 or etiquetas_p:
                        datos[href] = [str(tag) for tag in etiquetas_h1 + etiquetas_p]
                    else:
                        datos[href] = []
                except requests.exceptions.RequestException as e:
                    print(f"Error al acceder a {href}: {e}")
                except Exception as e:
                    print(f"Error inesperado al procesar {href}: {e}")
                    
        return datos
    
    except requests.exceptions.RequestException as e:
        print("Error al realizar la solicitud:", e)
        return {}

def guardar_en_json(datos, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        json.dump(datos, archivo, indent=4)

if __name__ == "__main__":
    url = 'https://es.wikipedia.org/wiki/Wikipedia:Portada'
    nombre_archivo_salida = 'datos_sitio_web.json'
    
    datos_sitio_web = rastrear_sitio_web(url)
    guardar_en_json(datos_sitio_web, nombre_archivo_salida)