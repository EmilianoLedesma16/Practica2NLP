import customtkinter as ctk
from tkinter import filedialog
from modules.busqueda_articulos import buscar_articulos  # Asegúrate de que esta función esté definida en el módulo correspondiente

def cargar_archivo():
    # Abrir un cuadro de diálogo para seleccionar un archivo .ris o .bibtex
    archivo = filedialog.askopenfilename(
        filetypes=[("Archivos RIS", "*.ris"), ("Archivos BibTeX", "*.bib")],
        title="Selecciona un archivo RIS o BibTeX"
    )
    if archivo:
        print(f"Archivo seleccionado: {archivo}")
        return archivo
    else:
        print("No se seleccionó ningún archivo.")
        return None


def create_search_tab(tabview):
    tab3 = tabview.add("Búsqueda")

    # Etiqueta para la configuración
    label = ctk.CTkLabel(tab3, text="Configuración de Búsqueda")
    label.pack(pady=10)

    # Variable para almacenar la ruta del archivo seleccionado
    archivo_var = [None]  # Usamos una lista para que sea mutable

    # Etiqueta para mostrar el archivo seleccionado
    archivo_label = ctk.CTkLabel(tab3, text="Por favor selecciona un archivo", wraplength=400)
    archivo_label.pack(pady=5)

    # Función para seleccionar un archivo
    def seleccionar_archivo():
        archivo = cargar_archivo()
        if archivo:
            archivo_var[0] = archivo
            archivo_label.configure(text=f"Archivo seleccionado: {archivo}")
            print(archivo_var[0])
        else:
            archivo_label.configure(text="No se seleccionó ningún archivo.")

    # Botón para cargar un archivo RIS o BibTeX
    button_cargar_archivo = ctk.CTkButton(
        tab3,
        text="Cargar Archivo RIS o BibTeX",
        command=seleccionar_archivo
    )
    button_cargar_archivo.pack(pady=10)

    # Menú desplegable para seleccionar unigramas o bigramas
    label_ngrama = ctk.CTkLabel(tab3, text="Selecciona el tipo de N-Grama:")
    label_ngrama.pack(pady=5)
    ngrama_var = ctk.StringVar(value="Unigramas")  # Valor por defecto
    dropdown_ngrama = ctk.CTkOptionMenu(tab3, values=["Unigramas", "Bigramas"], variable=ngrama_var)
    dropdown_ngrama.pack(pady=5)

    # Menú desplegable para seleccionar el método de vectorización
    label_vectorizacion = ctk.CTkLabel(tab3, text="Selecciona el método de vectorización:")
    label_vectorizacion.pack(pady=5)
    vectorizacion_var = ctk.StringVar(value="TF-IDF")  # Valor por defecto
    dropdown_vectorizacion = ctk.CTkOptionMenu(tab3, values=["Binario", "Frecuencia", "TF-IDF"], variable=vectorizacion_var)
    dropdown_vectorizacion.pack(pady=5)

    # Menú desplegable para seleccionar la referencia (abstract o título)
    label_referencia = ctk.CTkLabel(tab3, text="Selecciona la referencia para la comparación:")
    label_referencia.pack(pady=5)
    referencia_var = ctk.StringVar(value="Abstract")  # Valor por defecto
    dropdown_referencia = ctk.CTkOptionMenu(tab3, values=["Abstract", "Title"], variable=referencia_var)
    dropdown_referencia.pack(pady=5)

    # Botón para ejecutar la búsqueda
    button_buscar = ctk.CTkButton(
        tab3,
        text="Ejecutar Búsqueda",
        command=lambda: buscar_articulos(
        archivo_var[0],  # Archivo seleccionado
        ngrama_var.get(),  # Tipo de N-Grama
        vectorizacion_var.get(),  # Método de vectorización
        referencia_var.get()  # Referencia (abstract o título)
    )
    )
    button_buscar.pack(pady=20)