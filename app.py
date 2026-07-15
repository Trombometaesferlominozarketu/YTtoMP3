import os
import uuid
from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():

    url = request.form.get("url")

    if not url:
        return "Invalid URL", 400

    unique = str(uuid.uuid4())

    output_template = os.path.join(
        DOWNLOAD_FOLDER,
        unique + ".%(ext)s"
    )

    ydl_opts = {

        "format": "bestaudio/best",

        "noplaylist": True,

        "restrictfilenames": True,

        "outtmpl": output_template,

        "postprocessors": [

            {

                "key": "FFmpegExtractAudio",

                "preferredcodec": "mp3",

                "preferredquality": "192",

            }

        ],

    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            ydl.extract_info(url, download=True)

        mp3 = os.path.join(DOWNLOAD_FOLDER, unique + ".mp3")

        @after_this_request
        def remove(response):

            try:
                os.remove(mp3)
            except:
                pass

            return response

        return send_file(
            mp3,
            as_attachment=True,
            download_name="music.mp3"
        )

    except Exception as e:

        return f"<h2>Error</h2><pre>{e}</pre>"


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
