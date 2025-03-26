import sys
import time
import requests
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import csv
import pandas as pd
import os

def obtener_doi(nbib_content):
    match = re.search(r'LID\s*-\s*([\w.\/\-\(\)]*)\s*\[doi\]', nbib_content, re.DOTALL)
    if match:
        doi = match.group(1)
        return doi
    else:
        second_try = re.search(r'AID\s*-\s*([\w.\/\-\(\)]*)\s*\[doi\]', nbib_content, re.DOTALL)
        if second_try:
            doi = second_try.group(1)
            return doi
        else:
            return None

def obtener_title(nbib_content):
    match = re.search(r'TI\s*-\s(.*?\.)', nbib_content, re.DOTALL)
    title = match.group(1) if match else None
    if title:
        title = " ".join(title.split())
    return title

def obtener_authors(nbib_content):
    match = re.findall(r'(?<!F)AU\s*-\s(.*?)\r?\n', nbib_content)
    authors = ", ".join(match) if match else None
    if authors:
        authors = " ".join(authors.split())
    return authors

def obtener_journal(nbib_content):
    match = re.search(r'JT\s*-\s(.*?)(?:\r?\n[A-Z]{2,4}\s*-\s|$)', nbib_content, re.DOTALL)
    journal = match.group(1) if match else None
    if journal:
        journal = " ".join(journal.split())
    return journal

def obtener_abstract(nbib_content):
    match = re.search(r'AB\s*-\s(.*?)(?:\r?\n[A-Z]{2,4}\s*-\s|$)', nbib_content, re.DOTALL)
    abstract = match.group(1) if match else None
    if abstract:
        abstract = " ".join(abstract.split())
    return abstract

def obtener_publication_date(nbib_content):
    match = re.search(r'DP\s*-\s(\d{4})(?: ([A-Za-z]{3}))?(?: (\d{1,2}))?', nbib_content)
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        
        month_dict = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        
        month = month_dict.get(month, '') if month else ''
        day = day.zfill(2) if day else ''
        
        publication_date = f"{day}/{month}/{year}"
        if not day:
            publication_date = f"/{month}/{year}" if month else f"//{year}"
    else:
        publication_date = "//"
    
    return publication_date

def descargar_html(url, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for _ in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error al descargar {url}: {e}. Reintentando...")
            time.sleep(2)
    return None

def extraer_articulos_trending(max_articulos, existentes):
    base_url = "https://pubmed.ncbi.nlm.nih.gov/trending/"
    articulos = []
    pagina = 1
    
    while len(articulos) < max_articulos:
        url = f"{base_url}?page={pagina}" if pagina > 1 else base_url
        html = descargar_html(url)
        if not html:
            break
            
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('article', class_='full-docsum')
        
        for item in items:
            if len(articulos) >= max_articulos:
                break
                
            titulo_tag = item.find('a', class_='docsum-title')
            if titulo_tag:
                link = "https://pubmed.ncbi.nlm.nih.gov" + titulo_tag['href'] + "?format=pubmed"
                doi = obtener_doi(descargar_html(link))
                if doi and doi not in existentes:
                    articulos.append(link)
        
        pagina += 1
        time.sleep(1)
    
    return articulos

def guardar_csv(nombre_archivo, datos, existentes):
    # Ruta del archivo CSV
    ruta_directorio = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    os.makedirs(ruta_directorio, exist_ok=True)
    ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)

    columnas = ['DOI', 'Title', 'Authors', 'Abstract', 'Journal', 'Date']

    # Leer datos existentes del archivo CSV
    if os.path.exists(ruta_archivo):
        try:
            df_existente = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig')
        except (pd.errors.EmptyDataError, FileNotFoundError):
            df_existente = pd.DataFrame(columns=columnas)
    else:
        df_existente = pd.DataFrame(columns=columnas)

    # Filtrar datos nuevos (evitar duplicados)
    datos_filtrados = []
    for row in datos:
        if row[0] not in existentes:  # row[0] es el DOI
            datos_filtrados.append(row)

    # Crear DataFrame con los datos nuevos
    df_nuevos = pd.DataFrame(datos_filtrados, columns=columnas)

    if df_nuevos.empty and df_existente.empty:
        print("No hay datos para guardar. El archivo CSV permanecerá vacío.")
        return

    # Combinar datos existentes con los nuevos
    df_final = pd.concat([df_existente, df_nuevos]).drop_duplicates(subset=['DOI']).reset_index(drop=True)

    # Guardar el DataFrame combinado en el archivo CSV
    df_final.to_csv(ruta_archivo, sep=',', index=False, encoding='utf-8-sig', quoting=csv.QUOTE_MINIMAL)

    print(f"✅ Se han guardado {len(df_nuevos)} artículos nuevos en {ruta_archivo}")

def parsear_nbib(nbib_content):
    doi = obtener_doi(nbib_content)
    title = obtener_title(nbib_content)
    authors = obtener_authors(nbib_content)
    journal = obtener_journal(nbib_content)
    abstract = obtener_abstract(nbib_content)
    publication_date = obtener_publication_date(nbib_content)
    return [doi, title, authors, abstract, journal, publication_date]

if __name__ == "__main__":
    max_articulos = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    inicio_tiempo = time.time()

    # Leer artículos existentes
    nombre_csv = 'pubmed_raw_corpus.csv'
    ruta_archivo = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', nombre_csv))

    if os.path.exists(ruta_archivo):
        try:
            if os.stat(ruta_archivo).st_size == 0:
                print("El archivo CSV está vacío. Se eliminará.")
                os.remove(ruta_archivo)
                existentes = set()
            else:
                df_existente = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig')
                existentes = set(df_existente['DOI'].tolist())
        except (pd.errors.EmptyDataError, FileNotFoundError):
            print("Error al leer el archivo CSV. Se inicializará vacío.")
            existentes = set()
    else:
        print("El archivo CSV no existe. Se inicializará vacío.")
        existentes = set()

    print("🔍 Extrayendo enlaces a artículos trending...")
    articulos = extraer_articulos_trending(max_articulos, existentes)

    datos_pubmed = []
    for url in articulos:
        html = descargar_html(url)
        if not html:
            continue

        soup = BeautifulSoup(html, 'html.parser')
        nbib_content = soup.find('pre', class_='article-details').text

        if nbib_content:
            datos_articulo = parsear_nbib(nbib_content)
            datos_pubmed.append(datos_articulo)

    # Guardar en CSV manteniendo el número total de artículos
    guardar_csv(nombre_csv, datos_pubmed, existentes)

    print(f"ℹ️ Tiempo total de ejecución: {time.time() - inicio_tiempo:.2f} segundos.")