from flask import Flask, render_template, request
from pytube import YouTube

app = Flask(__name__)

def descargar_video(url, ruta_descarga):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path=ruta_descarga)
        return True, yt.title
    except Exception as e:
        return False, str(e)

def descargar_audio(url, ruta_descarga):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        audio.download(output_path=ruta_descarga)
        return True, yt.title
    except Exception as e:
        return False, str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        tipo_descarga = request.form["tipo_descarga"]
        ruta_descarga = request.form["ruta_descarga"]  # Obtener la ruta de descarga del formulario
        if tipo_descarga == "video":
            success, mensaje = descargar_video(url, ruta_descarga)
        elif tipo_descarga == "audio":
            success, mensaje = descargar_audio(url, ruta_descarga)
        else:
            success = False
            mensaje = "Tipo de descarga no válido"

        if success:
            return render_template("index.html", mensaje=f"Descarga completada: {mensaje}")
        else:
            return render_template("index.html", mensaje=f"Error: {mensaje}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    
