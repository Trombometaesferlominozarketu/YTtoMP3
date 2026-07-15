import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)
# Render nos permite usar la carpeta /tmp para descargas rápidas
DOWNLOAD_FOLDER = '/tmp/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Conversor Permanente</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0b0f19; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #111827; padding: 40px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); text-align: center; max-width: 450px; width: 90%; border: 1px solid #1f2937; }
        h1 { color: #f43f5e; font-size: 28px; margin-bottom: 10px; }
        p { color: #9ca3af; font-size: 14px; margin-bottom: 25px; }
        input[type="text"] { width: 100%; padding: 14px; border: 2px solid #374151; background: #0b0f19; color: white; border-radius: 8px; font-size: 14px; box-sizing: border-box; transition: 0.3s; }
        input[type="text"]:focus { border-color: #f43f5e; outline: none; }
        button { background: #f43f5e; color: white; border: none; width: 100%; padding: 14px; margin-top: 20px; font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: 0.2s; }
        button:hover { background: #e11d48; }
        .footer { margin-top: 25px; font-size: 11px; color: #4b5563; }
    </style>
</head>
<body>
    <div class="card">
        <h1>NubeMP3 Fijo 🚀</h1>
        <p>Tu propio convertidor permanente en la nube.</p>
        <form action="/convertir" method="POST">
            <input type="text" name="url" placeholder="Pega el enlace de YouTube aquí..." required>
            <button type="submit">Descargar MP3</button>
        </form>
        <div class="footer">Enlace permanente alojado en Render</div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/convertir', methods=['POST'])
def convertir():
    url = request.form.get('url')
    if not url: return "Enlace no válido", 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            mp3_path = os.path.splitext(filename) + '.mp3'
        
        return send_file(mp3_path, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    # Render asigna automáticamente un puerto, lo detectamos aquí
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
