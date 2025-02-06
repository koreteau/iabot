const fs = require("fs");
const path = require("path");

// Configuration : âge maximal d'un feedback en minutes
const FEEDBACK_EXPIRATION_MINUTES = 43800;

// Chemin du fichier feedback.json
const FEEDBACK_FILE = path.join(__dirname, "../../public/data/feedback.json");

// Fonction pour charger les feedbacks
function loadFeedbacks() {
    if (!fs.existsSync(FEEDBACK_FILE)) {
        return [];
    }
    try {
        const data = fs.readFileSync(FEEDBACK_FILE, "utf8");
        return JSON.parse(data) || [];
    } catch (error) {
        console.error("❌ Erreur lors du chargement des feedbacks :", error);
        return [];
    }
}

// Fonction pour sauvegarder les feedbacks nettoyés
function saveFeedbacks(feedbacks) {
    try {
        fs.writeFileSync(FEEDBACK_FILE, JSON.stringify(feedbacks, null, 2), "utf8");
    } catch (error) {
        console.error("❌ Erreur lors de la sauvegarde des feedbacks :", error);
    }
}

// Fonction pour supprimer les feedbacks trop vieux
function deleteOldFeedbacks() {
    const now = Date.now();
    const feedbacks = loadFeedbacks();

    const filteredFeedbacks = feedbacks.filter(fb => {
        const feedbackAgeMinutes = (now - new Date(fb.timestamp).getTime()) / 60000;
        return feedbackAgeMinutes <= FEEDBACK_EXPIRATION_MINUTES;
    });

    if (filteredFeedbacks.length !== feedbacks.length) {
        console.log(`🗑️ Suppression des feedbacks vieux de ${FEEDBACK_EXPIRATION_MINUTES} minutes...`);
        saveFeedbacks(filteredFeedbacks);
    } else {
        console.log(`✅ Aucun feedback à supprimer.`);
    }
}

// Lancer automatiquement le nettoyage toutes les X minutes
setInterval(deleteOldFeedbacks, FEEDBACK_EXPIRATION_MINUTES * 60000);

// Exécuter une première fois immédiatement
deleteOldFeedbacks();
