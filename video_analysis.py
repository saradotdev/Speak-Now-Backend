import os

os.environ["OPENCV_HEADLESS"] = "1"
import cv2  # for capturing and reading video
from deepface import DeepFace  # for analyzing facial expressions in video frames
from moviepy.editor import VideoFileClip  # for extracting audio from video


# function to analyze video frame by frame to recognize emotions expressed
def analyze_video(video_path):

    cap = cv2.VideoCapture(video_path)

    emotions = []

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        emotions.append(result[0])

    cap.release()

    return emotions


# function to extract audio from video file
def extract_audio(video_path, output_audio_path):

    video_clip = VideoFileClip(video_path)  # load video clip

    audio_clip = video_clip.audio  # extract audio from video clip

    audio_clip.write_audiofile(output_audio_path)  # save audio to a file

    video_clip.close()
    audio_clip.close()


# sending video file to functions to recognize emotions and extract audio
directory = os.path.join(os.path.dirname(__file__), "videos_for_analysis")

# listing all files in the directory
file = os.listdir(directory)

# constructing absolute paths for the file
file_path = os.path.join(directory, file[0])

filename = (file[0].split("."))[0]

video_path = os.path.join(
    os.path.dirname(__file__), "videos_for_analysis", filename + ".mp4"
)
output_audio_path = os.path.join(
    os.path.dirname(__file__), "audios_for_analysis", filename + ".wav"
)

facial_expression_data = analyze_video(video_path)  # extracted emotions
extract_audio(video_path, output_audio_path)  # extracted audio
