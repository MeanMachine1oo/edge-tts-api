from flask import Flask, request, send_file
import edge_tts
import asyncio
import tempfile
import os

app = Flask(__name__)

@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text', '')
    voice = data.get('voice', 'hi-IN-SwaraNeural')
    filename = data.get('filename', 'audio.mp3')
    
    async def generate():
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tmp_path = f.name
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(tmp_path)
        return tmp_path
    
    tmp_path = asyncio.run(generate())
    return send_file(tmp_path, mimetype='audio/mpeg', as_attachment=True, download_name=filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

Then update **Edge TTS** body to:
```
{{ JSON.stringify({ text: $json.hindiText, voice: "hi-IN-SwaraNeural", filename: "meal-plan-" + $json.MealDate + ".mp3" }) }}
