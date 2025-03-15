import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import sys
import pandas as pd

def descargar_html(url):
    """Descarga el código HTML de una página web."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error al descargar la página: {response.status_code}")
        return None

def limpiar_texto(texto):
    """Limpia espacios extra, saltos de línea y caracteres especiales."""
    return " ".join(texto.split()).strip()

def limpiar_autores(lista_autores):
    """Limpia la lista de autores eliminando duplicados, números y espacios extra."""
    autores_limpios = set()
    for autor in lista_autores:
        autor = limpiar_texto(autor)
        autor = autor.replace("et al.", "").strip()
        autor = " ".join([word for word in autor.split() if not word.isdigit()])  # Elimina números
        autores_limpios.add(autor)
    return ", ".join(sorted(autores_limpios))  # Ordenamos para evitar desorden en el CSV

def corregir_doi(doi):
    """Corrige la URL del DOI eliminando barras extra."""
    return doi.replace("https:///", "https://").replace("//pubmed", "/pubmed")

def extraer_articulos_pubmed(termino_busqueda, max_articulos):
    """Busca artículos en PubMed y extrae títulos y enlaces."""
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    articulos = []
    pagina = 0
    
    while len(articulos) < max_articulos:
        url = f"{base_url}?term={termino_busqueda}&size=50&sort=date&page={pagina+1}"
        html = descargar_html(url)
        if not html:
            break
        
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('article', class_='full-docsum')
        
        for item in items:
            titulo_tag = item.find('a', class_='docsum-title')
            if titulo_tag:
                titulo = limpiar_texto(titulo_tag.text)
                link = base_url + titulo_tag['href']
                articulos.append((titulo, link))
        
        if not items:
            break  # No hay más artículos disponibles
        
        pagina += 1
        time.sleep(1)
    
    return articulos[:max_articulos]

def extraer_detalles_articulo(url):
    """Extrae autores, resumen y fecha de publicación desde un artículo de PubMed."""
    html = descargar_html(url)
    if not html:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        titulo = limpiar_texto(soup.find('h1', class_='heading-title').text)
        
        # Obtener lista de autores y limpiarlos
        lista_autores = [a.text.strip() for a in soup.find_all('span', class_='authors-list-item')]
        autores = limpiar_autores(lista_autores)
        
        # Obtener el resumen limpiando los saltos de línea
        abstract = soup.find('div', class_='abstract-content')
        abstract = limpiar_texto(abstract.text) if abstract else "No abstract available"
        
        # Obtener la fecha
        fecha = soup.find('span', class_='cit')
        fecha = limpiar_texto(fecha.text) if fecha else "Unknown Date"
        
        # Corregir DOI eliminando errores en la URL
        doi = corregir_doi(url)
        
        return [doi, titulo, autores, abstract, fecha]
    except:
        return None

def guardar_en_csv(nombre_archivo, datos):
    """Guarda los datos en un archivo CSV evitando duplicados y limpiando el formato."""
    ruta_directorio = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(ruta_directorio, exist_ok=True)
    ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)
    
    if os.path.exists(ruta_archivo) and os.stat(ruta_archivo).st_size > 0:
        try:
            df_existente = pd.read_csv(ruta_archivo, sep='\t', encoding='utf-8')
            doi_existentes = set(df_existente['DOI'].tolist())
        except pd.errors.EmptyDataError:
            print("⚠️ El archivo CSV estaba vacío, se creará desde cero.")
            doi_existentes = set()
    else:
        doi_existentes = set()
    
    datos_filtrados = [row for row in datos if row[0] not in doi_existentes]
    
    with open(ruta_archivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        if not os.path.exists(ruta_archivo) or os.stat(ruta_archivo).st_size == 0:
            writer.writerow(["DOI", "Title", "Authors", "Abstract", "Date"])
        writer.writerows(datos_filtrados)

# Iniciar ejecución
inicio_tiempo = time.time()

termino_busqueda = sys.argv[1]  # Tema de búsqueda (ejemplo: "machine learning")
cantidad_articulos = int(sys.argv[2])  # Número de artículos solicitados

# Extraer artículos
articulos = extraer_articulos_pubmed(termino_busqueda, cantidad_articulos)
print(f"✅ Extraídos {len(articulos)} artículos de PubMed sobre '{termino_busqueda}'")

datos_pubmed = []
for i, (titulo, link) in enumerate(articulos, 1):
    detalles = extraer_detalles_articulo(link)
    if detalles:
        datos_pubmed.append(detalles)
    time.sleep(1)

# Guardamos en CSV evitando duplicados
guardar_en_csv('pubmed_raw_corpus.csv', datos_pubmed)

# Detener el cronómetro y calcular el tiempo total
fin_tiempo = time.time()
tiempo_total = fin_tiempo - inicio_tiempo
print(f"⏳ Tiempo total de ejecución: {tiempo_total:.2f} segundos")
print("✅ Datos guardados en data/pubmed_raw_corpus.csv")
print("✅ Omi es gay y Rodas se la come\n")