import pandas as pd
import spacy
import os
import re
import nltk
from nltk.stem import WordNetLemmatizer

# Categorías gramaticales cuya stopword se debe eliminar
CATEGORIAS_STOP_POS = {"DET", "ADP", "CCONJ", "PRON", "AUX", "PART","INTJ", "SCONJ", "NUM"}  # Artículos, preposiciones, conjunciones, pronombres, verbos auxiliares y particles


# Descargar recursos de NLTK
nltk.download('wordnet')
nltk.download('omw-1.4')  # soporte multilingüe

# Inicializar el lematizador de WordNet
lemmatizer = WordNetLemmatizer()

# Cargar modelo de spaCy en inglés (modelo más grande para mayor precisión)
nlp = spacy.load("en_core_web_md")  # Cambiado de en_core_web_sm a en_core_web_md

# Patrones para detectar tecnicismos que no deben separarse
PATRONES_ESPECIALES = [
    r'\b[A-Z]{2,}\d+[A-Z]*\b',        # KL3M, GPT4
    r'\b\d+[A-Z]{1,}\b',              # 4K, 16K
    r'\b[A-Z]+-\d+[a-zA-Z]?\b',       # GPT-4o, BPE-128k
    r'\b[a-zA-Z]+-[a-zA-Z]+\b'        # age-associated, il6-dependent
]

# Función para eliminar fragmentos de LaTeX
def eliminar_latex(texto):
    texto = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', texto)  # Eliminar comandos LaTeX como \textbf{...}
    texto = re.sub(r'\$.*?\$', '', texto)              # Eliminar expresiones matemáticas $...$
    texto = re.sub(r'\s*-\s*', '-', texto)            # Conservar guiones en palabras compuestas
    return texto

# Función para proteger tecnicismos
def proteger_tecnicismos(texto):
    protegidos = {}
    i = 0
    for patron in PATRONES_ESPECIALES:
        for match in re.findall(patron, texto):
            placeholder = f"TOKEN{i}"
            protegidos[placeholder] = match
            texto = texto.replace(match, placeholder)
            i += 1
    return texto, protegidos

# Función para restaurar tecnicismos
def restaurar_tecnicismos(tokens, protegidos):
    return [protegidos[token] if token in protegidos else token for token in tokens]

# Función para eliminar redundancias en el texto
def eliminar_redundancias(texto):
    palabras = texto.split()
    texto_sin_redundancias = " ".join(sorted(set(palabras), key=palabras.index))
    return texto_sin_redundancias

# Función para lematizar con NLTK como respaldo
def lematizar_con_respaldo(token):
    # Primero intenta con spaCy
    lema_spacy = token.lemma_.lower()
    
    # Si spaCy no lematiza correctamente o el token es plural, usa NLTK
    if lema_spacy == token.text.lower() or token.tag_ == "NNS":  # "NNS" es el tag para sustantivos plurales
        lema_nltk = lemmatizer.lemmatize(token.text.lower(), pos='n')  # Forzar sustantivo
        return lema_nltk
    
    return lema_spacy

# Función para normalizar texto
def normalizar_texto(texto, eliminar_redundancias_flag=True):
    # Asefurar que todo esté en minúsculas
    #texto = texto.lower()
    
    # Eliminar LaTeX
    texto = eliminar_latex(texto)
    
    # Proteger tecnicismos
    texto, protegidos = proteger_tecnicismos(texto)
    
    # Procesar texto con spaCy
    doc = nlp(texto)
    tokens_limpios = []

    for token in doc:
        # Ignorar puntuación, espacios y stopwords
        if token.is_punct or token.is_space:
            continue
        
        #Eliminar stopwords según la categoría gramatical
        if token.pos_ in CATEGORIAS_STOP_POS:
            continue 

        # Conservar tecnicismos protegidos
        if token.text in protegidos:
            tokens_limpios.append(token.text)
            continue

        # Lematizar con respaldo de NLTK
        tokens_limpios.append(lematizar_con_respaldo(token))

    # Restaurar tecnicismos
    tokens_finales = restaurar_tecnicismos(tokens_limpios, protegidos)

    # Validar que todos los tecnicismos se restauraron
    for token in tokens_finales:
        if token.startswith("TOKEN"):
            print(f"Advertencia: El tecnicismo {token} no fue restaurado correctamente.")
    
    # Eliminar redundancias si es necesario
    if eliminar_redundancias_flag:
        texto_final = eliminar_redundancias(" ".join(tokens_finales))
    else:
        texto_final = " ".join(tokens_finales)
    
    return texto_final

# Función para procesar el corpus
def procesar_corpus(ruta_entrada, ruta_salida):
    try:
        # Leer el archivo CSV de entrada
        df = pd.read_csv(ruta_entrada, sep=',', encoding='utf-8-sig', on_bad_lines='skip')
        print(f"Cargando corpus desde: {ruta_entrada}")

        # Validar que las columnas necesarias existan
        if 'Title' not in df.columns or 'Abstract' not in df.columns:
            raise ValueError("El archivo de entrada debe contener las columnas 'Title' y 'Abstract'.")

        # Combinar título y resumen en una nueva columna
        #df['Texto_Completo'] = df['Title'].fillna('') + ". " + df['Abstract'].fillna('')

        # Aplicar la normalización al texto completo
        df['Cleaned_Title'] = df['Title'].fillna('').apply(normalizar_texto)
        df['Cleaned_Abstract'] = df['Abstract'].fillna('').apply(normalizar_texto)

        # Guardar el DataFrame limpio en el archivo de salida
        df.to_csv(ruta_salida, index=False, encoding='utf-8-sig', sep='\t')
        print(f"Corpus limpio guardado en: {ruta_salida}")
    except Exception as e:
        print(f"Error procesando el corpus: {e}")
        raise

if __name__ == "__main__":
    # Definir rutas de entrada y salida
    ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

    archivos = [
        ("arxiv_raw_corpus.csv", "arxiv_clean_corpus.csv"),
        ("pubmed_raw_corpus.csv", "pubmed_clean_corpus.csv")
    ]

    for entrada, salida in archivos:
        ruta_entrada = os.path.join(ruta_base, entrada)
        ruta_salida = os.path.join(ruta_base, salida)
        procesar_corpus(ruta_entrada, ruta_salida)
