import requests # Solicitudes HTTP
from bs4 import BeautifulSoup # Analizar y extraer datos de HTML
import csv # Manipular CSV
import os # Traabajar rutas de archivos
import time # Medir tiempo
import pandas as pd # Trabajar con datos tabulares
import re # Expresiones regulares
import sys # Argumentos de línea de comandos
from dateutil import parser # Analizar fechas

# Descargar HTML
def descargar_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error al descargar la página: {response.status_code}")
        return None

# Limpia el texto eliminando espacios sobrantes
def limpiar_texto(texto):
    return " ".join(texto.split()).strip()

# Limpia los nombres de los autores
def limpiar_autores(lista_autores):
    autores_limpios = set()
    for autor in lista_autores:
        autor = limpiar_texto(autor)
        autor = autor.replace("et al.", "").strip()
        autor = " ".join([word for word in autor.split() if not word.isdigit()])
        autores_limpios.add(autor)
    return ", ".join(sorted(autores_limpios)).replace(",,", ",")

# Extraer DOI de la URL
def extraer_doi(url):
    match = re.search(r'pubmed.ncbi.nlm.nih.gov/(\d+)', url)
    return match.group(1) if match else "Unknown DOI"


def extraer_articulos_trending(max_articulos, pagina=1):
    base_url = "https://pubmed.ncbi.nlm.nih.gov/trending/"
    articulos = []
    
    while len(articulos) < max_articulos:
        url = base_url if pagina == 1 else f"{base_url}?page={pagina}"
        html = descargar_html(url)
        if not html:
            break
        
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('article', class_='full-docsum') # Busca todos los artículos en la página
        
        for item in items:
            if len(articulos) >= max_articulos:
                break
            titulo_tag = item.find('a', class_='docsum-title')
            # Extrae los elementos del HTML
            if titulo_tag:
                titulo = limpiar_texto(titulo_tag.text)
                link = "https://pubmed.ncbi.nlm.nih.gov" + titulo_tag['href']
                doi = extraer_doi(link)
                articulos.append((doi, titulo, link))
        
        if not items:
            break
        
        pagina += 1
        #time.sleep(0.5)  # Reduced sleep time
    
    return articulos

def extraer_detalles_articulo(doi, url):
    html = descargar_html(url)
    if not html:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    try:
        titulo = limpiar_texto(soup.find('h1', class_='heading-title').text)
        lista_autores = [a.text.strip() for a in soup.find_all('span', class_='authors-list-item')]
        autores = limpiar_autores(lista_autores)
        abstract = soup.find('div', class_='abstract-content')
        abstract = limpiar_texto(abstract.text) if abstract else "No abstract available"
        fecha = soup.find('span', class_='cit')
        fecha = limpiar_texto(fecha.text) if fecha else "Unknown Date"
        fecha = parser.parse(fecha).strftime('%d/%m/%Y')  # Reformat the date
        return [doi, titulo, autores, abstract, fecha]
    except:
        return None

def guardar_en_csv(nombre_archivo, datos):
    ruta_directorio = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    os.makedirs(ruta_directorio, exist_ok=True)
    ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)
    
    if os.path.exists(ruta_archivo) and os.stat(ruta_archivo).st_size > 0:
        try:
            df_existente = pd.read_csv(ruta_archivo, sep='\t', encoding='utf-8')
            doi_existentes = set(df_existente['DOI'].astype(str).tolist())
        except (pd.errors.EmptyDataError, KeyError):
            doi_existentes = set()
    else:
        doi_existentes = set()
    
    datos_filtrados = [row for row in datos if row[0] not in doi_existentes]
    
    with open(ruta_archivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        if os.stat(ruta_archivo).st_size == 0:
            writer.writerow(["DOI", "Title", "Authors", "Abstract", "Date"])
        writer.writerows(datos_filtrados)
    
    return len(datos_filtrados)

if __name__ == "__main__":
    max_articulos = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    inicio_tiempo = time.time()
    total_nuevos_articulos = 0
    pagina = 1
    
    while total_nuevos_articulos < max_articulos:
        articulos = extraer_articulos_trending(max_articulos - total_nuevos_articulos, pagina)
        #print(f"✅ Extraídos {len(articulos)} artículos de la sección Trending de PubMed")
        
        datos_pubmed = []
        for doi, titulo, link in articulos:
            if doi == "Unknown DOI":
                continue
            detalles = extraer_detalles_articulo(doi, link)
            if detalles:
                datos_pubmed.append(detalles)
            #time.sleep(1)
        
        nuevos_articulos = guardar_en_csv('pubmed_raw_corpus.csv', datos_pubmed)
        total_nuevos_articulos += nuevos_articulos
        pagina += 1
    
    fin_tiempo = time.time()
    tiempo_total = fin_tiempo - inicio_tiempo
    print(f"⏳ Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    print(f"✅ {total_nuevos_articulos} nuevos artículos guardados en ./data/pubmed_raw_corpus.csv")