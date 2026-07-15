import os
from flask import Flask, render_template_string, request, send_file
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = '/tmp/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Diseño definitivo años 50: letras cromadas tipo emblema de coche clásico y foto nítida de SLC
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YT to MP3 - De Luxe Chrome Station</title>
    <!-- Cargamos fuentes cursivas estilizadas y gruesas inspiradas en emblemas vintage -->
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Playfair+Display:ital,wght@1,900&family=Shrikhand&family=Oswald:wght@700&display=swap" rel="stylesheet">
    
    <style>
        body { 
            margin: 0;
            padding: 0;
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh;
            /* Foto nítida en alta definición del atardecer real de Salt Lake City */
            background: url('https://unsplash.com') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Oswald', sans-serif;
            overflow: hidden;
        }
        
        .header-container {
            position: absolute;
            top: 6vh;
            width: 100%;
            text-align: center;
            z-index: 10;
        }

        /* LETRAS MUY GRUESAS ESTILO EMBLEMA CROMADO "DE LUXE" DE 1950 */
        h1 { 
            font-family: 'Shrikhand', cursive;
            font-size: 100px; /* Enorme arriba */
            margin: 0;
            padding: 0;
            text-align: center;
            letter-spacing: -1px;
            
            /* Efecto de degradado metálico (Cromo Espejo) */
            background: linear-gradient(
                to bottom, 
                #ffffff 0%, 
                #e2e8f0 45%, 
                #475569 50%, 
                #0f172a 55%, 
                #cbd5e1 60%, 
                #ffffff 100%
            );
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            
            /* Relieve biselado tridimensional muy grueso y pesado */
            filter: drop-shadow(2px 2px 0px #ffffff) 
                    drop-shadow(-1px -1px 0px #475569)
                    drop-shadow(4px 4px 0px #0f172a)
                    drop-shadow(8px 8px 15px rgba(0,0,0,0.7));
            
            line-height: 1;
        }
        
        /* El "to" intercalado en minúsculas con estilo caligráfico de los 50 */
        h1 span.lowercase-to {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 900;
            font-size: 75px;
            margin: 0 10px;
            background: linear-gradient(to bottom, #ffffff 0%, #cbd5e1 50%, #475569 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            filter: drop-shadow(2px 2px 0px #0f172a);
        }

        .card { 
            background: rgba(253, 246, 226, 0.94); /* Tarjeta color crema vintage sutil */
            padding: 40px; 
            border-radius: 4px; 
            text-align: center; 
            max-width: 440px; 
            width: 90%; 
            /* Estilo caja de taller mecánico antiguo */
            border: 4px solid #0f172a; 
            box-shadow: 12px 12px 0px #0f172a, 0px 20px 50px rgba(0,0,0,0.5); 
            margin-top: 22vh; /* Deja espacio al gran letrero cromado */
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
            background: #cf483a; /* Rojo óxido vintage */
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
        <!-- Título enorme con efecto cromado biselado, todo en mayúsculas menos "to" -->
        <h1>YT <span class="lowercase-to">to</span> MP3</h1>
    </div>

    <div class="card">
        <p>AUDIO EXTRACTION TERMINAL</p>
        <form action="/convertir" method="POST">
            <input type="text" name="url" placeholder="PASTE YOUTUBE LINK HERE" required>
            <button type="submit">START CONVERSION</button>
        </form>
        <div class="footer">DE LUXE DESERT EDITION</div>
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
