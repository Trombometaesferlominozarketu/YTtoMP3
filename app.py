import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = '/tmp/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Diseño industrial de 1950 con letras 3D de hierro y fondo real del atardecer en SLC
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT to MP3 - 1950 Industrial Iron</title>
    <!-- Cargamos fuentes tipográficas pesadas de estilo bloque industrial clásico -->
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Alfa+Slab+One&family=Lilita+One&family=Oswald:wght@700&display=swap" rel="stylesheet">
    
    <style>
        body { 
            margin: 0;
            padding: 0;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh;
            /* Imagen real de fondo inspirada en tu toma aérea del atardecer de Salt Lake City */
            background: linear-gradient(rgba(30, 17, 42, 0.4), rgba(58, 28, 63, 0.45)), 
                        url('https://unsplash.com');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            font-family: 'Oswald', sans-serif;
        }
        
        .header-container {
            position: absolute;
            top: 5vh;
            width: 100%;
            text-align: center;
        }

        /* TÍTULO ENORME DE HIERRO EN 3D ESTILO 1950 */
        h1 { 
            font-family: 'Alfa Slab One', cursive;
            font-size: 90px; /* Enorme arriba */
            margin: 0;
            padding: 0;
            text-align: center;
            letter-spacing: -2px;
            color: #2b2b2a; /* Tono hierro oscuro envejecido */
            text-transform: uppercase;
            line-height: 0.9;
            
            /* Capas de sombras pesadas e inclinadas simulando relieve tridimensional de metal macizo */
            text-shadow: 
                1px 1px 0px #3d3d3c,
                2px 2px 0px #1a1a19,
                3px 3px 0px #1a1a19,
                4px 4px 0px #111110,
                5px 5px 0px #111110,
                6px 6px 0px #090909,
                7px 7px 0px #090909,
                8px 8px 15px rgba(0, 0, 0, 0.8),
                12px 12px 30px rgba(0, 0, 0, 0.6);
        }
        
        /* Modificador específico exigido para el "to" en minúsculas */
        h1 span.lowercase-to {
            text-transform: lowercase;
            font-family: 'Lilita One', sans-serif;
            font-size: 75px;
            color: #d1cdc4; /* Contraste metálico más claro o galvanizado */
            margin: 0 10px;
            text-shadow: 
                1px 1px 0px #a3a099,
                2px 2px 0px #1a1a19,
                3px 3px 0px #1a1a19,
                4px 4px 5px rgba(0, 0, 0, 0.6);
        }

        .card { 
            background: rgba(253, 246, 226, 0.93); /* Tarjeta color crema vintage con ligera transparencia */
            padding: 40px; 
            border-radius: 2px; 
            text-align: center; 
            max-width: 440px; 
            width: 90%; 
            border: 4px solid #1a1a19; 
            box-shadow: 10px 10px 0px #1a1a19, 0px 20px 40px rgba(0,0,0,0.5); 
            margin-top: 15vh; /* Ajuste para dejar espacio al gran letrero superior */
        }
        
        p { 
            color: #1a1a19; 
            font-size: 15px; 
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 700;
            margin: 0 0 30px 0;
            border-bottom: 2px dashed #1a1a19;
            padding-bottom: 15px;
        }
        
        input[type="text"] { 
            width: 100%; 
            padding: 14px; 
            border: 3px solid #1a1a19; 
            background: #ffffff; 
            color: #1a1a19; 
            border-radius: 0px; 
            font-size: 14px; 
            box-sizing: border-box; 
            font-family: 'Oswald', sans-serif;
            text-align: center;
            font-weight: bold;
        }
        
        input[type="text"]:focus { 
            outline: none;
            background: #fffdf5;
            border-color: #8c271e;
        }
        
        button { 
            background: #cf483a; /* Botón rojo óxido clásico */
            color: #fdf6e2; 
            border: 3px solid #1a1a19; 
            width: 100%; 
            padding: 15px; 
            margin-top: 25px; 
            font-size: 18px; 
            font-weight: 700; 
            text-transform: uppercase;
            letter-spacing: 2px;
            border-radius: 0px; 
            cursor: pointer; 
            box-shadow: 4px 4px 0px #1a1a19;
            transition: all 0.1s ease;
        }
        
        button:hover { 
            transform: translate(2px, 2px); 
            box-shadow: 2px 2px 0px #1a1a19;
            background: #e05345;
        }
        
        .footer { 
            margin-top: 30px; 
            font-size: 11px; 
            color: #57544d; 
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
        }
    </style>
</head>
<body>

    <div class="header-container">
        <!-- Letras enormes en mayúsculas menos "to" -->
        <h1>YT <span class="lowercase-to">to</span> MP3</h1>
    </div>

    <div class="card">
        <p>AUDIO EXTRACTION TERMINAL</p>
        <form action="/convertir" method="POST">
            <input type="text" name="url" placeholder="PASTE YOUTUBE LINK HERE" required>
            <button type="submit">START CONVERSION</button>
        </form>
        <div class="footer">SALT LAKE CITY • UTAH OUTPOST</div>
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
