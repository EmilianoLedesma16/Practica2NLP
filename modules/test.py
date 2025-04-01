import spacy

# Cargar el modelo de spaCy
nlp = spacy.load("en_core_web_sm")  # Cambia a "en_core_web_trf" si deseas usar el modelo avanzado

# Lista de párrafos que deseas verificar
test_paragraphs = [
    "we introduce domain-specific BPE tokenizers for legal, financial, and governmental text. ",
    "Dace critique enhance llm reasoning stepwise natural language self capability large model particularly complex task require multi step logical deduction remain significant challenge traditional inference time scale method utilize scalar reward signal process evaluate candidate lack nuanced qualitative information essential understanding justify paper propose novel approach panel employ generate feedback guide level search rich human readable retain facilitate well inform decision making bypass need specific verifier associated training overhead make broadly applicable diverse experimental result challenging benchmark include aime gpqa demonstrate significantly performance outperform base code available http url support encourage future research promising field",
    "Specialized tokenizers for preprocessing applications remain understudied.",
    "Large language models have showcased remarkable capabilities in conversational AI.",
    "This approach bypasses the need for task-specific verifiers and the associated training overhead."
]

# Procesar cada párrafo y verificar su lematización
for paragraph in test_paragraphs:
    doc = nlp(paragraph)  # Procesar el párrafo
    lemas = [token.lemma_ for token in doc if not token.is_punct and not token.is_space]
    print(f"Párrafo original: {paragraph}")
    print(f"Lematización: {' '.join(lemas)}\n")
