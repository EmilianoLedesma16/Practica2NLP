import requests
from bs4 import BeautifulSoup
import csv
import os
import time

def descargar_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error al descargar la página: {response.status_code}")
        return None

# Extrae títulos y enlaces de los artículos desde múltiples páginas de arXiv.
def extraer_articulos_arxiv(url_base, seccion, max_articulos=150):
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

# Guarda los datos en un archivo CSV.
def guardar_en_csv(nombre_archivo, datos):
    ruta_directorio = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(ruta_directorio, exist_ok=True)  # Crear la carpeta si no existe
    ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)
    
    with open(ruta_archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(["DOI", "Title", "Authors", "Abstract", "Section", "Date"])
        writer.writerows(datos)

# Iniciar el cronómetro
inicio_tiempo = time.time()

# Secciones de arXiv a recolectar
secciones_arxiv = {
    "cs.CL": "Computation and Language",
    "cs.CV": "Computer Vision and Pattern Recognition"
}

datos_arxiv = []

for codigo, nombre in secciones_arxiv.items():
    url_arxiv = f"https://arxiv.org/list/{codigo}/recent"
    articulos = extraer_articulos_arxiv(url_arxiv, nombre)
    print(f"✅ Extraídos {len(articulos)} artículos de {nombre}")
    
    for i, (titulo, link, seccion) in enumerate(articulos, 1):
        detalles = extraer_detalles_articulo(link, seccion)
        if detalles:
            datos_arxiv.append(detalles)
        time.sleep(1)  # Pausa para evitar bloqueos por parte del Servidor jeje

# Guardamos en CSV en la carpeta data/ a nivel del proyecto
guardar_en_csv('arxiv_raw_corpus.csv', datos_arxiv)

# Detener el cronómetro y mostrar el tiempo transcurrido
fin_tiempo = time.time()
tiempo_total = fin_tiempo - inicio_tiempo
print("✅ Datos guardados en data/arxiv_raw_corpus.csv")
print(f" Tiempo transcurrido: {tiempo_total:.2f} segundos")

