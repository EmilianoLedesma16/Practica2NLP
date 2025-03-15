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
def extraer_articulos_arxiv(url_base, seccion, max_articulos):
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

# Guarda los datos en un archivo CSV evitando duplicados.
def guardar_en_csv(nombre_archivo, datos):
    ruta_directorio = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(ruta_directorio, exist_ok=True)  # Crear la carpeta si no existe
    ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)
    
    # Cargar datos existentes si el archivo ya existe
    if os.path.exists(ruta_archivo):
        try:
            df_existente = pd.read_csv(ruta_archivo, sep='\t', encoding='utf-8')
            doi_existentes = set(df_existente['DOI'].tolist())
        except pd.errors.EmptyDataError:
            print("El archivo CSV está vacío, se creará uno nuevo.")
            doi_existentes = set()
    else:
        doi_existentes = set()
    
    # Filtrar artículos nuevos
    datos_filtrados = [row for row in datos if row[0] not in doi_existentes]
    
    # Guardar datos combinados
    with open(ruta_archivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        if not os.path.exists(ruta_archivo) or os.stat(ruta_archivo).st_size == 0:
            writer.writerow(["DOI", "Title", "Authors", "Abstract", "Section", "Date"])
        writer.writerows(datos_filtrados)

# Iniciar el cronómetro antes de comenzar la ejecución
inicio_tiempo = time.time()

# Leer parámetros de la interfaz
tipo_seccion = sys.argv[1]  # Computation and Language o Computer Vision
cantidad_articulos = int(sys.argv[2])  # Número de artículos solicitados

# Diccionario para mapear la selección del usuario a las claves de arXiv
secciones_arxiv = {
    "Computation and Language": "cs.CL",
    "Computer Vision": "cs.CV"
}

codigo_seccion = secciones_arxiv.get(tipo_seccion)
if not codigo_seccion:
    print("Error: Sección no válida.")
    sys.exit(1)

# Extraer artículos
url_arxiv = f"https://arxiv.org/list/{codigo_seccion}/recent"
articulos = extraer_articulos_arxiv(url_arxiv, tipo_seccion, cantidad_articulos)
print(f"✅ Extraídos {len(articulos)} artículos de {tipo_seccion}")

datos_arxiv = []
for i, (titulo, link, seccion) in enumerate(articulos, 1):
    detalles = extraer_detalles_articulo(link, seccion)
    if detalles:
        datos_arxiv.append(detalles)
    time.sleep(1)  # Pausa para evitar bloqueos

# Guardamos en CSV evitando duplicados
guardar_en_csv('arxiv_raw_corpus.csv', datos_arxiv)

# Detener el cronómetro y calcular el tiempo total
fin_tiempo = time.time()
tiempo_total = fin_tiempo - inicio_tiempo
print(f"⏳ Tiempo total de ejecución: {tiempo_total:.2f} segundos")
print("✅ Datos guardados en data/arxiv_raw_corpus.csv")
print("✅ Omi es gay y el Rodas es puto\n")