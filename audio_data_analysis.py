import os
import librosa  # for audio loading and extracting features
import tensorflow as tf  # for loading the machine learning model
import numpy as np  # for normalizing and reshaping audio features

model_relative_path = "../backend/Emotion_Voice_Detection_Model.h5"
model_absolute_path = os.path.abspath(model_relative_path)
model = tf.keras.models.load_model(model_absolute_path)  # load the model


# function to extract and normalize features from audio file
def preprocess_audio(file_path, target_shape=(216, 1)):

    y, sr = librosa.load(file_path, sr=None)  # load audio file

    features = librosa.feature.mfcc(
        y=y, sr=sr, n_mfcc=13, hop_length=512
    )  # extract features

    features_flat = features.flatten(
        "F"
    )  # flatten the features along the last axis ('F' means flatten in column-major order)

    features_flat = features_flat[: np.prod(target_shape)]  # truncate if larger
    features_flat = np.pad(
        features_flat, (0, np.prod(target_shape) - len(features_flat))
    )

    features_flat = (features_flat - np.mean(features_flat)) / np.std(
        features_flat
    )  # normalize features
    # z = (x - mean) / standard deviation

    return features_flat.reshape(target_shape)


# function to predict emotions from extracted audio features
def predict_emotion(model, features):

    features = np.reshape(
        features, (-1, 216, 1)
    )  # reshape features to match the model's expected input shape

    predictions = model.predict(features)  # make predictions

    return predictions


directory = os.path.join(os.path.dirname(__file__), "audios_for_analysis")

# listing all files in the directory
file = os.listdir(directory)

# constructing absolute paths for the file
file_path = os.path.join(directory, file[0])

audio_features = preprocess_audio(file_path)

emotion_predictions = predict_emotion(model, audio_features)

# The model's output is a 2D array, reshape it into a 1D array and then convert it into a list to perform operations easily
emotion_predictions = emotion_predictions.reshape(10).tolist()

# The model's output is a probability distribution over different over different emotions. Each element in the output array represents the probability of the audio belonging to a specific emotion class.
emotion_labels = [
    "female_angry",
    "female_calm",
    "female_fearful",
    "female_happy",
    "female_sad",
    "male_angry",
    "male_calm",
    "male_fearful",
    "male_happy",
    "male_sad",
]

emotion_labels_and_predictions = dict()  # merging emotion labels and predictions

for i in emotion_labels:
    for j in emotion_predictions:
        emotion_labels_and_predictions[i] = j
        emotion_predictions.remove(j)
        break


# separating emotions from the dictionary
fearful = []
sad = []

happy = []
angry = []
calm = []

for i in emotion_labels_and_predictions.items():
    list_of_emotions = ["fearful", "sad", "happy", "angry", "calm"]
    for j in list_of_emotions:
        if j in i[0]:
            eval(j).append(i)


# function to add values for each emotion
def add_emotion_values(emotion):

    sum = 0
    for i in emotion:
        sum += i[1]

    return sum


fearful = add_emotion_values(fearful)
sad = add_emotion_values(sad)

happy = add_emotion_values(happy)
angry = add_emotion_values(angry)
calm = add_emotion_values(calm)

# nervousness and confidence calculated in speech
nervousness_in_speech = fearful + sad
confidence_in_speech = happy + angry + calm
