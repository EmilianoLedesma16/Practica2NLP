#Scraping de arXiv con Python
import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import sys
import pandas as pd

# Descarga el código HTML de una página web.
def descargar_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error al descargar la página: {response.status_code}")
        return None

# Extrae los títulos y enlaces de los artículos de arXiv.
def extraer_articulos_arxiv(url_base, seccion, max_articulos, existentes):
    articulos = []
    pagina = 0
    
    while len(articulos) < max_articulos:
        url = f"{url_base}?skip={pagina * 50}&show=50"
        html = descargar_html(url)
        if not html:
            break
        
        soup = BeautifulSoup(html, 'html.parser')
        nuevos_articulos = []
        
        for dt in soup.find_all('dt'):
            enlace = dt.find('a', title='Abstract')
            if enlace:
                titulo = enlace.text.strip()
                link = f"https://arxiv.org{enlace['href']}"
                doi = link.replace('https://arxiv.org/abs/', '10.48550/arXiv.')
                if doi not in existentes:
                    nuevos_articulos.append((titulo, link, seccion))
        
        if not nuevos_articulos:
            break  # No hay más artículos disponibles
        
        articulos.extend(nuevos_articulos)
        pagina += 1
        time.sleep(1)
    
    return articulos[:max_articulos]

# Extrae DOI, autores, resumen y fecha de publicación desde arXiv.
def extraer_detalles_articulo(url, seccion):
    html = descargar_html(url)
    if not html:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    
    try:
        titulo = soup.find('h1', class_='title').text.replace('Title:', '').strip()
        autores = ', '.join([a.text.strip() for a in soup.select('div.authors a')])
        abstract = soup.find('blockquote', class_='abstract').text.replace('Abstract:', '').strip()
        fecha = soup.find('div', class_='dateline').text.replace('Submitted on', '').strip()
        doi = url.replace('https://arxiv.org/abs/', '10.48550/arXiv.')
        return [doi, titulo, autores, abstract, seccion, fecha]
    except:
        return None

# Guarda los datos en un archivo CSV.
def guardar_en_csv(nombre_archivo, datos, total_articulos):
    ruta_directorio = os.path.join(os.getcwd(), 'data')
    os.makedirs(ruta_directorio, exist_ok=True)
    ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)
    
    columnas = ["DOI", "Title", "Authors", "Abstract", "Section", "Date"]
    
    # Manejo de archivos vacíos y evitar duplicados
    if os.path.exists(ruta_archivo):
        try:
            if os.stat(ruta_archivo).st_size == 0:
                os.remove(ruta_archivo)  # Elimina archivo vacío
                existentes = set()
            else:
                df_existente = pd.read_csv(ruta_archivo, sep='\t', encoding='utf-8')
                existentes = set(df_existente['DOI'].tolist())
        except (pd.errors.EmptyDataError, FileNotFoundError):
            existentes = set()
    else:
        existentes = set()
    
    # Filtrar datos nuevos y limpiar texto
    datos_filtrados = []
    for row in datos:
        if row[0] not in existentes:
            row = [str(item).replace('\n', ' ').replace('\r', ' ') for item in row]  # Limpiar saltos de línea
            datos_filtrados.append(row)

    # Crear DataFrame final con datos limpios
    df_final = pd.DataFrame(datos_filtrados, columns=columnas)
    if os.path.exists(ruta_archivo):
        df_existente = pd.read_csv(ruta_archivo, sep='\t', encoding='utf-8')
        df_final = pd.concat([df_existente, df_final]).drop_duplicates(subset=['DOI']).reset_index(drop=True)
    
    df_final = df_final.iloc[:total_articulos]  # Mantener solo el total requerido
    
    # Guardar CSV sin comillas innecesarias
    df_final.to_csv(ruta_archivo, sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, escapechar='\\')
    
    print(f" Se han guardado {len(df_final)} artículos en {ruta_archivo}")

# Iniciar el cronómetro antes de comenzar la ejecución
inicio_tiempo = time.time()

# Leer parámetros de la interfaz
tipo_seccion = sys.argv[1]
cantidad_articulos = int(sys.argv[2])

# Diccionario para mapear la selección del usuario a las claves de arXiv
secciones_arxiv = {
    "Computation and Language": "cs.CL",
    "Computer Vision": "cs.CV"
}

codigo_seccion = secciones_arxiv.get(tipo_seccion)
if not codigo_seccion:
    print("Error: Sección no válida.")
    sys.exit(1)

# Leer artículos existentes
nombre_csv = 'arxiv_raw_corpus.csv'
ruta_archivo = os.path.join(os.getcwd(), 'data', nombre_csv)

if os.path.exists(ruta_archivo):
    try:
        if os.stat(ruta_archivo).st_size == 0:
            os.remove(ruta_archivo)
            existentes = set()
        else:
            df_existente = pd.read_csv(ruta_archivo, sep='\t', encoding='utf-8')
            existentes = set(df_existente['DOI'].tolist())
    except (pd.errors.EmptyDataError, FileNotFoundError):
        existentes = set()
else:
    existentes = set()

# Extraer artículos nuevos
url_arxiv = f"https://arxiv.org/list/{codigo_seccion}/recent"
articulos = extraer_articulos_arxiv(url_arxiv, tipo_seccion, cantidad_articulos, existentes)
print(f" Extraídos {len(articulos)} artículos de {tipo_seccion}")

datos_arxiv = []
for i, (titulo, link, seccion) in enumerate(articulos, 1):
    detalles = extraer_detalles_articulo(link, seccion)
    if detalles:
        datos_arxiv.append(detalles)
    time.sleep(1)  # Pausa para evitar bloqueos

# Guardar en CSV manteniendo el número total de artículos
guardar_en_csv(nombre_csv, datos_arxiv, len(existentes) + cantidad_articulos)

# Detener el cronómetro y calcular el tiempo total
fin_tiempo = time.time()
tiempo_total = fin_tiempo - inicio_tiempo
print(f" Tiempo total de ejecución: {tiempo_total:.2f} segundos")
print(" Datos guardados en data/arxiv_raw_corpus.csv\n")
# Fin del código
