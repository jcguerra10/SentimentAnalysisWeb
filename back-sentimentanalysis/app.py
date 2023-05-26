from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
import tensorflow as tf
import os
from controller_models import process_wav_file

app = Flask(__name__)
cors = CORS(app, resources={r"/upload_audio": {"origins": "*"},
                            r"/upload_text": {"origins": "*"}})

model_audio = tf.keras.models.load_model('./models/model_audio.h5')


@app.route('/upload_audio', methods=['POST'])
def upload_file():
    # remove files if they exist
    if os.path.exists('original.wav'):
        os.remove('original.wav')
    if os.path.exists('converted.wav'):
        os.remove('converted.wav')

    file = request.files['file']
    audio = AudioSegment.from_file(file)

    # Ensure file is in wav format
    if file.filename.split('.')[-1] != 'wav':
        audio.export('converted.wav', format='wav')
    else:
        file.save('converted.wav')

    # Load audio file
    audioP = "converted.wav"
    probabilidades = process_wav_file(audioP)
    if probabilidades is not None:
        print(probabilidades)
        priority = ""
        if probabilidades[0][0] > 95:
            return jsonify({'message': "prioridad alta"}), 200
        else:
            return jsonify({'message': "prioridad baja"}), 200

    else:
        print("El archivo WAV es demasiado corto para el procesamiento")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
