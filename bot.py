from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from llama_cpp import Llama 
import os
import re
import pandas as pd

app = Flask(__name__)
CORS(app)  # Active le support CORS, au cas où

# 🔥 Chargement du modèle Llama
llm = Llama(model_path="mistral-7b-instruct-v0.1.Q4_K_M.gguf", n_ctx=2048)
print("Modèle chargé avec succès !")

# 📌 Fonction pour extraire l'année d'un nom de fichier
def extract_year_from_filename(filename):
    match = re.search(r"(20\d{2})", filename)
    return int(match.group(1)) if match else None

# 📌 Dossier contenant les fichiers CSV
data_folder = "data"

def search_f1_data(question):
    question = question.lower()
    files_to_return = []  # Liste des fichiers CSV à retourner

    # Vérifier s'il y a une année spécifique dans la question
    match = re.search(r"(20\d{2})", question)
    year = int(match.group(1)) if match else None

    # Vérifier si l'utilisateur demande les 5 dernières années
    if any(keyword in question for keyword in ["5 dernières années", "dernières années", "cinq ans", "l'année prochaine"]):
        if year:
            start_year = max(2020, year - 4)  # Ne pas descendre sous 2020
        else:
            start_year = 2020
        years = list(range(start_year, start_year + 5))
        print("5 dernières années:", years)
    else:
        years = [year] if year else []
        print("Année:", years)

    # Identifier les fichiers à récupérer selon la question
    if any(x in question for x in ["classement", "champion", "pilote"]):
        print("Traitement du classement")
        files_to_return = [f"classement/classement_f1_{y}.csv" for y in years]
    elif any(x in question for x in ["calendrier", "date"]):
        files_to_return = [f"calendrier/calendrier_f1_{y}.csv" for y in years]
    elif "circuit" in question:
        files_to_return = [f"circuits/circuits_f1_{y}.csv" for y in years]
    elif "constructeur" in question:
        files_to_return = [f"constructeurs/constructeurs_f1_{y}.csv" for y in years]

    # Charger et concaténer les fichiers trouvés
    data_results = []
    for file_key in files_to_return:
        file_path = os.path.join(data_folder, file_key)
        print("Fichier:", file_path)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            data_results.append(f"📂 **Données de {file_key}**\n{df.to_string(index=False)}\n\n")
    if data_results:
        return "\n".join(data_results)
    return "Désolé, je n'ai pas trouvé de données correspondantes."

def generate_response(question, data_results):
    # Limiter la taille des données envoyées au modèle
    if len(data_results) > 1500:
        data_results = data_results[:1500]
    
    prompt = f"""
    [INST] 
    Tu es un expert en Formule 1. Un utilisateur te pose la question :
    "{question}"
    
    Voici les données brutes extraites des fichiers CSV :
    {data_results}
    
    Analyse les données et donne une réponse claire et concise.
    [/INST]
    """

    response_text = ""
    # Utiliser le mode stream pour récupérer progressivement la réponse
    for chunk in llm(prompt, max_tokens=256, stream=True):
         response_text += chunk["choices"][0]["text"]
    return response_text

# Route pour servir la page HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route pour traiter la question et renvoyer la réponse (en JSON)
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    data_results = search_f1_data(question)
    answer = generate_response(question, data_results)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
