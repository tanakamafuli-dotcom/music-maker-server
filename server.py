from flask import Flask, request, send_file
from flask_cors import CORS
import requests, random, string, os, json
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

KEY = os.environ.get("POLLINATIONS_KEY", "pk_")
OWNER_CODE = "Tanaka2009"

if not os.path.exists("codes.json"):
    with open("codes.json","w") as f:
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
    voice = request.files['voice']
    genre = request.form.get('genre', 'Zimdancehall')
    preview = request.form.get('preview', 'true')
    voice.save("voice.wav")
    prompt = RIDDIMS.get(genre, RIDDIMS["Zimdancehall"])
    # ... (code yako yasara chengeta)
    return {"status": "ok"}

@app.route('/')
def home():
    return "Music Maker Server Live!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
