from flask import Flask, request, jsonify
from flask_cors import CORS
from pydub import AudioSegment
import tensorflow as tf
from scipy.io import wavfile
import librosa
import os
from controller_models import process_wav_file

app = Flask(__name__)
cors = CORS(app, resources={r"/upload_audio": {"origins": "*"},
                            r"/upload_text": {"origins": "*"}})

#model_text = tf.keras.models.load_model('model_text.h5')
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
    else:
        print("El archivo WAV es demasiado corto para el procesamiento")

    return jsonify({'message': 'File uploaded and converted successfully'}), 200


@app.route('/upload_text', methods=['POST'])
def upload_text():
    text = request.form['text']
    with open('text.txt', 'w') as f:
        f.write(text)
    return jsonify({'message': 'Text uploaded successfully'}), 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
