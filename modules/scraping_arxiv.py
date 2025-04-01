# Módulo para extraer artículos de arXiv y guardarlos en un archivo CSV.
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import time
import sys
import pandas as pd
import re

# Descarga el código HTML de una página web.
def descargar_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error al descargar la página: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# Extrae los títulos y enlaces de los artículos de arXiv.
def extraer_articulos_arxiv(url_base, seccion, cantidad_nuevos, existentes):
    nuevos_encontrados = []
    pagina = 0
    revisados = set()

    while len(nuevos_encontrados) < cantidad_nuevos:
        url = f"{url_base}?skip={pagina * 50}&show=50"
        html = descargar_html(url)
        if not html:
            break

        soup = BeautifulSoup(html, 'html.parser')
        dt_tags = soup.find_all('dt')

        if not dt_tags:
            print("⚠️ No se encontraron más artículos en arXiv.")
            break

        for dt in dt_tags:
            enlace = dt.find('a', title='Abstract')
            if enlace:
                link = f"https://arxiv.org{enlace['href']}"
                doi = link.replace('https://arxiv.org/abs/', '10.48550/arXiv.')

                if doi not in existentes and doi not in [art[1] for art in nuevos_encontrados]:
                    titulo = enlace.text.strip()
                    nuevos_encontrados.append((titulo, link, seccion))

                    if len(nuevos_encontrados) >= cantidad_nuevos:
                        break

        pagina += 1
        time.sleep(0.5)

    return nuevos_encontrados




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
        fecha_raw = soup.find('div', class_='dateline').text.replace('Submitted on', '').strip()

        # Limpiar la cadena de fecha para eliminar texto adicional
        fecha_limpia = re.search(r'\d{1,2} \w{3} \d{4}', fecha_raw)  # Buscar patrón de fecha
        if fecha_limpia:
            fecha = datetime.strptime(fecha_limpia.group(), '%d %b %Y').strftime('%d/%m/%Y')
        else:
            print(f"Error procesando la fecha: {fecha_raw}")
            fecha = None

        doi = url.replace('https://arxiv.org/abs/', '10.48550/arXiv.')
        return [doi, titulo, autores, abstract, seccion, fecha]
    except Exception as e:
        print(f"Error extrayendo detalles de {url}: {e}")
        return None

# Guarda los datos en un archivo CSV acumulando nuevos sin duplicados.
def guardar_en_csv(nombre_archivo, datos, existentes):
    # Ruta del archivo CSV
    ruta_directorio = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    os.makedirs(ruta_directorio, exist_ok=True)
    ruta_archivo = os.path.join(ruta_directorio, nombre_archivo)

    columnas = ["DOI", "Title", "Authors", "Abstract", "Section", "Date"]

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

    print(f"Datos nuevos a guardar: {datos_filtrados}")

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

def scrape_arxiv(tipo_seccion, cantidad_articulos):
    # Iniciar el cronómetro antes de comenzar la ejecución
    inicio_tiempo = time.time()

    # Diccionario para mapear la selección del usuario a las claves de arXiv
    secciones_arxiv = {
        "Computation and Language": "cs.CL",
        "Computer Vision": "cs.CV"
    }

    codigo_seccion = secciones_arxiv.get(tipo_seccion)
    if not codigo_seccion:
        print("Error: Sección no válida.")
        return

    # Leer artículos existentes
    nombre_csv = 'arxiv_raw_corpus.csv'
    ruta_archivo = os.path.abspath(os.path.join("..", "data", nombre_csv))

    if os.path.exists(ruta_archivo):
        try:
            if os.stat(ruta_archivo).st_size == 0:
                print("El archivo CSV está vacío. Se eliminará.")
                os.remove(ruta_archivo)
                existentes = set()
            else:
                df_existente = pd.read_csv(ruta_archivo, sep=',', encoding='utf-8-sig')
                print(f"Contenido del archivo CSV:\n{df_existente}")
                existentes = set(df_existente['DOI'].tolist())
                print(f"DOIs existentes cargados: {existentes}")
        except (pd.errors.EmptyDataError, FileNotFoundError):
            print("Error al leer el archivo CSV. Se inicializará vacío.")
            existentes = set()
    else:
        print("El archivo CSV no existe. Se inicializará vacío.")
        existentes = set()

    # Extraer artículos nuevos
    url_arxiv = f"https://arxiv.org/list/{codigo_seccion}/recent"
    articulos = extraer_articulos_arxiv(url_arxiv, tipo_seccion, cantidad_articulos, existentes)
    print(f"- Extraídos {len(articulos)} artículos de {tipo_seccion}")

    datos_arxiv = []
    for i, (titulo, link, seccion) in enumerate(articulos, 1):
        detalles = extraer_detalles_articulo(link, seccion)
        if detalles:
            print(f"Detalles extraídos correctamente: {detalles}")
            datos_arxiv.append(detalles)
        else:
            print(f"Error al extraer detalles del artículo: {link}")
        time.sleep(0.5)

    print(f"DOIs existentes en el archivo: {existentes}")
    print(f"DOIs extraídos: {[row[0] for row in datos_arxiv]}")

    # Guardar en CSV manteniendo el número total de artículos
    guardar_en_csv(nombre_csv, datos_arxiv, existentes)

    # Detener el cronómetro y calcular el tiempo total
    fin_tiempo = time.time()
    tiempo_total = fin_tiempo - inicio_tiempo
    print(f"⏳ Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    print("✅ Datos guardados en data/arxiv_raw_corpus.csv")

if __name__ == "__main__":
    scrape_arxiv()