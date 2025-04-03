import customtkinter as ctk
from tkinter import messagebox
import os
import pandas as pd
from modules.normalizacion_texto import procesar_corpus
from modules.vectorizacion_arxiv import generar_y_guardar_vectorizacion
from modules.vectorizacion_pubmed import generar_y_guardar_vectorizacion
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

            arxiv_clean = DATA_DIR / "arxiv_clean_corpus.csv"
            pubmed_clean = DATA_DIR / "pubmed_clean_corpus.csv"

            if not arxiv_clean.exists() or not pubmed_clean.exists():
                messagebox.showerror("Error", "Archivos de texto normalizado no encontrados.")
                return

            # Cargar los textos correctamente antes de pasarlos a la función
            df_arxiv = pd.read_csv(arxiv_clean, sep='\t', encoding='utf-8-sig')
            textos_arxiv = df_arxiv['Cleaned_Text'].tolist()  # Asegurar que es una lista
            df_pubmed = pd.read_csv(pubmed_clean, sep='\t', encoding='utf-8-sig')
            textos_pubmed = df_pubmed['Cleaned_Text'].tolist()

            # Verificar que los textos se cargaron bien
            print(f"Arxiv tiene {len(textos_arxiv)} documentos")
            print(f"PubMed tiene {len(textos_pubmed)} documentos")

            # Llamar a la función con los textos en lugar de la ruta del archivo
            
            generar_y_guardar_vectorizacion(textos_arxiv, str(PLK_DIR))
            generar_y_guardar_vectorizacion(textos_pubmed, str(PLK_DIR))

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
