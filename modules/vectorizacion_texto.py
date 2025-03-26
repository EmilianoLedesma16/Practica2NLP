import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import os

# Obtener la ruta base
ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

# Cargar el corpus limpio (ya normalizado) desde la carpeta 'data'
df_arxiv = pd.read_csv(os.path.join(ruta_base, 'arxiv_clean_corpus.csv'), sep='\t', encoding='utf-8-sig')

# Crear un vectorizador binario
vectorizador_binario = CountVectorizer(binary=True)

# Crear un vectorizador TF (Term Frequency)
vectorizador_tf = CountVectorizer()

# Crear un vectorizador TF-IDF
vectorizador_tfidf = TfidfVectorizer()

# Función para generar y guardar las representaciones
def generar_y_guardar_vectorizacion(textos, nombre_archivo):
    # Vectorización binaria
    matriz_binaria = vectorizador_binario.fit_transform(textos)
    # Vectorización TF (Term Frequency)
    matriz_tf = vectorizador_tf.fit_transform(textos)
    # Vectorización TF-IDF
    matriz_tfidf = vectorizador_tfidf.fit_transform(textos)
    
    # Guardar como archivo pkl en la carpeta 'data'
    with open(nombre_archivo['binario'], 'wb') as f:
        pickle.dump(matriz_binaria, f)
    with open(nombre_archivo['tf'], 'wb') as f:
        pickle.dump(matriz_tf, f)
    with open(nombre_archivo['tfidf'], 'wb') as f:
        pickle.dump(matriz_tfidf, f)

    print("Archivos guardados correctamente")

# Obtener los textos del corpus
textos = df_arxiv['Cleaned_Text'].tolist()

# Definir los nombres de archivo para guardar las matrices vectoriales con rutas relativas
nombre_archivo = {
    'binario': os.path.join(ruta_base, 'arxiv_vector_binaria.pkl'),
    'tf': os.path.join(ruta_base, 'arxiv_vector_tf.pkl'),
    'tfidf': os.path.join(ruta_base, 'arxiv_vector_tfidf.pkl')
}

# Generar y guardar las representaciones vectoriales
generar_y_guardar_vectorizacion(textos, nombre_archivo)
