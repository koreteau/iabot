import gradio as gr
import requests
import json

# Fonction pour récupérer les dernières infos F1
def get_f1_news():
    url = "https://ergast.com/api/f1/current.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        latest_race = races[-1] if races else None
        if latest_race:
            return f"🏁 **Prochain GP** : {latest_race['raceName']} - {latest_race['Circuit']['circuitName']} ({latest_race['date']})"
    
    return "Pas d'infos disponibles."

# Fonction du chatbot avec gestion de l'historique
def chatbot_response(user_input, chat_history):
    prompt = f"{user_input}\nBot:"

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "deepseek-r1:14b",
            "prompt": prompt
        }, stream=True)  # Activation du mode streaming

        bot_response = ""  # Initialisation de la réponse

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))  # Lire chaque ligne JSON
                    bot_response += data.get("response", "")  # Ajouter la réponse reçue
                except json.JSONDecodeError:
                    continue  # Ignore les erreurs JSON

        # Vérification de la réponse
        if not bot_response.strip():
            bot_response = "⚠️ Je n'ai pas compris votre question ou aucune réponse n'a été générée."

    except requests.exceptions.ConnectionError:
        bot_response = "⚠️ Erreur de connexion avec Ollama. Vérifie qu'il tourne avec `ollama serve`."

    # Ajout à l'historique et retour des messages
    chat_history.append((user_input, bot_response))
    print("Réponse complète du chatbot :", bot_response)
    return chat_history, chat_history

# Interface avec Gradio
with gr.Blocks() as demo:
    gr.Markdown("# 🏎️ ApexBot - Discussion en direct")

    chatbot = gr.Chatbot(label="Chat avec le bot F1")
    user_input = gr.Textbox(label="Pose ta question sur la F1", placeholder="Ex: Qui a gagné le dernier GP F1 ?")

    with gr.Row():
        send_button = gr.Button("Envoyer")
        news_button = gr.Button("📢 Dernières infos F1")

    f1_news = gr.Textbox(label="Infos F1", interactive=False)

    # Gestion des actions
    send_button.click(chatbot_response, inputs=[user_input, chatbot], outputs=[chatbot, chatbot])
    news_button.click(get_f1_news, outputs=f1_news)

# Lancer l'interface
demo.launch()
