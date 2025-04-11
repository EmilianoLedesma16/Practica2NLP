import customtkinter as ctk
from tkinter import messagebox
import os
import pandas as pd
from modules.normalizacion_texto import procesar_corpus
from modules.vectorizacion_arxiv import generar_y_guardar_vectorizacion as vectorizar_arxiv
from modules.vectorizacion_pubmed import generar_y_guardar_vectorizacion as vectorizar_pubmed

import pathlib

def create_processing_tab(tabview):
    tab = tabview.add("Procesamiento de Texto")
    
    # Widgets
    label = ctk.CTkLabel(tab, text="Procesamiento de Texto")
    label.pack(pady=10)
    
    def normalizar_textos():
        try:

            # Obtener ruta base de manera confiable
            BASE_DIR = pathlib.Path(__file__).parent.parent.parent
            DATA_DIR = BASE_DIR / "Practica2NLP/data"
        
            # Verificar si existe la carpeta data
            if not DATA_DIR.exists():
                messagebox.showerror("Error", f"No existe la carpeta 'data' en:\n{DATA_DIR}")
                return
            
            arxiv_input = DATA_DIR / "arxiv_raw_corpus.csv"
            pubmed_input = DATA_DIR / "pubmed_raw_corpus.csv"
        
            # Verificar archivos
            missing_files = []
            if not arxiv_input.exists(): missing_files.append(arxiv_input.name)
            if not pubmed_input.exists(): missing_files.append(pubmed_input.name)
        
            if missing_files:
                messagebox.showerror("Error", f"Faltan archivos:\n{', '.join(missing_files)}")
                return
            procesar_corpus(str(arxiv_input), str(DATA_DIR / "arxiv_clean_corpus.csv"))
            procesar_corpus(str(pubmed_input), str(DATA_DIR / "pubmed_clean_corpus.csv"))
            
            messagebox.showinfo("Éxito", "Normalización completada")
        except Exception as e:
            messagebox.showerror("Error", f"Error al normalizar:\n{str(e)}")

    def vectorizar_textos():
        try:
            BASE_DIR = pathlib.Path(__file__).parent.parent.parent
            DATA_DIR = BASE_DIR / "Practica2NLP/data"
            PLK_DIR = DATA_DIR / "plks"
            ruta_matrices_arxiv = os.path.join(PLK_DIR, "matrices", "arxiv")
            ruta_matrices_pubmed = os.path.join(PLK_DIR, "matrices", "pubmed")
            ruta_vectores_arxiv = os.path.join(PLK_DIR, "vectorizadores", "arxiv")
            ruta_vectores_pubmed = os.path.join(PLK_DIR, "vectorizadores", "pubmed")

            # Asegurar que las carpetas existen
            os.makedirs(ruta_matrices_arxiv, exist_ok=True)
            os.makedirs(ruta_matrices_pubmed, exist_ok=True)
            os.makedirs(ruta_vectores_arxiv, exist_ok=True)
            os.makedirs(ruta_vectores_pubmed, exist_ok=True)



            arxiv_clean = DATA_DIR / "arxiv_clean_corpus.csv"
            pubmed_clean = DATA_DIR / "pubmed_clean_corpus.csv"

            if not arxiv_clean.exists() or not pubmed_clean.exists():
                messagebox.showerror("Error", "Archivos de texto normalizado no encontrados.")
                return
            
            # Cargar los datos
            df_arxiv = pd.read_csv(arxiv_clean, sep='\t', encoding='utf-8')
            df_pubmed = pd.read_csv(pubmed_clean, sep='\t', encoding='utf-8')

            print("Columnas arXiv:", df_arxiv.columns)
            print("Columnas PubMed:", df_pubmed.columns)


            # Concatenacion de las columnas "Cleaned_Text" y "Cleaned_Abstract"
            df_arxiv["Cleaned_Text"] = df_arxiv["Cleaned_Title"].fillna('') + " " + df_arxiv["Cleaned_Abstract"].fillna('')
            df_pubmed["Cleaned_Text"] = df_pubmed["Cleaned_Title"].fillna('') + " " + df_pubmed["Cleaned_Abstract"].fillna('')
            
            # Convierte a listas para vectorizar
            textos_arxiv = df_arxiv["Cleaned_Text"].tolist()
            textos_pubmed = df_pubmed["Cleaned_Text"].tolist()

            print(f"Arxiv tiene {len(textos_arxiv)} documentos")
            print(f"PubMed tiene {len(textos_pubmed)} documentos")

            # Definicion de diccionario con los nombres de los archivos resultantes
            nombres_archivos_arxiv = {
                'binario_uni_titulo': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_binaria_uni_titulo.pkl'),
                'binario_uni_abstract': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_binaria_uni_abstract.pkl'),
                'tf_uni_titulo': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_tf_uni_titulo.pkl'),
                'tf_uni_abstract': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_tf_uni_abstract.pkl'),
                'tfidf_uni_titulo': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_tfidf_uni_titulo.pkl'),
                'tfidf_uni_abstract': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_tfidf_uni_abstract.pkl'),
                'binario_bi_titulo': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_binaria_bi_titulo.pkl'),
                'binario_bi_abstract': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_binaria_bi_abstract.pkl'),
                'tf_bi_titulo': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_tf_bi_titulo.pkl'),
                'tf_bi_abstract': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_tf_bi_abstract.pkl'),
                'tfidf_bi_titulo': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_tfidf_bi_titulo.pkl'),
                'tfidf_bi_abstract': os.path.join(ruta_matrices_arxiv, 'arxiv_vector_tfidf_bi_abstract.pkl'),
                
                'binario_uni_vect_titulo' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_binaria_uni_vect_titulo.pkl'),
                'binario_uni_vect_abstract' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_binaria_uni_vect_abstract.pkl'),
                'tf_uni_vect_titulo' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_tf_uni_vect_titulo.pkl'),
                'tf_uni_vect_abstract' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_tf_uni_vect_abstract.pkl'),
                'tfidf_uni_vect_titulo' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_tfidf_uni_vect_titulo.pkl'),
                'tfidf_uni_vect_abstract' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_tfidf_uni_vect_abstract.pkl'),
                'binario_bi_vect_titulo' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_binaria_bi_vect_titulo.pkl'),
                'binario_bi_vect_abstract' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_binaria_bi_vect_abstract.pkl'),
                'tf_bi_vect_titulo' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_tf_bi_vect_titulo.pkl'),
                'tf_bi_vect_abstract' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_tf_bi_vect_abstract.pkl'),
                'tfidf_bi_vect_titulo' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_tfidf_bi_vect_titulo.pkl'),
                'tfidf_bi_vect_abstract' : os.path.join(ruta_vectores_arxiv, 'arxiv_vector_tfidf_bi_vect_abstract.pkl')
            }
            
            nombres_archivos_pubmed = {
                k.replace('arxiv', 'pubmed'): v.replace('arxiv', 'pubmed').replace('arxiv/', 'pubmed/')
                for k, v in nombres_archivos_arxiv.items()
            }

            # Llamada correcta con los 3 argumentos
            vectorizar_pubmed(textos_pubmed, textos_pubmed, nombres_archivos_pubmed)
            vectorizar_arxiv(textos_arxiv, textos_arxiv, nombres_archivos_arxiv)


            messagebox.showinfo("Éxito", "Vectorización completada")
        except Exception as e:
            messagebox.showerror("Error", f"Error al vectorizar:\n{str(e)}")


    # Botones
    button_normalizar = ctk.CTkButton(
        tab,
        text="Normalizar Textos",
        command=normalizar_textos
    )
    button_normalizar.pack(pady=10)

    button_vectorizar = ctk.CTkButton(
        tab,
        text="Vectorizar Textos",
        command=vectorizar_textos
    )
    button_vectorizar.pack(pady=10)

    return tab
