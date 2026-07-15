import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = '/tmp/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Diseño retro años 50 con paleta de colores del atardecer de Salt Lake City
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT to MP3 - Retro Converter</title>
    <!-- Importamos tipografías de estilo mid-century / retro de los años 50 -->
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Lobster&family=Oswald:wght@500;700&display=swap" rel="stylesheet">
    
    <style>
        body { 
            font-family: 'Oswald', sans-serif; 
            /* Degradado lineal que imita un atardecer profundo en el desierto de Utah */
            background: linear-gradient(180deg, #1e112a 0%, #3a1c3f 25%, #772b44 50%, #b8413a 75%, #e07641 100%);
            background-attachment: fixed;
            color: #fdf6e2; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0; 
        }
        
        .card { 
            background: #fdf6e2; /* Color crema suave vintage para la tarjeta */
            padding: 50px 40px; 
            border-radius: 4px; 
            text-align: center; 
            max-width: 480px; 
            width: 90%; 
            border: 4px solid #1e112a; 
            /* Sombra paralela sólida y gruesa típica del diseño gráfico de 1950 */
            box-shadow: 12px 12px 0px #1e112a; 
        }
        
        h1 { 
            font-family: 'Lobster', cursive;
            color: #b8413a; 
            font-size: 72px; /* Letras mucho más grandes */
            margin: 0 0 10px 0; 
            line-height: 1.1;
            font-weight: normal;
            /* Efecto de relieve retro usando sombras de texto repetidas */
            text-shadow: 2px 2px 0px #fdf6e2, 5px 5px 0px #1e112a;
        }
        
        p { 
            color: #1e112a; 
            font-size: 16px; 
            text-transform: uppercase;
            letter-spacing: 2px;
            font-weight: 700;
            margin-bottom: 35px; 
        }
        
        input[type="text"] { 
            width: 100%; 
            padding: 14px; 
            border: 3px solid #1e112a; 
            background: #ffffff; 
            color: #1e112a; 
            border-radius: 0px; 
            font-size: 15px; 
            box-sizing: border-box; 
            font-family: 'Oswald', sans-serif;
            text-align: center;
        }
        
        input[type="text"]:focus { 
            outline: none;
            background: #fff9e6;
            border-color: #b8413a;
        }
        
        button { 
            background: #e07641; 
            color: #1e112a; 
            border: 3px solid #1e112a; 
            width: 100%; 
            padding: 15px; 
            margin-top: 25px; 
            font-size: 20px; 
            font-weight: 700; 
            text-transform: uppercase;
            letter-spacing: 1px;
            border-radius: 0px; 
            cursor: pointer; 
            box-shadow: 4px 4px 0px #1e112a;
            transition: all 0.1s ease;
        }
        
        button:hover { 
            transform: translate(2px, 2px); 
            box-shadow: 2px 2px 0px #1e112a;
            background: #f08953;
        }
        
        .footer { 
            margin-top: 35px; 
            font-size: 12px; 
            color: #772b44; 
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>YT to MP3</h1>
        <p>High Quality Audio Extraction</p>
        <form action="/convertir" method="POST">
            <input type="text" name="url" placeholder="PASTE YOUTUBE LINK HERE" required>
            <button type="submit">Convert & Download</button>
        </form>
        <div class="footer">Salt Lake City Transmissions</div>
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
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
