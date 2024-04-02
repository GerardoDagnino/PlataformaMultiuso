from flask import Flask, render_template, request, send_file
from pytube import YouTube

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        tipo_descarga = request.form["tipo_descarga"]
        
        # Descargar el video o audio
        try:
            yt = YouTube(url)
            if tipo_descarga == "video":
                stream = yt.streams.get_highest_resolution()
                filename = f"{yt.title}.mp4"
            elif tipo_descarga == "audio":
                stream = yt.streams.filter(only_audio=True).first()
                filename = f"{yt.title}.mp3"
            else:
                return render_template("index.html", mensaje="Tipo de descarga no válido")

            # Descargar el archivo
            stream.download()
            
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
