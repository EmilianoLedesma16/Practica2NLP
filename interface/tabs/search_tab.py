import customtkinter as ctk
from tkinter import filedialog

def cargar_archivo():
    # Abrir un cuadro de diálogo para seleccionar un archivo .ris o .bibtex
    archivo = filedialog.askopenfilename(
        filetypes=[("Archivos RIS", "*.ris"), ("Archivos BibTeX", "*.bibtex")],
        title="Selecciona un archivo RIS o BibTeX"
    )
    if archivo:
        print(f"Archivo seleccionado: {archivo}")
        return archivo
    else:
        print("No se seleccionó ningún archivo.")
        return None

def ejecutar_busqueda(archivo, ngrama, vectorizacion):
    if not archivo:
        print("Por favor, selecciona un archivo antes de continuar.")
        return

    print(f"Ejecutando búsqueda con las siguientes opciones:")
    print(f"- Archivo: {archivo}")
    print(f"- N-Grama: {ngrama}")
    print(f"- Vectorización: {vectorizacion}")
    # Aquí puedes llamar a la función que procesará el archivo y realizará la búsqueda

def create_search_tab(tabview):
    tab3 = tabview.add("Búsqueda")

    # Etiqueta para la configuración
    label = ctk.CTkLabel(tab3, text="Configuración de Búsqueda")
    label.pack(pady=10)

    # Botón para cargar un archivo RIS o BibTeX
    archivo_var = [None]  # Usamos una lista para almacenar el archivo seleccionado
    def seleccionar_archivo():
        archivo_var[0] = cargar_archivo()

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

    # Botón para ejecutar la búsqueda
    button_buscar = ctk.CTkButton(
        tab3,
        text="Ejecutar Búsqueda",
        command=lambda: ejecutar_busqueda(
            archivo_var[0],  # Archivo cargado
            ngrama_var.get(),  # Tipo de N-Grama
            vectorizacion_var.get()  # Método de vectorización
        )
    )
    button_buscar.pack(pady=20)