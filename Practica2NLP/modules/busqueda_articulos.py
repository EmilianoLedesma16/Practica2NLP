import re
from modules.normalizacion_texto import normalizar_texto
import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

vectorizadores = {
        "Binario" : "binaria",
        "Frecuencia" : "tf",
        "TF-IDF" : "tfidf",
        "Bigramas" : "bi",
        "Unigramas" : "uni",
        "Abstract" : "abstract",
        "Title" : "titulo",
    }

def obtener_ruta_raiz():
    # __file__ es la ruta del archivo actual
    ruta_actual = os.path.abspath(__file__)
    # Subir hasta la raíz del proyecto (en este caso, dos niveles arriba)
    ruta_raiz = os.path.abspath(os.path.join(ruta_actual, "..", ".."))
    return ruta_raiz

root_path = obtener_ruta_raiz()

def vectorizar_texto(texto, ngrama, vectorizacion, referencia):

    vectorizador_pubmed_path = f"{root_path}/data/plks/vectorizadores/pubmed/pubmed_vector_{vectorizadores[vectorizacion]}_{vectorizadores[ngrama]}_vect_{vectorizadores[referencia]}.pkl"
    vectorizador_arxiv_path = f"{root_path}/data/plks/vectorizadores/arxiv/arxiv_vector_{vectorizadores[vectorizacion]}_{vectorizadores[ngrama]}_vect_{vectorizadores[referencia]}.pkl"

    try:
        with open(vectorizador_pubmed_path, 'rb') as file:
            vectorizador_pubmed = pickle.load(file)
    except FileNotFoundError:
        print(f"El vectorizador de PubMed no se encontró en la ruta: {vectorizador_pubmed_path}")
        return None
    
    try:
        with open(vectorizador_arxiv_path, 'rb') as file:
            vectorizador_arxiv = pickle.load(file)
    except FileNotFoundError:
        print(f"El vectorizador de arXiv no se encontró en la ruta: {vectorizador_arxiv_path}")
        return None

    matrices = [None, None]

    matrices[0] = vectorizador_pubmed.transform([texto])
    matrices[1] = vectorizador_arxiv.transform([texto])
    
    return matrices

def cargar_archivo_referencia(ruta_archivo, referencia):

    if (ruta_archivo.endswith(".ris")):
        return procesar_ris(ruta_archivo, referencia)
    elif (ruta_archivo.endswith(".bib")):
        return procesar_bib(ruta_archivo, referencia)
    else:
        raise ValueError("Formato de archivo no soportado. Solo se admiten archivos .ris y .bib.")
    
def procesar_ris(ruta_archivo, referencia):
    
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        contenido = file.read()

    # Buscar el título (campo "TI  -") al inicio de una línea
    title = re.search(r'^TI\s*-\s*(.+)', contenido, re.MULTILINE)
    # Buscar el abstract (campo "AB  -") y capturar todas las líneas hasta el siguiente campo
    abstract = re.search(r'^AB\s*-\s*(.+?)(?=\n[A-Z]{2}\s*-|\nER\s*-)', contenido, re.MULTILINE | re.DOTALL)

    # Extraer y limpiar el título
    if title:
        titulo = title.group(1).strip()
    else:
        titulo = None

    # Extraer y limpiar el abstract
    if abstract:
        # Procesar cada línea del abstract para eliminar espacios adicionales
        lineas = abstract.group(1).splitlines()
        resumen = " ".join(linea.strip() for linea in lineas).strip()
    else:
        resumen = None

    if referencia == "Title":
        return titulo
    elif referencia == "Abstract":
        return resumen

def procesar_bib(ruta_archivo, referencia):
    """
    Procesa un archivo BibTeX y extrae el título y el abstract.
    """
    with open(ruta_archivo, 'r', encoding="UTF-8") as file:
        contenido = file.read()

    # Buscar el título (campo "title = {...}")
    title = re.search(r'title\s*=\s*\{(.*?)\}', contenido, re.DOTALL)
    # Buscar el abstract (campo "abstract = {...}")
    abstract = re.search(r'abstract\s*=\s*\{(.*?)\}', contenido, re.DOTALL)

    # Extraer y limpiar el título
    if title:
        titulo = title.group(1).strip()
    else:
        titulo = None

    # Extraer y limpiar el abstract
    if abstract:
        resumen = abstract.group(1).strip()
    else:
        resumen = None

    if referencia == "Title":
        return titulo
    elif referencia == "Abstract":
        return resumen


def buscar_articulos(nombre_archivo, ngrama, vectorizacion, referencia):
    
    matriz_pubmed_path = f"{root_path}/data/plks/matrices/pubmed/pubmed_vector_{vectorizadores[vectorizacion]}_{vectorizadores[ngrama]}_{vectorizadores[referencia]}.pkl"
    matriz_arxiv_path = f"{root_path}/data/plks/matrices/arxiv/arxiv_vector_{vectorizadores[vectorizacion]}_{vectorizadores[ngrama]}_{vectorizadores[referencia]}.pkl"

    pubmed_csv_path = f"{root_path}/data/pubmed_raw_corpus.csv"
    arxiv_csv_path = f"{root_path}/data/arxiv_raw_corpus.csv"

    try:
        pubmed_data = pd.read_csv(pubmed_csv_path)
        arxiv_data = pd.read_csv(arxiv_csv_path)
    except FileNotFoundError as e:
        print(f"No se pudo cargar el archivo CSV: {e}")
        return None, None

    try:
        with open(matriz_pubmed_path, 'rb') as file:
            matriz_pubmed = pickle.load(file)
    except FileNotFoundError:
        print(f"La matriz de PubMed no se encontró en la ruta: {matriz_pubmed_path}")
        return None, None

    try:
        with open(matriz_arxiv_path, 'rb') as file:
            matriz_arxiv = pickle.load(file)
    except FileNotFoundError:
        print(f"La matriz de arXiv no se encontró en la ruta: {matriz_arxiv_path}")
        return None, None

    titulos_pubmed = pubmed_data["Title"].tolist()
    titulos_arxiv = arxiv_data["Title"].tolist()

    texto = cargar_archivo_referencia(nombre_archivo, referencia)
    if not texto:
        print("No se pudo extraer texto del archivo seleccionado.")
        return None, None

    texto_normalizado = normalizar_texto(texto)

    matriz_vectorizada = vectorizar_texto(texto_normalizado, ngrama, vectorizacion, referencia)
    if matriz_vectorizada is None:
        print("No se pudo vectorizar el texto.")
        return None, None

    similitudes_pubmed = cosine_similarity(matriz_vectorizada[0], matriz_pubmed)
    similitudes_arxiv = cosine_similarity(matriz_vectorizada[1], matriz_arxiv)

    resultados_pubmed = sorted(enumerate(similitudes_pubmed[0]), key=lambda x: x[1], reverse=True)
    resultados_arxiv = sorted(enumerate(similitudes_arxiv[0]), key=lambda x: x[1], reverse=True)

    # Crear listas de resultados con títulos y similitudes
    resultados_pubmed_formateados = [(titulos_pubmed[idx], similitud) for idx, similitud in resultados_pubmed[:10]]
    resultados_arxiv_formateados = [(titulos_arxiv[idx], similitud) for idx, similitud in resultados_arxiv[:10]]

    return resultados_pubmed_formateados, resultados_arxiv_formateados