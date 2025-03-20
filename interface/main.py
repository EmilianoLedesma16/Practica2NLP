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
        if not (1 <= cantidad <= 150):
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "El número de artículos debe ser un número entero entre 1 y 150")
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
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "modules", "scraping_pubmed.py")
        subprocess.run(["python", script_path, str(cantidad)])
        messagebox.showinfo("Éxito", f"Scraping completado: {cantidad} artículos descargados en data/pubmed_trending.csv")

def actualizar_interfaz():
    """Muestra los campos correctos según la fuente seleccionada."""
    if tipo_var.get() == "arXiv":
        frame_arxiv.pack(pady=5)
        frame_pubmed.pack_forget()
    else:
        frame_arxiv.pack_forget()
        frame_pubmed.pack(pady=5)

# Configurar ventana principal
root = tk.Tk()
root.title("Scraping de Artículos Científicos")
root.geometry("400x350")

# Tipo de scraping
tipo_var = tk.StringVar(value="arXiv")
tk.Label(root, text="Selecciona el tipo de scraping:").pack()
tk.Radiobutton(root, text="arXiv", variable=tipo_var, value="arXiv", command=actualizar_interfaz).pack()
tk.Radiobutton(root, text="PubMed", variable=tipo_var, value="PubMed", command=actualizar_interfaz).pack()

# Sección para arXiv
frame_arxiv = tk.Frame(root)
tk.Label(frame_arxiv, text="Selecciona la sección de arXiv:").pack()
seccion_var = tk.StringVar()
seccion_menu = ttk.Combobox(frame_arxiv, textvariable=seccion_var, state="readonly")
seccion_menu["values"] = ("Computation and Language", "Computer Vision")
seccion_menu.pack()
frame_arxiv.pack(pady=5)

# Sección para PubMed (Oculta por defecto)
frame_pubmed = tk.Frame(root)
frame_pubmed.pack_forget()

# Número de artículos
cantidad_var = tk.StringVar()
tk.Label(root, text="Número de artículos (1-150):").pack()
cantidad_entry = tk.Entry(root, textvariable=cantidad_var)
cantidad_entry.pack()

# Botón para ejecutar
btn_ejecutar = tk.Button(root, text="Iniciar Scraping", command=ejecutar_scraping)
btn_ejecutar.pack(pady=10)

root.mainloop()