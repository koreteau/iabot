import gradio as gr
import requests

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
    # Formatage du contexte avec l'historique de discussion
    context = "\n".join([f"User: {msg[0]}\nBot: {msg[1]}" for msg in chat_history])
    
    # Construction du prompt avec l'historique
    prompt = f"{context}\nUser: {user_input}\nBot:"

    # Envoi de la requête à Ollama
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "deepseek/deepseek-coder-r1",
        "prompt": prompt
    })
    
    if response.status_code == 200:
        bot_response = response.json().get("response", "Je n'ai pas compris la question.")
    else:
        bot_response = "Erreur de connexion avec Ollama."

    # Ajout de la réponse dans l'historique
    chat_history.append((user_input, bot_response))

    return chat_history, chat_history

# Interface avec Gradio
with gr.Blocks() as demo:
    gr.Markdown("# 🏎️ ApexBot - Discussion en direct")

    chatbot = gr.Chatbot(label="Chat avec le bot F1")
    user_input = gr.Textbox(label="Pose ta question sur la F1", placeholder="Ex: Qui a gagné le dernier GP ?")

    with gr.Row():
        send_button = gr.Button("Envoyer")
        news_button = gr.Button("📢 Dernières infos F1")

    f1_news = gr.Textbox(label="Infos F1", interactive=False)

    # Gestion des actions
    send_button.click(chatbot_response, inputs=[user_input, chatbot], outputs=[chatbot, chatbot])
    news_button.click(get_f1_news, outputs=f1_news)

# Lancer l'interface
demo.launch()
