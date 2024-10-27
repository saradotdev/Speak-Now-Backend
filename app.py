from flask import Flask, request, jsonify
from flask_cors import CORS  # Cross Origin Resource Sharing
import os
import uuid
import sys

app = Flask(__name__)
CORS(app)


def restart_server():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def empty_folder(folder_name):

    for file_name in os.listdir(folder_name):
        file_path = os.path.join(folder_name, file_name)
        os.remove(file_path)


filename = ""


@app.route("/api/upload_video", methods=["GET", "POST"])
def upload_video():

    global filename

    if request.method == "POST":

        video_file = request.files["video"]

        # creating the directory if it doesn't exist
        video_dir = os.path.join(os.path.dirname(__file__), "videos_for_analysis")
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)

        audio_dir = os.path.join(os.path.dirname(__file__), "audios_for_analysis")
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        # deleting previous video and audio files if any
        empty_folder("videos_for_analysis")
        empty_folder("audios_for_analysis")

        filename = str(uuid.uuid4())

        # saving new video file for analysis
        save_path = os.path.join(
            os.path.dirname(__file__), "videos_for_analysis", filename + ".mp4"
        )
        video_file.save(save_path)

        return jsonify({"success": "video posted successfully"})

    if request.method == "GET":
        from facial_expression_data_analysis import (
            nervousness_in_expressions,
            confidence_in_expressions,
        )
        from audio_data_analysis import nervousness_in_speech, confidence_in_speech

        # compiling results from expression and speech analysis
        nervousness = nervousness_in_expressions + nervousness_in_speech
        confidence = confidence_in_expressions + confidence_in_speech

        nervousness = int(nervousness)
        confidence = int(confidence)

        return jsonify({"nervousness": nervousness, "confidence": confidence})


@app.route("/api/delete_video", methods=["POST"])
def delete_video():

    # deleting video and audio files after analysis
    empty_folder("videos_for_analysis")
    empty_folder("audios_for_analysis")

    # restarting server to delete previous analysis results
    restart_server()

    return jsonify({"success": "Video deleted successfully"})


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Server is running successfully"})


if __name__ == "__main__":
    app.run()
