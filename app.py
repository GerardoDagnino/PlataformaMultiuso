import os
from flask import Flask, render_template, request
from pytube import YouTube
import time

app = Flask(__name__)

def get_default_download_path():
    """Obtiene la ruta predeterminada de descarga del sistema operativo."""
    if os.name == 'nt':  # Windows
        import winreg
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            try:
                location, _ = winreg.QueryValueEx(key, downloads_guid)
                return location
            except FileNotFoundError:
                return None
    elif os.name == 'posix':  # macOS y Linux
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        return None

def descargar_video(url, ruta_descarga):
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download(output_path=ruta_descarga)
        time.sleep(30)  # Espera 5 segundos entre cada descarga
        return True, yt.title
    except Exception as e:
        return False, str(e)

def descargar_audio(url, ruta_descarga):
    try:
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        audio.download(output_path=ruta_descarga)
        time.sleep(30)  # Espera 5 segundos entre cada descarga
        return True, yt.title
    except Exception as e:
        return False, str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        tipo_descarga = request.form["tipo_descarga"]
        ruta_descarga = get_default_download_path()
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
    app.run(host='0.0.0.0', port=8080)
