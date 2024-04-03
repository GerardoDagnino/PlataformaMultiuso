from flask import Flask, render_template, request, jsonify
import youtube_dl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descargar_video', methods=['POST'])
def descargar_video():
    url = request.form['url']
    try:
        ydl_opts = {
            'verbose': True  # Agregar el flag --verbose
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
        return jsonify({'mensaje': '¡Video descargado correctamente!'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
