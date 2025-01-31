import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# URL de l'API AJAX
url = "https://www.chateauversailles-spectacles.fr/wp/wp-admin/admin-ajax.php"

# En-têtes pour simuler une requête légitime
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# Données envoyées dans le POST
payload = {
    "action": "agenda_category_second",
    "numberResults": 9,  # Nombre d'événements à récupérer
    "date": ""  # Laisse vide pour voir ce que ça retourne
}

# Envoi de la requête POST
response = requests.post(url, headers=headers, data=payload)

# Vérifier si la requête a réussi
if response.status_code != 200:
    print("Erreur de chargement des événements :", response.status_code)
    exit()

# Parser le HTML renvoyé par l'API avec BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Trouver toutes les cartes d'événements
events = soup.select(".card-info")

# Vérifier si des événements ont été trouvés
if not events:
    print("Aucun événement trouvé.")
    exit()

# Liste pour stocker les données extraites
event_list = []

for event in events:
    try:
        # Date de l'événement
        day = event.select_one(".card__date .h2").text.strip() if event.select_one(".card__date .h2") else "Non spécifié"
        month = event.select_one(".card__date .d-mobile, .card__date .d-dekstop").text.strip() if event.select_one(".card__date .d-mobile, .card__date .d-dekstop") else "Non spécifié"
        year = event.select_one(".card__date .bold400-sm").text.strip() if event.select_one(".card__date .bold400-sm") else "Non spécifié"
        date = f"{day} {month} {year}"

        # Nom de l'événement
        title_elem = event.select_one(".h5.block.bold.mb-0")
        title = title_elem.text.strip() if title_elem else "Non spécifié"

        # Catégorie
        category_elem = event.select_one(".card__label")
        category = category_elem.text.strip() if category_elem else "Non spécifié"

        # Lieu
        location_elem = event.select_one(".lieu")
        location = location_elem.text.strip() if location_elem else "Non spécifié"

        # Image
        image_elem = event.select_one("img.media__desktop")
        image = image_elem["src"] if image_elem else "Non spécifié"

        # Lien de réservation
        link_elem = event.select_one(".card__overlay a")
        link = link_elem["href"] if link_elem else "Non spécifié"

        # Ajouter les données extraites à la liste
        event_list.append({
            "Date": date,
            "Événement": title,
            "Catégorie": category,
            "Lieu": location,
            "Lien de réservation": link,
            "Image": image
        })

    except AttributeError as e:
        print(f"Erreur lors de l'extraction d'un événement : {e}")

# Sauvegarde en JSON et CSV
df = pd.DataFrame(event_list)
df.to_csv("programmation_chateau_versailles.csv", index=False, encoding="utf-8-sig", sep=";")
with open("programmation_chateau_versailles.json", "w", encoding="utf-8") as json_file:
    json.dump(event_list, json_file, indent=4, ensure_ascii=False)

print("Données extraites et enregistrées avec succès !")