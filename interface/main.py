import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

# Ejecuta el scraping según la opción seleccionada.
def ejecutar_scraping():
    opcion_tipo = tipo_var.get()
    
    # Validar la cantidad de artículos
    try:
        cantidad = int(cantidad_var.get())
        rango_max = 150 if opcion_tipo == "arXiv" else 300  # Ajustar el límite según la fuente
        if not (1 <= cantidad <= rango_max):
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", f"El número de artículos debe ser un número entero entre 1 y {rango_max}")
        return
    
    if opcion_tipo == "arXiv":
        opcion_seccion = seccion_var.get()
        if opcion_seccion not in ["Computation and Language", "Computer Vision"]:
            messagebox.showerror("Error", "Por favor, selecciona una sección válida de arXiv")
            return
        
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "modules", "scraping_arxiv.py")
        subprocess.run(["python", script_path, opcion_seccion, str(cantidad)])
        messagebox.showinfo("Éxito", f"Scraping completado: {cantidad} artículos descargados en data/arxiv_raw_corpus.csv")
    
    elif opcion_tipo == "PubMed":
        termino_busqueda = pubmed_var.get().strip()
        if not termino_busqueda:
            messagebox.showerror("Error", "Por favor, ingresa un término de búsqueda para PubMed")
            return
        
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "modules", "scraping_pubmed.py")
        subprocess.run(["python", script_path, termino_busqueda, str(cantidad)])
        messagebox.showinfo("Éxito", f"Scraping completado: {cantidad} artículos descargados en data/pubmed_raw_corpus.csv")

def actualizar_interfaz():
    """Muestra los campos correctos según la fuente seleccionada y actualiza el rango de artículos."""
    for widget in frame_form.winfo_children():
        widget.pack_forget()  # Oculta todos los elementos antes de actualizar

    # Título
    tk.Label(frame_form, text="Selecciona el tipo de scraping:").pack()
    tk.Radiobutton(frame_form, text="arXiv", variable=tipo_var, value="arXiv", command=actualizar_interfaz).pack()
    tk.Radiobutton(frame_form, text="PubMed", variable=tipo_var, value="PubMed", command=actualizar_interfaz).pack()
    
    # Sección específica de la fuente
    if tipo_var.get() == "arXiv":
        tk.Label(frame_form, text="Selecciona la sección de arXiv:").pack()
        seccion_menu.pack()
        cantidad_label_var.set("Número de artículos (1-150):")
    else:
        tk.Label(frame_form, text="Término de búsqueda en PubMed:").pack()
        pubmed_entry.pack()
        cantidad_label_var.set("Número de artículos (1-300):")
    
    # Campo de cantidad de artículos
    cantidad_label.pack()
    cantidad_entry.pack()

    # Botón de ejecución siempre debajo de los campos visibles
    btn_ejecutar.pack(pady=10)

# Configurar ventana principal
root = tk.Tk()
root.title("Scraping de Artículos Científicos")
root.geometry("400x350")

# Frame principal para los campos de entrada
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

# Variables
tipo_var = tk.StringVar(value="arXiv")
seccion_var = tk.StringVar()
pubmed_var = tk.StringVar()
cantidad_var = tk.StringVar()
cantidad_label_var = tk.StringVar(value="Número de artículos (1-150):")

# Dropdown de secciones de arXiv
seccion_menu = ttk.Combobox(frame_form, textvariable=seccion_var, state="readonly")
seccion_menu["values"] = ("Computation and Language", "Computer Vision")

# Entrada de texto para PubMed
pubmed_entry = tk.Entry(frame_form, textvariable=pubmed_var)

# Campo de cantidad de artículos
cantidad_label = tk.Label(frame_form, textvariable=cantidad_label_var)
cantidad_entry = tk.Entry(frame_form, textvariable=cantidad_var)

# Botón para ejecutar scraping (siempre debajo)
btn_ejecutar = tk.Button(root, text="Iniciar Scraping", command=ejecutar_scraping)

# Cargar la interfaz inicial
actualizar_interfaz()

root.mainloop()