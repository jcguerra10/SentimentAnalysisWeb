import tensorflow as tf


def predict_text(text):
    model_text = tf.keras.models.load_model('./models/model_text.h5')
    return model_text.predict([text])[0][0]


def predict_audio(audio):
    model_audio = tf.keras.models.load_model('./models/model_audio.h5')
    return model_audio.predict([audio])[0][0]
