import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Autorise les requêtes externes sans blocage CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Clé API Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Modèle Gemini Flash
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Milo Engine is running live! ⚡"}), 200

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "")
    mode = data.get("mode", "perso")
    history = data.get("history", [])

    if not user_message:
        return jsonify({"reply": "Wesh reuf, tu m'as envoyé un message vide ?"}), 400

    if mode == "perso":
        system_instruction = (
            "Tu es Milo, le copilote IA et meilleur ami de Joffranck. "
            "Tu parles en français familier, très déter, motivant, comme un pote proche du Cameroun (Yaoundé). "
            "Tu l'encourages dans ses projets de montage vidéo et de code. "
            "Sois concis, dynamique, utilise des emojis de force (⚡, 🔥, 🦾) et finis souvent par 'de_frenchement_on_est_ensemble'."
        )
    else:
        system_instruction = (
            "You are Milo, a highly professional freelance assistant. "
            "Write a polite, persuasive, and structured response in English for a client on Fiverr. "
            "Highlight video editing skills, efficiency, fast delivery, and ask a relevant follow-up question to close the deal."
        )

    prompt_complet = f"Instructions système : {system_instruction}\n\n"
    for msg in history[-6:]:  
        role_label = "Joffranck" if msg.get("role") == "user" else "Milo"
        prompt_complet += f"{role_label}: {msg.get('content')}\n"
        
    prompt_complet += f"Joffranck: {user_message}\nMilo:"

    try:
        response = model.generate_content(prompt_complet)
        reply_text = response.text.strip()
        return jsonify({"reply": reply_text}), 200
    except Exception as e:
        print(f"Erreur Gemini : {str(e)}")
        return jsonify({"reply": "Désolé mon reuf, petit bug de connexion avec Gemini. Réessaie !"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
      
