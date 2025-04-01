import customtkinter as ctk

def normalizar_texto():
    # Lógica para normalizar texto
    print("Normalizando texto...")

def vectorizar_texto():
    # Lógica para vectorizar texto
    print("Vectorizando texto...")

def create_processing_tab(tabview):
    tab2 = tabview.add("Procesamiento de Texto")

    # Widgets específicos de la pestaña
    label = ctk.CTkLabel(tab2, text="Procesamiento de Texto")
    label.pack(pady=10)

    button_normalizar = ctk.CTkButton(tab2, text="Normalizar Texto", command=normalizar_texto)
    button_normalizar.pack(pady=10)

    button_vectorizar = ctk.CTkButton(tab2, text="Vectorizar Texto", command=vectorizar_texto)
    button_vectorizar.pack(pady=10)