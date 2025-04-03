import re
from modules.normalizacion_texto import normalizar_texto
import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity

def obtener_ruta_raiz():
    # __file__ es la ruta del archivo actual
    ruta_actual = os.path.abspath(__file__)
    # Subir hasta la raíz del proyecto (en este caso, dos niveles arriba)
    ruta_raiz = os.path.abspath(os.path.join(ruta_actual, "..", ".."))
    return ruta_raiz

def vectorizar_texto(texto, ngrama, vectorizacion):
    
    root_path = obtener_ruta_raiz()

    vectorizadores = {
        "Binario" : "binaria",
        "Frecuencia" : "tf",
        "TF-IDF" : "tfidf",
        "Bigramas" : "bi",
        "Unigramas" : "uni"
    }

    vectorizador_pubmed_path = f"{root_path}/data/plks/vectorizadores/pubmed/pubmed_vector_{vectorizadores[vectorizacion]}_{vectorizadores[ngrama]}_vect.pkl"
    vectorizador_arxiv_path = f"{root_path}/data/plks/vectorizadores/arxiv/arxiv_vector_{vectorizadores[vectorizacion]}_{vectorizadores[ngrama]}_vect.pkl"

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

    matriz_vectorizada_pubmed = vectorizador_pubmed.transform([texto])
    matriz_vectorizada_arxiv = vectorizador_arxiv.transform([texto])
    
    similitudes_pubmed = cosine_similarity(matriz_vectorizada_pubmed)

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

    texto = cargar_archivo_referencia(nombre_archivo, referencia)
    texto_normalizado = normalizar_texto(texto)

    # Vectorizar el texto normalizado
    matriz_vectorizada = vectorizar_texto(texto_normalizado, ngrama, vectorizacion)



