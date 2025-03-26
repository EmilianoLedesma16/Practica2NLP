import csv
import pandas as pd
import spacy
import os
import re

# Cargar modelo de spaCy en inglés
nlp = spacy.load("en_core_web_sm")

POS_STOP_ALLOWED = {"DET", "PRON", "CCONJ", "SCONJ", "ADP"}

# Patrones para detectar tecnicismos que no deben separarse
PATRONES_ESPECIALES = [
    r'\b[A-Z]{2,}\d+[A-Z]*\b',        # KL3M, GPT4
    r'\b\d+[A-Z]{1,}\b',              # 4K, 16K
    r'\b[A-Z]+-\d+[a-zA-Z]?\b',       # GPT-4o, BPE-128k
]

# Eliminar LaTeX
def eliminar_latex(texto):
    texto = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', texto)
    texto = re.sub(r'\$.*?\$', '', texto)
    return texto

# Reemplazar tecnicismos por marcadores únicos (TOKEN0, TOKEN1...)
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

# Restaurar tokens técnicos al final
def restaurar_tecnicismos(tokens, protegidos):
    return [protegidos[token] if token in protegidos else token for token in tokens]

def normalizar_texto(texto):
    texto = eliminar_latex(texto)
    texto, protegidos = proteger_tecnicismos(texto)
    doc = nlp(texto)
    tokens_limpios = []

    for token in doc:
        if token.is_punct or token.is_space:
            continue

        if token.text in protegidos:
            tokens_limpios.append(token.text)
            continue

        if token.is_stop and token.pos_ in POS_STOP_ALLOWED:
            continue
        else:
            tokens_limpios.append(token.lemma_.lower())

    tokens_finales = restaurar_tecnicismos(tokens_limpios, protegidos)
    return " ".join(tokens_finales)

def procesar_corpus(ruta_entrada, ruta_salida):
    try:
        df = pd.read_csv(ruta_entrada, sep=',', encoding='utf-8-sig', on_bad_lines='skip')
        print(f"Cargando corpus desde: {ruta_entrada}")

        df['Texto_Completo'] = df['Title'].fillna('') + ". " + df['Abstract'].fillna('')
        df['Cleaned_Text'] = df['Texto_Completo'].apply(normalizar_texto)

        df.to_csv(ruta_salida, index=False, encoding='utf-8-sig', sep='\t')
        print(f"Corpus limpio guardado en: {ruta_salida}")
    except Exception as e:
        print(f"Error procesando el corpus: {e}")

if __name__ == "__main__":
    ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

    archivos = [
        ("arxiv_raw_corpus.csv", "arxiv_clean_corpus.csv"),
        ("pubmed_raw_corpus.csv", "pubmed_clean_corpus.csv")
    ]

    for entrada, salida in archivos:
        ruta_entrada = os.path.join(ruta_base, entrada)
        ruta_salida = os.path.join(ruta_base, salida)
        procesar_corpus(ruta_entrada, ruta_salida)
