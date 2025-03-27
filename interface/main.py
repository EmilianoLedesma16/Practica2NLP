import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

top_windows = {"normalizar": None, "vectorizar": None}

def ejecutar_scraping():
    opcion_tipo = tipo_var.get()
    try:
        cantidad = int(cantidad_var.get())
        rango_max = 150 if opcion_tipo == "arXiv" else 300
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
        script_path = os.path.join("modules", "scraping_arxiv.py")
        subprocess.run(["python", script_path, opcion_seccion, str(cantidad)])
    
    elif opcion_tipo == "PubMed":
        termino_busqueda = pubmed_var.get().strip()
        if not termino_busqueda:
            messagebox.showerror("Error", "Por favor, ingresa un término de búsqueda para PubMed")
            return
        script_path = os.path.join("modules", "scraping_pubmed.py")
        subprocess.run(["python", script_path, termino_busqueda, str(cantidad)])

def abrir_ventana_proceso(proceso):
    if top_windows[proceso] and tk.Toplevel.winfo_exists(top_windows[proceso]):
        return
    
    def iniciar_proceso():
        seleccion = tipo_var_proceso.get()
        if not seleccion:
            messagebox.showerror("Error", "Por favor, selecciona una opción")
            return
        script_name = "normalizacion_texto.py" if proceso == "normalizar" else "vectorizacion_texto.py"
        script_path = os.path.join("modules", script_name)
        subprocess.run(["python", script_path, seleccion])
        messagebox.showinfo("Éxito", f"{proceso.capitalize()} completado para {seleccion}")
        ventana.destroy()
        top_windows[proceso] = None
    
    ventana = tk.Toplevel(root)
    top_windows[proceso] = ventana
    ventana.title(f"{proceso.capitalize()} Texto")
    ventana.geometry("300x200")
    tipo_var_proceso = tk.StringVar()
    
    ttk.Label(ventana, text="Selecciona la fuente de datos:").pack(pady=10)
    ttk.Radiobutton(ventana, text="arXiv", variable=tipo_var_proceso, value="arXiv").pack()
    ttk.Radiobutton(ventana, text="PubMed", variable=tipo_var_proceso, value="PubMed").pack()
    ttk.Button(ventana, text="Iniciar", command=iniciar_proceso).pack(pady=20)

def actualizar_interfaz():
    for widget in frame_form.winfo_children():
        widget.pack_forget()
    tk.Label(frame_form, text="Selecciona el tipo de scraping:").pack()
    tk.Radiobutton(frame_form, text="arXiv", variable=tipo_var, value="arXiv", command=actualizar_interfaz).pack()
    tk.Radiobutton(frame_form, text="PubMed", variable=tipo_var, value="PubMed", command=actualizar_interfaz).pack()
    if tipo_var.get() == "arXiv":
        tk.Label(frame_form, text="Selecciona la sección de arXiv:").pack()
        seccion_menu.pack()
        cantidad_label_var.set("Número de artículos (1-150):")
    else:
        tk.Label(frame_form, text="Término de búsqueda en PubMed:").pack()
        pubmed_entry.pack()
        cantidad_label_var.set("Número de artículos (1-300):")
    cantidad_label.pack()
    cantidad_entry.pack()
    btn_ejecutar.pack(pady=10)

root = tk.Tk()
root.title("Scraping de Artículos Científicos")
root.geometry("400x350")

frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tipo_var = tk.StringVar(value="arXiv")
seccion_var = tk.StringVar()
pubmed_var = tk.StringVar()
cantidad_var = tk.StringVar()
cantidad_label_var = tk.StringVar(value="Número de artículos (1-150):")

seccion_menu = ttk.Combobox(frame_form, textvariable=seccion_var, state="readonly")
seccion_menu["values"] = ("Computation and Language", "Computer Vision")

pubmed_entry = tk.Entry(frame_form, textvariable=pubmed_var)

cantidad_label = tk.Label(frame_form, textvariable=cantidad_label_var)
cantidad_entry = tk.Entry(frame_form, textvariable=cantidad_var)

btn_ejecutar = tk.Button(root, text="Iniciar Scraping", command=ejecutar_scraping)
btn_ejecutar.pack(pady=10)

frame_botones = tk.Frame(root)
frame_botones.pack()

btn_normalizar = tk.Button(frame_botones, text="Normalizar Texto", command=lambda: abrir_ventana_proceso("normalizar"))
btn_normalizar.grid(row=0, column=0, padx=10, pady=10)

btn_vectorizar = tk.Button(frame_botones, text="Vectorizar Texto", command=lambda: abrir_ventana_proceso("vectorizar"))
btn_vectorizar.grid(row=0, column=1, padx=10, pady=10)

actualizar_interfaz()
root.mainloop()
