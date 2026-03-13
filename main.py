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
    
    async def generate():
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tmp_path = f.name
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(tmp_path)
        return tmp_path
    
    tmp_path = asyncio.run(generate())
    return send_file(tmp_path, mimetype='audio/mpeg', as_attachment=True, download_name='audio.mp3')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

4. Click **Commit new file**

Then create another file — click **Add file** → **Create new file**:
5. Name it `requirements.txt`
6. Paste:
```
flask
edge-tts
