import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import os

# Obtener la ruta base
ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

# Cargar el corpus limpio (ya normalizado) desde la carpeta 'data'
df_pubmed = pd.read_csv(os.path.join(ruta_base, 'pubmed_clean_corpus.csv'), sep='\t', encoding='utf-8-sig')

# Crear un vectorizador binario
vectorizador_binario = CountVectorizer(binary=True, ngram_range=(1, 2))

# Crear un vectorizador TF (Term Frequency)
vectorizador_tf = CountVectorizer(ngram_range=(1, 2))

# Crear un vectorizador TF-IDF
vectorizador_tfidf = TfidfVectorizer(ngram_range=(1, 2))

# Función para generar y guardar las representaciones
def generar_y_guardar_vectorizacion(textos, nombre_archivo):
    # Vectorización binaria
    matriz_binaria = vectorizador_binario.fit_transform(textos)
    print("Matriz binaria generada")
    print(vectorizador_binario.get_feature_names_out()[:500])
    print(matriz_binaria)
    print(matriz_binaria.toarray())
    
    # Vectorización TF (Term Frequency)
    matriz_tf = vectorizador_tf.fit_transform(textos)
    print("Matriz tf generada")
    print(vectorizador_tf.get_feature_names_out()[:500])
    print(matriz_tf)
    print(matriz_tf.toarray())

    # Vectorización TF-IDF
    matriz_tfidf = vectorizador_tfidf.fit_transform(textos)
    print("Matriz tf-idf generada")
    print(vectorizador_tfidf.get_feature_names_out()[:500])
    print(matriz_tfidf)
    print(matriz_tfidf.toarray())
    
    # Guardar como archivo pkl en la carpeta 'data'
    with open(nombre_archivo['binario'], 'wb') as f:
        pickle.dump(matriz_binaria, f)
    with open(nombre_archivo['tf'], 'wb') as f:
        pickle.dump(matriz_tf, f)
    with open(nombre_archivo['tfidf'], 'wb') as f:
        pickle.dump(matriz_tfidf, f)

    print("Archivos guardados correctamente")

# Obtener los textos del corpus
textos = df_pubmed['Cleaned_Text'].tolist()

# Definir los nombres de archivo para guardar las matrices vectoriales con rutas relativas
nombre_archivo = {
    'binario': os.path.join(ruta_base, 'pubmed_vector_binaria.pkl'),
    'tf': os.path.join(ruta_base, 'pubmed_vector_tf.pkl'),
    'tfidf': os.path.join(ruta_base, 'pubmed_vector_tfidf.pkl')
}

# Generar y guardar las representaciones vectoriales
generar_y_guardar_vectorizacion(textos, nombre_archivo)
