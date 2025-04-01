import sys
import os
import customtkinter as ctk
from tabs.scraping_tab import create_scraping_tab
from tabs.processing_tab import create_processing_tab
from tabs.search_tab import create_search_tab

# Agregar el directorio raíz del proyecto al PYTHONPATH
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(f"Directorio raíz del proyecto: {root_path}")
sys.path.append(root_path)

# Agregar la carpeta "modules" directamente al PYTHONPATH
modules_path = os.path.join(root_path, "modules")
sys.path.append(modules_path)

print("Rutas en sys.path:")
for path in sys.path:
    print(path)

def main():
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Scraping y Procesamiento de Texto")

    # Manejar el cierre de la ventana de forma segura
    def on_closing():
        print("Cerrando la aplicación...")
        app.quit()  # Detener el bucle principal de manera segura

    app.protocol("WM_DELETE_WINDOW", on_closing)

    tabview = ctk.CTkTabview(app)
    tabview.pack(pady=20, padx=20, fill="both", expand=True)

    # Crear las pestañas
    create_scraping_tab(tabview)
    create_processing_tab(tabview)
    create_search_tab(tabview)

    app.mainloop()

if __name__ == "__main__":
    main()