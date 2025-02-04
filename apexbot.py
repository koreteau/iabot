import gradio as gr
import requests
import json
import time
import re  # Ajout d'une librairie pour nettoyer le texte

# Fonction pour interagir avec Ollama et récupérer la réponse complète
def respond(user_input, chat_history):
    prompt = f"{user_input}\nBot:"

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "deepseek-r1:14b",
            "prompt": prompt
        }, stream=True)  # Activation du mode streaming

        bot_response = ""

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))  # Lire chaque ligne JSON
                    bot_response += data.get("response", "")  # Ajouter la réponse reçue
                except json.JSONDecodeError:
                    continue  # Ignore les erreurs JSON

        if not bot_response.strip():
            bot_response = "⚠️ Je n'ai pas compris votre question ou aucune réponse n'a été générée."

    except requests.exceptions.ConnectionError:
        bot_response = "⚠️ Erreur de connexion avec Ollama. Vérifie qu'il tourne avec `ollama serve`."

    # Debugging pour voir ce que reçoit l'UI
    print("Réponse complète du chatbot :", bot_response)

    # 🔹 **Nettoyage du texte : Supprime les balises <think> et tout leur contenu**
    bot_response = re.sub(r"<think>.*?</think>", "", bot_response, flags=re.DOTALL).strip()

    # 🔹 Vérification après nettoyage
    print("Réponse nettoyée :", bot_response)

    # Ajout de l'historique au format dict (Gradio messages)
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": bot_response})

    time.sleep(1)  # Simule un petit délai pour l'affichage

    return "", chat_history  # Retourne l'input vide + l'historique mis à jour

# Interface Gradio
with gr.Blocks() as demo:
    gr.Markdown("# 🏎️ APEXBOT")

    chatbot = gr.Chatbot(type="messages")  # Format messages correct
    msg = gr.Textbox(label="Pose ta question", placeholder="Ex: Qui a gagné le dernier GP de F1 ?")
    clear = gr.ClearButton([msg, chatbot])  # Bouton pour réinitialiser la conversation

    msg.submit(respond, [msg, chatbot], [msg, chatbot])  # Envoi du message quand l'utilisateur appuie sur Entrée

if __name__ == "__main__":
    demo.launch()