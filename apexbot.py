import requests
import json
import gradio as gr

# Fonction pour interagir avec Ollama et récupérer la réponse complète
def chatbot_response(user_input, history):
    prompt = f"{user_input}\nBot:"

    # Ajout du prompt du user à l'historique
    history.append(gr.ChatMessage(role="user", content=user_input))

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

    # Ajout de l'historique au format ChatMessage
    history.append(gr.ChatMessage(role="assistant", content=bot_response))
    
    return history  # Retourne l'historique mis à jour

# Interface Gradio avec le format natif ChatMessage
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Chatbot F1 avec DeepSeek-R1")

    # Initialisation de l'historique avec un message d'accueil
    history = [gr.ChatMessage(role="assistant", content="Salut ! Pose-moi tes questions.")]

    chatbot = gr.Chatbot(history, type="messages")  # Utilisation du bon format
    user_input = gr.Textbox(label="Pose ta question sur la F1", placeholder="Ex: Qui a gagné le dernier GP ?")

    with gr.Row():
        send_button = gr.Button("Envoyer")
        clear_button = gr.Button("🗑 Réinitialiser")

    send_button.click(chatbot_response, inputs=[user_input, chatbot], outputs=chatbot)
    clear_button.click(lambda: [gr.ChatMessage(role="assistant", content="Nouvelle conversation.")], outputs=chatbot)

demo.launch()
