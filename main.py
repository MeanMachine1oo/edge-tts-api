from flask import Flask, request, send_file, jsonify
import edge_tts
import asyncio
import tempfile
import os

app = Flask(__name__)

AUDIO_DIR = '/tmp/audio'
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text', '')
    voice = data.get('voice', 'hi-IN-SwaraNeural')
    filename = data.get('filename', 'audio.mp3')
    
    filepath = os.path.join(AUDIO_DIR, filename)
    
    async def generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(filepath)
    
    asyncio.run(generate())
    
    base_url = os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'localhost:5000')
    audio_url = f"https://{base_url}/audio/{filename}"
    
    return jsonify({ "url": audio_url, "filename": filename })

@app.route('/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    filepath = os.path.join(AUDIO_DIR, filename)
    return send_file(filepath, mimetype='audio/mpeg')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
