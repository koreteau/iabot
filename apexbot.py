import gradio as gr
import requests
import json
<<<<<<< Updated upstream
import re
import os
import glob
=======
import time
import re  # Pour nettoyer le texte
>>>>>>> Stashed changes


F1_FOLDERS = {
    "calendrier": "data/calendrier",
    "circuits": "data/circuits",
    "classements": "data/classement"
}

F1_KEYWORDS = ["F1", "Formula 1", "Grand Prix", "pilote", "écurie", "championnat", "circuit", "calendrier", "classement", "course", "GP"]

def load_f1_data():
    """ Charge toutes les données F1 des fichiers Markdown en mémoire sous forme de dictionnaire """
    f1_data = {}
    
    for category, folder in F1_FOLDERS.items():
        if not os.path.exists(folder):
            print(f"🚫 Dossier introuvable : {folder}")
            continue

        for filepath in glob.glob(os.path.join(folder, "*.md")):
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                year_match = re.search(r"(\d{4})", filepath)
                if year_match:
                    year = int(year_match.group(1))
                    if year not in f1_data:
                        f1_data[year] = {}
                    f1_data[year][category] = content
                    print(f"✅ Données chargées pour {year} ({category}) depuis {filepath}")

    return f1_data

F1_DATABASE = load_f1_data()

def is_f1_question(user_input):
    """ Vérifie si la question concerne la F1 en cherchant des mots-clés """
    return any(keyword.lower() in user_input.lower() for keyword in F1_KEYWORDS)

def extract_latest_data():
    """ Construit un contexte avec les informations F1 les plus récentes des fichiers `.md` """
    latest_year = max(F1_DATABASE.keys(), default=None)
    if not latest_year:
        return None 

    latest_data = []
    for category, content in F1_DATABASE[latest_year].items():
        latest_data.append(f"### {category.capitalize()} - {latest_year}\n{content}")

    return "\n\n".join(latest_data) if latest_data else None

def query_ollama(user_input, f1_context):
    """ Envoie une requête à DeepSeek en lui imposant d'utiliser les fichiers `.md` """
    
    if f1_context:
        prompt = f"""
        Tu es un expert en Formule 1. Voici les données les plus récentes extraites de fichiers officiels :
        
        {f1_context}
        
        Utilise **uniquement ces informations** pour générer ta réponse.
        Ne t'appuie PAS sur tes propres connaissances si la réponse est dans les fichiers fournis.

        Question de l'utilisateur :
        {user_input}
        """
    else:
        prompt = f"""
        Tu es un expert en Formule 1. Aucune donnée locale récente n'est disponible.
        Réponds avec tes propres connaissances, mais précise bien que tes informations peuvent être obsolètes.

        Question de l'utilisateur :
        {user_input}
        """
    
    try:
        res = requests.post("http://localhost:11434/api/generate", json={
            "model": "deepseek-r1:14b",
            "prompt": prompt
        }, stream=True)

        bot_response = ""
        for line in res.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    bot_response += data.get("response", "")
                except json.JSONDecodeError:
                    continue

        return bot_response.strip() or "⚠️ Je n'ai pas compris ta question."
    
    except requests.exceptions.ConnectionError:
        return "⚠️ Erreur de connexion avec Ollama. Vérifie qu'il tourne avec `ollama serve`."

<<<<<<< Updated upstream
def respond(user_input, chat_history):
    """ Génère une réponse combinée entre DeepSeek et nos fichiers F1 """

    # Vérifier si la question concerne la F1
    f1_data = extract_latest_data() if is_f1_question(user_input) else None
    
    # Demander une réponse à DeepSeek en lui imposant nos fichiers comme source principale
    ollama_response = query_ollama(user_input, f1_data)

    # Comparer les résultats et choisir la meilleure réponse
    response = ollama_response

    # Nettoyage du texte pour enlever les raisonnements de l'ia
    response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

    # Mise à jour de l'historique
=======
    # Affichage pour le débogage
    print("Réponse complète du chatbot :", bot_response)

    # Nettoyage du texte : suppression des balises <think> et de leur contenu
    bot_response = re.sub(r"<think>.*?</think>", "", bot_response, flags=re.DOTALL).strip()

    print("Réponse nettoyée :", bot_response)

    # Mise à jour de l'historique (format Gradio messages)
>>>>>>> Stashed changes
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})

<<<<<<< Updated upstream
    print("Réponse générée :", response)

    return "", chat_history

=======
    time.sleep(1)  # Délai simulé pour l'affichage

    return "", chat_history  # Retourne l'input vide et l'historique mis à jour

# Fonction pour enregistrer le feedback
def enregistrer_feedback(feedback, chat_history):
    # Ici, vous pouvez envoyer le feedback vers une API, l'enregistrer dans une base de données ou un fichier
    print("Feedback reçu :", feedback)
    
    # Exemple d'enregistrement dans un fichier (mode append)
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write("Feedback: " + feedback + "\n")
        f.write("Historique: " + json.dumps(chat_history, ensure_ascii=False) + "\n")
        f.write("="*50 + "\n")
    
    # Réinitialiser la zone de texte de feedback
    return gr.update(value="")
>>>>>>> Stashed changes

with gr.Blocks() as demo:
    gr.Markdown("# 🏎️ APEXBOT")

<<<<<<< Updated upstream
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(label="Pose ta question", placeholder="Ex: Qui a gagné le Grand Prix de Monza en 2020 ?")
    clear = gr.ClearButton([msg, chatbot])

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
=======
    # Zone du chatbot et du message utilisateur
    chatbot = gr.Chatbot(type="messages")
    msg = gr.Textbox(label="Pose ta question", placeholder="Ex: Qui a gagné le dernier GP de F1 ?")
    clear = gr.ClearButton([msg, chatbot])

    # Soumission du message utilisateur
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    # Zone de feedback
    gr.Markdown("### Donnez votre feedback sur la réponse")
    feedback_input = gr.Textbox(label="Votre feedback", placeholder="Ex: La réponse était claire / peu pertinente, etc.")
    feedback_button = gr.Button("Envoyer le feedback")
    feedback_button.click(enregistrer_feedback, [feedback_input, chatbot], feedback_input)
>>>>>>> Stashed changes

if __name__ == "__main__":
    demo.launch()
