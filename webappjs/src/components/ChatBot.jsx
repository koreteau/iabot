import { useState, useEffect, useRef } from "react";
import { Card, Button, Input, Textarea } from "@material-tailwind/react";


const F1_KEYWORDS = ["F1", "Formula 1", "Grand Prix", "pilote", "écurie", "championnat", "circuit", "calendrier", "classement", "course", "GP"];

export default function Chatbot() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [feedback, setFeedback] = useState("");
    const chatEndRef = useRef(null);
    const [f1Data, setF1Data] = useState(null);

    // Charger les fichiers F1 une seule fois au démarrage
    useEffect(() => {
        loadF1Data();
    }, []);

    async function loadF1Data() {
        try {
            const response = await fetch("/data/f1_data.json"); // Simule un chargement local
            const data = await response.json();
            setF1Data(data);
        } catch (error) {
            console.error("Erreur lors du chargement des fichiers F1 :", error);
        }
    }

    function isF1Question(text) {
        return F1_KEYWORDS.some(keyword => text.toLowerCase().includes(keyword.toLowerCase()));
    }

    function extractLatestF1Data() {
        if (!f1Data) return null;
        const latestYear = Math.max(...Object.keys(f1Data).map(Number));
        return latestYear ? Object.entries(f1Data[latestYear]).map(([category, content]) => `### ${category} - ${latestYear}\n${content}`).join("\n\n") : null;
    }

    async function queryOllama(userInput) {
        const f1Context = isF1Question(userInput) ? extractLatestF1Data() : null;

        const prompt = f1Context
            ? `Tu es un expert en Formule 1. Voici les données les plus récentes :\n\n${f1Context}\n\nUtilise **uniquement ces informations** pour répondre.\nQuestion : ${userInput}`
            : `Tu es un expert en Formule 1. Aucune donnée locale récente n'est disponible.\nRéponds avec tes propres connaissances.\n\nQuestion : ${userInput}`;

        try {
            const response = await fetch("http://localhost:11434/api/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ model: "deepseek-r1:14b", prompt }),
            });

            let botResponse = "";
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                // Décoder et parser chaque ligne JSON
                const lines = decoder.decode(value).split("\n").filter(line => line.trim() !== "");
                for (const line of lines) {
                    try {
                        const data = JSON.parse(line);
                        if (data.response) {
                            botResponse += data.response;
                        }
                    } catch (error) {
                        console.error("Erreur de parsing JSON :", error);
                    }
                }
            }

            // Nettoyage des éventuelles balises <think>
            botResponse = botResponse.replace(/<think>.*?<\/think>/gs, "").trim();

            return botResponse || "⚠️ Je n'ai pas compris la question.";
        } catch (error) {
            console.error("Erreur avec Ollama :", error);
            return "⚠️ Erreur de connexion avec Ollama.";
        }
    }


    async function sendMessage() {
        if (!input.trim()) return;

        const userMessage = { role: "user", content: input };
        setMessages((prev) => [...prev, userMessage]);

        const botMessageContent = await queryOllama(input);
        const botMessage = { role: "assistant", content: botMessageContent };

        setMessages((prev) => [...prev, botMessage]);
        setInput("");
    }

    async function sendFeedback() {
        if (!feedback.trim()) return;

        try {
            await fetch("/feedback.txt", {
                method: "POST",
                headers: { "Content-Type": "text/plain" },
                body: `Feedback: ${feedback}\nHistorique: ${JSON.stringify(messages, null, 2)}\n\n`,
            });
        } catch (error) {
            console.error("Erreur lors de l'enregistrement du feedback :", error);
        }

        setFeedback("");
    }

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    return (
        <div className="max-w-2xl mx-auto mt-8 p-4">
            <h1 className="text-2xl font-bold mb-4">🏎️ APEXBOT</h1>

            <Card className="h-96 overflow-y-auto p-4 bg-gray-100 rounded-lg shadow">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`mb-2 p-2 rounded-lg ${msg.role === "user" ? "bg-blue-300 text-right" : "bg-gray-200"
                            }`}
                    >
                        {msg.content}
                    </div>
                ))}
                <div ref={chatEndRef} />
            </Card>

            <div className="flex items-center mt-4 space-x-2">
                <Input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Pose ta question..." />
                <Button onClick={sendMessage} disabled={!input.trim()}>Envoyer</Button>
            </div>

            <div className="mt-4">
                <h2 className="text-lg font-semibold">Feedback</h2>
                <Textarea value={feedback} onChange={(e) => setFeedback(e.target.value)} placeholder="Votre avis sur la réponse..." />
                <Button className="mt-2" onClick={sendFeedback} disabled={!feedback.trim()}>Envoyer le feedback</Button>
            </div>
        </div>
    );
}
