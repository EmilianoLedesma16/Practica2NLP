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
vectorizador_binario_unigramas = CountVectorizer(binary=True, ngram_range=(1,1), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF (Term Frequency)
vectorizador_tf_unigramas = CountVectorizer(ngram_range=(1, 1), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF-IDF
vectorizador_tfidf_unigramas = TfidfVectorizer(ngram_range=(1, 1), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# ------------------------------------------------------------
# Vectorización usando bigramas

# Crear un vectorizador binario
vectorizador_binario_bigramas = CountVectorizer(binary=True, ngram_range=(2,2), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF (Term Frequency)
vectorizador_tf_bigramas = CountVectorizer(ngram_range=(2,2), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Crear un vectorizador TF-IDF
vectorizador_tfidf_bigramas = TfidfVectorizer(ngram_range=(2,2), token_pattern= r'(?u)\w+|\w+\n|\.|\¿|\?')

# Función para generar y guardar las representaciones
def generar_y_guardar_vectorizacion(textos, nombre_archivo):
    # Vectorización binaria
    matriz_binaria_unigramas = vectorizador_binario_unigramas.fit_transform(textos)
    # print("Matriz binaria generada")
    # print(vectorizador_binario.get_feature_names_out()[:500])
    # print(matriz_binaria)
    # print(matriz_binaria.toarray())
    
    # Vectorización TF (Term Frequency)
    matriz_tf_unigramas = vectorizador_tf_unigramas.fit_transform(textos)
    # print("Matriz tf generada")
    # print(vectorizador_tf.get_feature_names_out()[:500])
    # print(matriz_tf)
    # print(matriz_tf.toarray())

    # Vectorización TF-IDF
    matriz_tfidf_unigramas = vectorizador_tfidf_unigramas.fit_transform(textos)
    # print("Matriz tf-idf generada")
    # print(vectorizador_tfidf.get_feature_names_out()[:500])
    # print(matriz_tfidf)
    # print(matriz_tfidf.toarray())

    matriz_binaria_bigramas = vectorizador_binario_bigramas.fit_transform(textos)

    matriz_tf_bigramas = vectorizador_tf_bigramas.fit_transform(textos)

    matriz_tfidf_bigramas = vectorizador_tfidf_bigramas.fit_transform(textos)
    
    # Guardar como archivo pkl en la carpeta 'data'
    with open(nombre_archivo['binario_uni'], 'wb') as f:
        pickle.dump(matriz_binaria_unigramas, f)
    with open(nombre_archivo['tf_uni'], 'wb') as f:
        pickle.dump(matriz_tf_unigramas, f)
    with open(nombre_archivo['tfidf_uni'], 'wb') as f:
        pickle.dump(matriz_tfidf_unigramas, f)
    with open(nombre_archivo['binario_bi'], 'wb') as f:
        pickle.dump(matriz_binaria_bigramas, f)
    with open(nombre_archivo['tf_bi'], 'wb') as f:
        pickle.dump(matriz_tf_bigramas, f)
    with open(nombre_archivo['tfidf_bi'], 'wb') as f:
        pickle.dump(matriz_tfidf_bigramas, f)
    with open(nombre_archivo['binario_uni_vect'], 'wb') as f:
        pickle.dump(vectorizador_binario_unigramas, f)
    with open(nombre_archivo['tf_uni_vect'], 'wb') as f:
        pickle.dump(vectorizador_tf_unigramas, f)
    with open(nombre_archivo['tfidf_uni_vect'], 'wb') as f:
        pickle.dump(vectorizador_tfidf_unigramas, f)
    with open(nombre_archivo['binario_bi_vect'], 'wb') as f:
        pickle.dump(vectorizador_binario_bigramas, f)
    with open(nombre_archivo['tf_bi_vect'], 'wb') as f:
        pickle.dump(vectorizador_tf_bigramas, f)
    with open(nombre_archivo['tfidf_bi_vect'], 'wb') as f:
        pickle.dump(vectorizador_tfidf_bigramas, f)

    print("Archivos guardados correctamente")

# Obtener los textos del corpus
textos = df_arxiv['Cleaned_Text'].tolist()

# Definir los nombres de archivo para guardar las matrices vectoriales con rutas relativas
nombre_archivo = {
    'binario_uni': os.path.join(ruta_matrices, 'arxiv_vector_binaria_uni.pkl'),
    'tf_uni': os.path.join(ruta_matrices, 'arxiv_vector_tf_uni.pkl'),
    'tfidf_uni': os.path.join(ruta_matrices, 'arxiv_vector_tfidf_uni.pkl'),
    'binario_bi': os.path.join(ruta_matrices, 'arxiv_vector_binaria_bi.pkl'),
    'tf_bi': os.path.join(ruta_matrices, 'arxiv_vector_tf_bi.pkl'),
    'tfidf_bi': os.path.join(ruta_matrices, 'arxiv_vector_tfidf_bi.pkl'),
    'binario_uni_vect' : os.path.join(ruta_vectores, 'arxiv_vector_binaria_uni_vect.pkl'),
    'tf_uni_vect' : os.path.join(ruta_vectores, 'arxiv_vector_tf_uni_vect.pkl'),
    'tfidf_uni_vect' : os.path.join(ruta_vectores, 'arxiv_vector_tfidf_uni_vect.pkl'),
    'binario_bi_vect' : os.path.join(ruta_vectores, 'arxiv_vector_binaria_bi_vect.pkl'),
    'tf_bi_vect' : os.path.join(ruta_vectores, 'arxiv_vector_tf_bi_vect.pkl'),
    'tfidf_bi_vect' : os.path.join(ruta_vectores, 'arxiv_vector_tfidf_bi_vect.pkl')
}

# Generar y guardar las representaciones vectoriales
generar_y_guardar_vectorizacion(textos, nombre_archivo)
