from flask import Flask, request, send_file
import requests, random, string, os, json
from pydub import AudioSegment

app = Flask(__name__)
KEY = "pk_"
OWNER_CODE = "Tanaka2009"

if not os.path.exists("codes.json"):
    with open("codes.json","w") as f:
        json.dump([], f)

RIDDIMS = {
 "Zimdancehall": "Zimdancehall riddim 92 BPM heavy bass",
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
    genre = request.form.get('genre','Zimdancehall')
    preview = request.form.get('preview','true')
    voice.save("voice.wav")
    prompt = RIDDIMS.get(genre, RIDDIMS["Zimdancehall"])
    url = f"https://gen.pollinations.ai/audio/{prompt}?model=google/lyria-3.5&key={KEY}"
    r = requests.get(url, timeout=120)
    open("riddim.mp3","wb").write(r.content)
    v = AudioSegment.from_file("voice.wav")
    rd = AudioSegment.from_file("riddim.mp3") - 6
    rd = (rd * (len(v)//len(rd)+1))[:len(v)]
    final = rd.overlay(v)
    if preview == "true":
        final[:30000].export("preview.mp3", format="mp3")
        return send_file("preview.mp3")
    else:
        final.export("final.mp3", format="mp3")
        return send_file("final.mp3")

@app.route('/verify-code')
def verify():
    code = request.args.get('code','')
    if code == OWNER_CODE: return "valid_owner"
    codes = json.load(open("codes.json"))
    return "valid_paid" if code in codes else "invalid"

@app.route('/use-code')
def use_code():
    code = request.args.get('code','')
    if code == OWNER_CODE: return "ok"
    codes = json.load(open("codes.json"))
    if code in codes:
        codes.remove(code)
        json.dump(codes, open("codes.json","w"))
        return "ok"
    return "invalid"

@app.route('/generate-code')
def generate():
    if request.args.get('secret','') != OWNER_CODE: return "unauthorized"
    new_code = "MM-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    codes = json.load(open("codes.json"))
    codes.append(new_code)
    json.dump(codes, open("codes.json","w"))
    return new_code

app.run(host='0.0.0.0', port=10000)
