import csv
import pandas as pd
import spacy
import os

# Cargar modelo de spaCy en inglés
nlp = spacy.load("en_core_web_sm")

def normalizar_texto(texto):
    doc = nlp(texto)
    tokens_limpios = [
        token.lemma_.lower() for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return " ".join(tokens_limpios)

def procesar_corpus(ruta_entrada, ruta_salida):
    try:
        df = pd.read_csv(ruta_entrada, sep=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, encoding='utf-8-sig',on_bad_lines='skip')
        
        print(f"Cargando corpus desde: {ruta_entrada}")

        # Combinar título y resumen
        df['Texto_Completo'] = df['Title'].fillna('') + ". " + df['Abstract'].fillna('')

        # Aplicar normalización
        df['Cleaned_Text'] = df['Texto_Completo'].apply(normalizar_texto)

        # Guardar corpus limpio
        df.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
        print(f"Corpus limpio guardado en: {ruta_salida}")
    except Exception as e:
        print(f"Error procesando el corpus: {e}")

if __name__ == "__main__":
    # Rutas de entrada/salida
    ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

    archivos = [
        ("arxiv_raw_corpus.csv", "arxiv_clean_corpus.csv"),
        ("pubmed_raw_corpus.csv", "pubmed_clean_corpus.csv")
    ]

    for entrada, salida in archivos:
        ruta_entrada = os.path.join(ruta_base, entrada)
        ruta_salida = os.path.join(ruta_base, salida)
        procesar_corpus(ruta_entrada, ruta_salida)
