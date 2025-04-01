import sys
import os
import customtkinter as ctk

# Agregar la carpeta raíz del proyecto al PYTHONPATH
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_path)

# Agregar la carpeta "modules" directamente al PYTHONPATH
modules_path = os.path.join(root_path, "modules")
sys.path.append(modules_path)

from modules.scraping_arxiv import scrape_arxiv
from modules.scraping_pubmed import scrape_pubmed

print("Rutas en sys.path desde scraping_tab:")
for path in sys.path:
    print(path)

def ejecutar_scraping(opcion, seccion, num_articulos):
    try:
        # Convertir el número de artículos a entero
        num_articulos = int(num_articulos)

        if opcion == "arXiv":
            # Llamar a la función scrape_arxiv con los argumentos seleccionados
            scrape_arxiv(seccion, num_articulos)
            print(f"Scraping de {num_articulos} artículos de arXiv en la sección '{seccion}' completado.")
        elif opcion == "PubMed":
            # Llamar a la función scrape_pubmed con el número de artículos
            scrape_pubmed(num_articulos)
            print(f"Scraping de {num_articulos} artículos de PubMed completado.")
        else:
            print("Por favor, selecciona una fuente válida.")
    except ValueError:
        print("El número de artículos debe ser un número entero.")

def create_scraping_tab(tabview):
    tab1 = tabview.add("Scraping")

    # Etiqueta para la configuración
    label = ctk.CTkLabel(tab1, text="Configuración de Scraping")
    label.pack(pady=10)

    # Menú desplegable para seleccionar la fuente
    label_fuente = ctk.CTkLabel(tab1, text="Selecciona la fuente:")
    label_fuente.pack(pady=5)
    fuente_var = ctk.StringVar(value="arXiv")  # Valor por defecto
    dropdown_fuente = ctk.CTkOptionMenu(tab1, values=["arXiv", "PubMed"], variable=fuente_var)
    dropdown_fuente.pack(pady=5)

    # Menú desplegable para seleccionar la sección (solo para arXiv)
    label_seccion = ctk.CTkLabel(tab1, text="Selecciona la sección (solo para arXiv):")
    seccion_var = ctk.StringVar(value="Computation and Language")  # Valor por defecto
    dropdown_seccion = ctk.CTkOptionMenu(tab1, values=["Computation and Language", "Computer Vision"], variable=seccion_var)

    # Campo de entrada para el número de artículos
    label_num_articulos = ctk.CTkLabel(tab1, text="Número de artículos a scrapear:")
    label_num_articulos.pack(pady=5)
    entry_num_articulos = ctk.CTkEntry(tab1, placeholder_text="Ejemplo: 10")
    entry_num_articulos.pack(pady=5)

    # Botón para ejecutar el scraping
    button_scraping = ctk.CTkButton(
        tab1,
        text="Ejecutar Scraping",
        command=lambda: ejecutar_scraping(fuente_var.get(), seccion_var.get(), entry_num_articulos.get())
    )
    button_scraping.pack(pady=20)

    # Función para mostrar/ocultar el selector de sección
    def actualizar_seccion(*args):
        if fuente_var.get() == "arXiv":
            label_seccion.pack(pady=5)
            dropdown_seccion.pack(pady=5)
        else:
            label_seccion.pack_forget()
            dropdown_seccion.pack_forget()

    # Vincular el cambio de fuente a la función de actualización
    fuente_var.trace("w", actualizar_seccion)

    # Inicializar el estado del selector de sección
    actualizar_seccion()