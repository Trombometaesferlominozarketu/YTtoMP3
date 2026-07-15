import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = '/tmp/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Diseño fiel a la tipografía hilada del Chevrolet Deluxe 1950 y fondo nativo garantizado
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT to MP3 - De Luxe Station</title>
    <!-- Importamos la fuente ideal de Google para emular la tipografía cursiva unida de los emblemas automotrices -->
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Ole+Script:wght@700&family=Oswald:wght@700&display=swap" rel="stylesheet">
    
    <style>
        body { 
            margin: 0;
            padding: 0;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh;
            /* Recreación exacta del degradado del atardecer real de Salt Lake City de tu foto */
            background: linear-gradient(180deg, #180a2b 0%, #3b1442 30%, #7d1c3a 55%, #c73e28 75%, #ec8625 90%, #f6b62c 100%);
            background-attachment: fixed;
            font-family: 'Oswald', sans-serif;
            overflow: hidden;
        }
        
        .header-container {
            position: absolute;
            top: 7vh;
            width: 100%;
            text-align: center;
            z-index: 10;
        }

        /* GRAFÍA AUTOMOTRIZ DE LUXE EXACTA: CURSIVA, HILADA, ULTRA GRUESA E INCLINADA */
        h1 { 
            font-family: 'Ole Script', cursive;
            font-weight: 700;
            font-size: 110px; /* Enorme arriba */
            margin: 0 auto;
            display: inline-block;
            letter-spacing: -2px; /* Letras unidas e hiladas entre sí */
            line-height: 0.9;
            text-transform: none; /* Mantiene las mayúsculas y minúsculas idénticas al emblema */
            
            /* Inclinación aerodinámica del logo clásico del coche */
            transform: rotate(-3deg) skewX(-12deg); 
            
            /* Acabado Cromo Espejo inyectado */
            background: linear-gradient(
                to bottom, 
                #ffffff 0%, 
                #f1f5f9 42%, 
                #475569 48%, 
                #0f172a 53%, 
                #cbd5e1 68%, 
                #ffffff 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            
            /* Relieve macizo biselado tridimensional idéntico en cada carácter */
            filter: drop-shadow(2px 2px 0px #ffffff)
                    drop-shadow(-1px -1px 0px #475569)
                    drop-shadow(6px 6px 0px #0f172a)
                    drop-shadow(10px 10px 15px rgba(0,0,0,0.7));
        }
        
        /* Aseguramos que la palabra "to" mantenga de forma estricta la misma grafía, grosor y cromo */
        h1 span.same-font-to {
            font-family: 'Ole Script', cursive;
            font-weight: 700;
            font-size: 90px;
            margin: 0 4px;
            background: linear-gradient(
                to bottom, 
                #ffffff 0%, 
                #f1f5f9 42%, 
                #475569 48%, 
                #0f172a 53%, 
                #cbd5e1 68%, 
                #ffffff 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .card { 
            background: rgba(253, 246, 226, 0.95); /* Color crema clásico de taller */
            padding: 40px; 
            border-radius: 4px; 
            text-align: center; 
            max-width: 440px; 
            width: 90%; 
            border: 4px solid #0f172a; 
            box-shadow: 12px 12px 0px #0f172a, 0px 20px 50px rgba(0,0,0,0.5); 
            margin-top: 26vh; 
            position: relative;
            z-index: 5;
        }
        
        p { 
            color: #0f172a; 
            font-size: 15px; 
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 700;
            margin: 10px 0 30px 0;
            border-bottom: 2px dashed #0f172a;
            padding-bottom: 15px;
        }
        
        input[type="text"] { 
            width: 100%; 
            padding: 14px; 
            border: 3px solid #0f172a; 
            background: #ffffff; 
            color: #0f172a; 
            border-radius: 0px; 
            font-size: 14px; 
            box-sizing: border-box; 
            font-family: 'Oswald', sans-serif;
            text-align: center;
            font-weight: bold;
        }
        
        input[type="text"]:focus { 
            outline: none;
            background: #fffef9;
            border-color: #cf483a;
        }
        
        button { 
            background: #cf483a; 
            color: #fdf6e2; 
            border: 3px solid #0f172a; 
            width: 100%; 
            padding: 15px; 
            margin-top: 25px; 
            font-size: 18px; 
            font-weight: 700; 
            text-transform: uppercase;
            letter-spacing: 2px;
            border-radius: 0px; 
            cursor: pointer; 
            box-shadow: 4px 4px 0px #0f172a;
            transition: all 0.1s ease;
        }
        
        button:hover { 
            transform: translate(2px, 2px); 
            box-shadow: 2px 2px 0px #0f172a;
            background: #b5392d;
        }
        
        .footer { 
            margin-top: 30px; 
            font-size: 11px; 
            color: #475569; 
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
        }
    </style>
</head>
<body>

    <div class="header-container">
        <!-- El texto completo replica la tipografía hilada del emblema real, manteniendo el "to" integrado -->
        <h1>YT <span class="same-font-to">to</span> MP3</h1>
    </div>

    <div class="card">
        <p>AUDIO EXTRACTION TERMINAL</p>
        <form action="/convertir" method="POST">
            <input type="text" name="url" placeholder="PASTE YOUTUBE LINK HERE" required>
            <button type="submit">START CONVERSION</button>
        </form>
        <div class="footer">SALT LAKE CITY OUTPOST</div>
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
