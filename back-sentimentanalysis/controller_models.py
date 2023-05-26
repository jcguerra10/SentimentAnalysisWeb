import tensorflow as tf
import numpy as np
import librosa
import scipy.fft
import pickle
import os
import warnings
from keras.models import load_model

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

if tf.test.gpu_device_name():
    print('GPU found')
else:
    print("No GPU found")

#warnings.filterwarnings("ignore", message="n_fft=2048 is too large for input signal of length=1304")


def extract_features_from_audio(audio_data, frame_len, hop_len):
    frames = librosa.util.frame(audio_data, frame_length=frame_len, hop_length=hop_len)
    windowed_frames = np.hanning(frame_len).reshape(-1, 1) * frames

    features = []

    for frame in windowed_frames:
        result = np.array([])
        mfcc = np.mean(librosa.feature.mfcc(y=frame, sr= 22050).T, axis=0)
        result = np.hstack((result, mfcc))

        dft = np.mean(librosa.stft(y=frame))
        result = np.hstack((result, dft))

        dct = np.mean(scipy.fft.dct(frame))
        result = np.hstack((result, mfcc))

        features.append(result)

    features_matrix = np.array(features)
    features_matrix = features_matrix[1:-1]

    return features_matrix


def process_wav_file(file_path):
    # Carga el modelo desde el archivo
    modelo_cargado = load_model('./models/model_audio.h5')

    # Carga el scaler desde el archivo
    with open('./helpers/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Parámetros para la extracción de características
    minima = 1.48
    frame_len = 50
    hop_len = 25

    # Carga el archivo WAV y obtiene la frecuencia de muestreo y los datos de audio
    audio, sr = librosa.load(file_path, sr=22050)

    # Calcula la longitud de la ventana en muestras
    longitud_ventana = int(minima * sr)

    if len(audio) >= longitud_ventana:
        # Calcula el centro del audio
        centro_audio = len(audio) // 2

        # Retrocede y avanza la mitad de la longitud de la ventana
        inicio_ventana = centro_audio - (longitud_ventana // 2)
        fin_ventana = centro_audio + (longitud_ventana // 2)

        # Extrae los datos dentro de la ventana
        datos_ventana = audio[inicio_ventana:fin_ventana]

        fTest = extract_features_from_audio(datos_ventana, frame_len, hop_len)
        fTest = np.real(fTest)

        arr_reshaped = fTest.reshape(1, -1)

        # Escalado de características
        escalado = scaler.transform(arr_reshaped)
        escalado = np.expand_dims(escalado, axis=2)

        # Predicción con el modelo cargado
        predicciones = modelo_cargado.predict(escalado)

        # Convierte las probabilidades en porcentajes
        probabilidades = np.round(predicciones * 100, 2)

        return probabilidades

    else:
        return None
