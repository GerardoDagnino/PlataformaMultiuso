from flask import Flask, render_template, request, send_file
import youtube_dl

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        tipo_descarga = request.form["tipo_descarga"]
        
        # Descargar el video o audio
        try:
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',  # Nombre de archivo basado en el título del video
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if tipo_descarga == "video":
                    # Descargar el video
                    ydl.download([url])
                    filename = f"{info['title']}.mp4"
                elif tipo_descarga == "audio":
                    # Descargar el audio
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                    ydl.download([url])
                    filename = f"{info['title']}.mp3"
                else:
                    return render_template("index.html", mensaje="Tipo de descarga no válido")

            # Proporcionar enlace de descarga
            return render_template("descarga.html", filename=filename)
        
        except Exception as e:
            return render_template("index.html", mensaje=f"Error: {e}")
    
    return render_template("index.html")

@app.route("/descargar/<filename>")
def descargar_archivo(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
