import os
import base64
from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

client = Anthropic()

ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}

PLATFORM_PROMPTS = {
    'instagram': """Tu es un expert en marketing Instagram. Analyse cette photo et génère une publication Instagram parfaite.

Réponds UNIQUEMENT avec ce format exact :

📝 LÉGENDE :
[2 à 4 phrases engageantes avec emojis adaptés au contenu, ton authentique et personnel]

💬 CALL-TO-ACTION :
[Une phrase courte pour inviter l'interaction : question, invitation à commenter, partager, etc.]

#️⃣ HASHTAGS :
[25 à 30 hashtags pertinents séparés par des espaces, mélange de hashtags populaires et de niche]""",

    'vinted': """Tu es un expert en vente sur Vinted. Analyse cette photo et génère une annonce complète et attractive.

Réponds UNIQUEMENT avec ce format exact :

🏷️ TITRE :
[Titre accrocheur et précis, max 50 caractères, ex: "Robe fleurie Zara taille S - état neuf"]

📋 DESCRIPTION :
[Description détaillée : marque si visible, couleur, matière si devinable, état (neuf / très bon état / bon état / satisfaisant), style, détails particuliers. 3 à 5 phrases.]

📏 TAILLE : [Taille ou fourchette de tailles, ex: S/M ou 38/40]

💰 PRIX SUGGÉRÉ : [Prix en euros, réaliste pour Vinted, ex: 18€]

📂 CATÉGORIE : [Catégorie Vinted, ex: Robes / Vêtements femme / Chaussures / Accessoires / etc.]""",

    'leboncoin': """Tu es un expert en vente sur Leboncoin. Analyse cette photo et génère une annonce efficace.

Réponds UNIQUEMENT avec ce format exact :

🏷️ TITRE :
[Titre précis et informatif, max 60 caractères]

📋 DESCRIPTION :
[Description complète : état, caractéristiques principales, éventuellement raison de vente. Style direct et honnête. 3 à 5 phrases.]

💰 PRIX SUGGÉRÉ : [Prix en euros réaliste pour Leboncoin, ex: 25€]

📂 CATÉGORIE : [Catégorie Leboncoin appropriée, ex: Vêtements / Électronique / Meuble / Sport / etc.]

📍 LIEU DE RETRAIT : [À compléter par le vendeur]""",

    'facebook': """Tu es un expert en vente sur Facebook Marketplace. Analyse cette photo et génère une annonce conviviale et attractive.

Réponds UNIQUEMENT avec ce format exact :

🏷️ TITRE :
[Titre accrocheur, style Facebook, avec emoji si pertinent]

📋 DESCRIPTION :
[Description chaleureuse et détaillée, avec état, caractéristiques. Style Facebook Marketplace : direct, accessible et convivial. 3 à 5 phrases. Terminer par "N'hésitez pas à me contacter !"]

💰 PRIX SUGGÉRÉ : [Prix en euros, ex: 20€]

📂 CATÉGORIE : [Catégorie Facebook Marketplace]

📍 ZONE GÉOGRAPHIQUE : [À compléter par le vendeur]"""
}

PLATFORM_NAMES = {
    'instagram': 'Instagram',
    'vinted': 'Vinted',
    'leboncoin': 'Leboncoin',
    'facebook': 'Facebook Marketplace',
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    if 'image' not in request.files:
        return jsonify({'error': 'Aucune image fournie.'}), 400

    file = request.files['image']
    platform = request.form.get('platform', '')

    if not file or file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné.'}), 400

    if platform not in PLATFORM_PROMPTS:
        return jsonify({'error': 'Plateforme non supportée.'}), 400

    mime_type = file.content_type or 'image/jpeg'
    if mime_type not in ALLOWED_MIME_TYPES:
        mime_type = 'image/jpeg'

    image_bytes = file.read()
    if len(image_bytes) == 0:
        return jsonify({'error': 'Le fichier image est vide.'}), 400

    image_b64 = base64.standard_b64encode(image_bytes).decode('utf-8')

    try:
        response = client.messages.create(
            model='claude-opus-4-7',
            max_tokens=1024,
            messages=[
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'image',
                            'source': {
                                'type': 'base64',
                                'media_type': mime_type,
                                'data': image_b64,
                            },
                        },
                        {
                            'type': 'text',
                            'text': PLATFORM_PROMPTS[platform],
                        },
                    ],
                }
            ],
        )
        generated = response.content[0].text
        return jsonify({
            'result': generated,
            'platform': PLATFORM_NAMES[platform],
        })
    except Exception as exc:
        return jsonify({'error': f'Erreur API : {exc}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
