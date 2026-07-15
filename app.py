import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = '/tmp/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Diseño con tipografía unificada, recta, inclinada y maciza estilo emblema 1950
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT to MP3 - De Luxe Station</title>
    <!-- Importamos una fuente ultra-gruesa y geométrica ideal para el efecto bloque -->
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Archivo+Black&family=Oswald:wght@700&display=swap" rel="stylesheet">
    
    <style>
        body { 
            margin: 0;
            padding: 0;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh;
            /* Atardecer real en Salt Lake City sin filtros que lo oscurezcan */
            background-image: url('https://wikimedia.org');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-family: 'Oswald', sans-serif;
            overflow: hidden;
        }
        
        .header-container {
            position: absolute;
            top: 8vh;
            width: 100%;
            text-align: center;
            z-index: 10;
        }

        /* GRAFÍA UNIFICADA: LETRAS RECTAS, MUY GRUESAS E INCLINADAS EN BLOQUE */
        h1 { 
            font-family: 'Archivo Black', sans-serif;
            font-size: 80px; /* Tamaño masivo uniforme */
            margin: 0 auto;
            display: inline-block;
            text-transform: uppercase;
            letter-spacing: -4px; /* Letras muy juntas y compactas */
            font-style: normal;
            
            /* Inclinación exacta y paralela para todo el bloque de texto */
            transform: skewX(-15deg); 
            
            /* Efecto metálico cromado líquido reflectante */
            background: linear-gradient(
                to bottom, 
                #ffffff 0%, 
                #f1f5f9 40%, 
                #475569 48%, 
                #0f172a 52%, 
                #cbd5e1 65%, 
                #ffffff 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            
            /* Relieve macizo tridimensional biselado idéntico en cada letra */
            filter: drop-shadow(2px 2px 0px #ffffff)
                    drop-shadow(-1px -1px 0px #475569)
                    drop-shadow(5px 5px 0px #0f172a)
                    drop-shadow(8px 8px 12px rgba(0,0,0,0.6));
            
            line-height: 1;
        }
        
        /* Modificador estricto: "to" en minúsculas pero con la misma tipografía, grosor e inclinación */
        h1 span.lowercase-to {
            text-transform: lowercase;
            font-size: 70px; /* Ligeramente ajustado para armonizar la línea superior */
            margin: 0 4px;
            letter-spacing: -6px;
        }

        .card { 
            background: rgba(253, 246, 226, 0.94); /* Fondo crema limpio */
            padding: 40px; 
            border-radius: 2px; 
            text-align: center; 
            max-width: 440px; 
            width: 90%; 
            border: 4px solid #0f172a; 
            box-shadow: 12px 12px 0px #0f172a, 0px 20px 50px rgba(0,0,0,0.5); 
            margin-top: 24vh; 
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
        <!-- Todo el bloque comparte la misma fuente exacta e inclinación geométrica -->
        <h1>YT <span class="lowercase-to">to</span> MP3</h1>
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
