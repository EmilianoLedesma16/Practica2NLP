import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import os

# Obtener la ruta base
ruta_data = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
ruta_matrices = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'plks', 'matrices','arxiv'))
ruta_vectores = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'plks', 'vectorizadores','arxiv'))

# Cargar el corpus limpio (ya normalizado) desde la carpeta 'data'
df_arxiv = pd.read_csv(os.path.join(ruta_data, 'arxiv_clean_corpus.csv'), sep='\t', encoding='utf-8-sig')

# ------------------------------------------------------------
# Vectorización usando unigramas

# Crear un vectorizador binario
vectorizador_binario_unigramas_titulo = CountVectorizer(binary=True, ngram_range=(1,1), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF (Term Frequency)
vectorizador_tf_unigramas_titulo = CountVectorizer(ngram_range=(1, 1), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF-IDF
vectorizador_tfidf_unigramas_titulo = TfidfVectorizer(ngram_range=(1, 1), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

vectorizador_binario_unigramas_abstract = CountVectorizer(binary=True, ngram_range=(1,1), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF (Term Frequency)
vectorizador_tf_unigramas_abstract = CountVectorizer(ngram_range=(1, 1), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF-IDF
vectorizador_tfidf_unigramas_abstract = TfidfVectorizer(ngram_range=(1, 1), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# ------------------------------------------------------------
# Vectorización usando bigramas

# Crear un vectorizador binario
vectorizador_binario_bigramas_titulo = CountVectorizer(binary=True, ngram_range=(2,2), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF (Term Frequency)
vectorizador_tf_bigramas_titulo = CountVectorizer(ngram_range=(2,2), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF-IDF
vectorizador_tfidf_bigramas_titulo = TfidfVectorizer(ngram_range=(2,2), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

vectorizador_binario_bigramas_abstract = CountVectorizer(binary=True, ngram_range=(2,2), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF (Term Frequency)
vectorizador_tf_bigramas_abstract = CountVectorizer(ngram_range=(2,2), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF-IDF
vectorizador_tfidf_bigramas_abstract = TfidfVectorizer(ngram_range=(2,2), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Función para generar y guardar las representaciones
def generar_y_guardar_vectorizacion(textos_titulo, textos_abstract, nombre_archivo):
    # Vectorización binaria
    matriz_binaria_unigramas_titulo = vectorizador_binario_unigramas_titulo.fit_transform(textos_titulo)
    matriz_binaria_unigramas_abstract = vectorizador_binario_unigramas_abstract.fit_transform(textos_abstract)
    # print("Matriz binaria generada")
    # print(vectorizador_binario.get_feature_names_out()[:500])
    # print(matriz_binaria)
    # print(matriz_binaria.toarray())
    
    # Vectorización TF (Term Frequency)
    matriz_tf_unigramas_titulo = vectorizador_tf_unigramas_titulo.fit_transform(textos_titulo)
    matriz_tf_unigramas_abstract = vectorizador_tf_unigramas_abstract.fit_transform(textos_abstract)
    # print("Matriz tf generada")
    # print(vectorizador_tf.get_feature_names_out()[:500])
    # print(matriz_tf)
    # print(matriz_tf.toarray())

    # Vectorización TF-IDF
    matriz_tfidf_unigramas_titulo = vectorizador_tfidf_unigramas_titulo.fit_transform(textos_titulo)
    matriz_tfidf_unigramas_abstract = vectorizador_tfidf_unigramas_abstract.fit_transform(textos_abstract)
    # print("Matriz tf-idf generada")
    # print(vectorizador_tfidf.get_feature_names_out()[:500])
    # print(matriz_tfidf)
    # print(matriz_tfidf.toarray())

    matriz_binaria_bigramas_titulo = vectorizador_binario_bigramas_titulo.fit_transform(textos_titulo)
    matriz_binaria_bigramas_abstract= vectorizador_binario_bigramas_abstract.fit_transform(textos_abstract)
    matriz_tf_bigramas_titulo = vectorizador_tf_bigramas_titulo.fit_transform(textos_titulo)
    matriz_tf_bigramas_abstract = vectorizador_tf_bigramas_abstract.fit_transform(textos_abstract)
    matriz_tfidf_bigramas_titulo = vectorizador_tfidf_bigramas_titulo.fit_transform(textos_titulo)
    matriz_tfidf_bigramas_abstract = vectorizador_tfidf_bigramas_abstract.fit_transform(textos_abstract)
    
    # Guardar como archivo pkl en la carpeta 'data'
    with open(nombre_archivo['binario_uni_titulo'], 'wb') as f:
        pickle.dump(matriz_binaria_unigramas_titulo, f)
    with open(nombre_archivo['binario_uni_abstract'], 'wb') as f:
        pickle.dump(matriz_binaria_unigramas_abstract, f)
    with open(nombre_archivo['tf_uni_titulo'], 'wb') as f:
        pickle.dump(matriz_tf_unigramas_titulo, f)
    with open(nombre_archivo['tf_uni_abstract'], 'wb') as f:
        pickle.dump(matriz_tf_unigramas_abstract, f)
    with open(nombre_archivo['tfidf_uni_titulo'], 'wb') as f:
        pickle.dump(matriz_tfidf_unigramas_titulo, f)
    with open(nombre_archivo['tfidf_uni_abstract'], 'wb') as f:
        pickle.dump(matriz_tfidf_unigramas_abstract, f)
    with open(nombre_archivo['binario_bi_titulo'], 'wb') as f:
        pickle.dump(matriz_binaria_bigramas_titulo, f)
    with open(nombre_archivo['binario_bi_abstract'], 'wb') as f:
        pickle.dump(matriz_binaria_bigramas_abstract, f)
    with open(nombre_archivo['tf_bi_titulo'], 'wb') as f:
        pickle.dump(matriz_tf_bigramas_titulo, f)
    with open(nombre_archivo['tf_bi_abstract'], 'wb') as f:
        pickle.dump(matriz_tf_bigramas_abstract, f)
    with open(nombre_archivo['tfidf_bi_titulo'], 'wb') as f:
        pickle.dump(matriz_tfidf_bigramas_titulo, f)
    with open(nombre_archivo['tfidf_bi_abstract'], 'wb') as f:
        pickle.dump(matriz_tfidf_bigramas_abstract, f)
    with open(nombre_archivo['binario_uni_vect_titulo'], 'wb') as f:
        pickle.dump(vectorizador_binario_unigramas_titulo, f)
    with open(nombre_archivo['binario_uni_vect_abstract'], 'wb') as f:
        pickle.dump(vectorizador_binario_unigramas_abstract, f)
    with open(nombre_archivo['tf_uni_vect_titulo'], 'wb') as f:
        pickle.dump(vectorizador_tf_unigramas_titulo, f)
    with open(nombre_archivo['tf_uni_vect_abstract'], 'wb') as f:
        pickle.dump(vectorizador_tf_unigramas_abstract, f)
    with open(nombre_archivo['tfidf_uni_vect_titulo'], 'wb') as f:
        pickle.dump(vectorizador_tfidf_unigramas_titulo, f)
    with open(nombre_archivo['tfidf_uni_vect_abstract'], 'wb') as f:
        pickle.dump(vectorizador_tfidf_unigramas_abstract, f)
    with open(nombre_archivo['binario_bi_vect_titulo'], 'wb') as f:
        pickle.dump(vectorizador_binario_bigramas_titulo, f)
    with open(nombre_archivo['binario_bi_vect_abstract'], 'wb') as f:
        pickle.dump(vectorizador_binario_bigramas_abstract, f)
    with open(nombre_archivo['tf_bi_vect_titulo'], 'wb') as f:
        pickle.dump(vectorizador_tf_bigramas_titulo, f)
    with open(nombre_archivo['tf_bi_vect_abstract'], 'wb') as f:
        pickle.dump(vectorizador_tf_bigramas_abstract, f)
    with open(nombre_archivo['tfidf_bi_vect_titulo'], 'wb') as f:
        pickle.dump(vectorizador_tfidf_bigramas_titulo, f)
    with open(nombre_archivo['tfidf_bi_vect_abstract'], 'wb') as f:
        pickle.dump(vectorizador_tfidf_bigramas_abstract, f)

    print("Archivos guardados correctamente")

# Obtener los textos del corpus
textos_titulo = df_arxiv['Cleaned_Title'].tolist()
textos_abstract = df_arxiv['Cleaned_Abstract'].tolist()

# Definir los nombres de archivo para guardar las matrices vectoriales con rutas relativas
nombre_archivo = {
    'binario_uni_titulo': os.path.join(ruta_matrices, 'arxiv_vector_binaria_uni_titulo.pkl'),
    'binario_uni_abstract': os.path.join(ruta_matrices, 'arxiv_vector_binaria_uni_abstract.pkl'),
    'tf_uni_titulo': os.path.join(ruta_matrices, 'arxiv_vector_tf_uni_titulo.pkl'),
    'tf_uni_abstract': os.path.join(ruta_matrices, 'arxiv_vector_tf_uni_abstract.pkl'),
    'tfidf_uni_titulo': os.path.join(ruta_matrices, 'arxiv_vector_tfidf_uni_titulo.pkl'),
    'tfidf_uni_abstract': os.path.join(ruta_matrices, 'arxiv_vector_tfidf_uni_abstract.pkl'),
    'binario_bi_titulo': os.path.join(ruta_matrices, 'arxiv_vector_binaria_bi_titulo.pkl'),
    'binario_bi_abstract': os.path.join(ruta_matrices, 'arxiv_vector_binaria_bi_abstract.pkl'),
    'tf_bi_titulo': os.path.join(ruta_matrices, 'arxiv_vector_tf_bi_titulo.pkl'),
    'tf_bi_abstract': os.path.join(ruta_matrices, 'arxiv_vector_tf_bi_abstract.pkl'),
    'tfidf_bi_titulo': os.path.join(ruta_matrices, 'arxiv_vector_tfidf_bi_titulo.pkl'),
    'tfidf_bi_abstract': os.path.join(ruta_matrices, 'arxiv_vector_tfidf_bi_abstract.pkl'),
    'binario_uni_vect_titulo' : os.path.join(ruta_vectores, 'arxiv_vector_binaria_uni_vect_titulo.pkl'),
    'binario_uni_vect_abstract' : os.path.join(ruta_vectores, 'arxiv_vector_binaria_uni_vect_abstract.pkl'),
    'tf_uni_vect_titulo' : os.path.join(ruta_vectores, 'arxiv_vector_tf_uni_vect_titulo.pkl'),
    'tf_uni_vect_abstract' : os.path.join(ruta_vectores, 'arxiv_vector_tf_uni_vect_abstract.pkl'),
    'tfidf_uni_vect_titulo' : os.path.join(ruta_vectores, 'arxiv_vector_tfidf_uni_vect_titulo.pkl'),
    'tfidf_uni_vect_abstract' : os.path.join(ruta_vectores, 'arxiv_vector_tfidf_uni_vect_abstract.pkl'),
    'binario_bi_vect_titulo' : os.path.join(ruta_vectores, 'arxiv_vector_binaria_bi_vect_titulo.pkl'),
    'binario_bi_vect_abstract' : os.path.join(ruta_vectores, 'arxiv_vector_binaria_bi_vect_abstract.pkl'),
    'tf_bi_vect_titulo' : os.path.join(ruta_vectores, 'arxiv_vector_tf_bi_vect_titulo.pkl'),
    'tf_bi_vect_abstract' : os.path.join(ruta_vectores, 'arxiv_vector_tf_bi_vect_abstract.pkl'),
    'tfidf_bi_vect_titulo' : os.path.join(ruta_vectores, 'arxiv_vector_tfidf_bi_vect_titulo.pkl'),
    'tfidf_bi_vect_abstract' : os.path.join(ruta_vectores, 'arxiv_vector_tfidf_bi_vect_abstract.pkl')
}

# Generar y guardar las representaciones vectoriales
generar_y_guardar_vectorizacion(textos_titulo, textos_abstract, nombre_archivo)
