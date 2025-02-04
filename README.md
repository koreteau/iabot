# APEXBOT - Chatbot Formule 1 🏎️

![GitHub Repo](https://img.shields.io/badge/GitHub-APEXBOT-blue)

## 🚀 Introduction
APEXBOT est un chatbot interactif permettant d'obtenir des informations sur la Formule 1. Il repose sur un modèle de langage (`f1-bot`) et une base de données structurée. L'interface est développée avec **Gradio**, et les réponses sont générées via **Ollama**.

## 📂 Arborescence du projet
```
📂 data
│   ├── 📂 calendrier
│   ├── 📂 circuits
│   ├── 📂 classement
│   ├── 📂 constructeurs
├── apexbot.py
├── Data_scrapping.ipynb
├── feedback.txt
├── Modelfile.md
├── .gitattributes
```

## ✨ Fonctionnalités principales
- 🔍 **Réponses sur la Formule 1** grâce à un modèle de langage dédié.
- 📝 **Gestion d’un historique de conversation**.
- 📩 **Système de feedback** pour améliorer les réponses.
- 📊 **Base de données complète** sur les saisons de F1 (constructeurs, classements, circuits, etc.).

## 📜 Détails des fichiers

### `apexbot.py` - Chatbot 🧠
- Interface développée avec **Gradio**.
- Requêtes envoyées à **Ollama** via une API.
- Nettoyage des réponses pour éviter les erreurs de formatage.
- Stockage des retours utilisateurs dans `feedback.txt`.

### `Data_scrapping.ipynb` - Extraction des données 🌍
- Notebook Jupyter permettant de récupérer des données de F1.
- basé sur **Pandas** et **requests**.

### `Modelfile.md` - Configuration du modèle 🛠️
- Modèle utilisé : **deepseek-r1:14b**.
- Intégration des fichiers de données : `calendrier`, `classements`, `constructeurs`, etc.

### `feedback.txt` - Stockage des avis utilisateurs 📜
- Contient l’historique des retours utilisateurs.
- Utilisé pour améliorer les réponses du chatbot.

### `data/` - Base de données de la F1 🏁
- Contient des fichiers `.md` regroupant les données historiques des saisons de F1.
- Exemples de constructeurs en 2021 : Alpine, Ferrari, Mercedes, Red Bull...

## 📥 Installation & Utilisation

### 🛠️ Prérequis
- Python 3.x
- Ollama
- Gradio

### 1️⃣ Installation
```sh
git clone https://github.com/koreteau/iabot.git
cd iabot
pip install -r requirements.txt
```

### 2️⃣ Lancer Ollama
```sh
ollama serve
```

### 3️⃣ Exécuter le chatbot
```sh
python apexbot.py
```
---

## 💡 Conclusion
APEXBOT est un **chatbot dédié à la Formule 1**, combinant intelligence artificielle et données historiques. Son développement peut être enrichi avec des fonctionnalités supplémentaires, notamment **l'intégration de résultats en direct** et **l'amélioration du modèle linguistique**.

