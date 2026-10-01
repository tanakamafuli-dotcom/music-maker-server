from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

KEY = os.environ.get("POLLINATIONS_KEY", "pk_test")
OWNER_CODE = "Tanaka2009"

if not os.path.exists("codes.json"):
    with open("codes.json", "w") as f:
        json.dump([], f)

RIDDIMS = {
    "Zimdancehall": "Zimdancehall riddim 92 BPM hard bass",
    "Afrobeats": "Afrobeats 105 BPM log drum",
    "Sungura": "Sungura 110 BPM lead guitar",
    "Amapiano": "Amapiano 113 BPM piano",
    "Dancehall": "Dancehall 95 BPM",
    "Hip Hop": "Trap beat 85 BPM 808",
    "Gospel": "Gospel 75 BPM piano",
    "Afro Jazz": "Afro Jazz 80 BPM sax"
}

@app.route('/make-song', methods=['POST'])
def make():
    try:
        voice = request.files.get('voice')
        genre = request.form.get('genre', 'Zimdancehall')
        prompt = RIDDIMS.get(genre, RIDDIMS["Zimdancehall"])
        return jsonify({"status": "ok", "genre": genre, "prompt": prompt})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Music Maker Server Live!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
