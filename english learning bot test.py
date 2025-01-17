import streamlit as st
from gtts import gTTS
import os
import time
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play

# Configure page
st.set_page_config(page_title="AI Learning Bot", page_icon="🎓", layout="wide")

# Navigation
st.sidebar.title("Navigation")
options = ["Video Lessons", "Quiz Section", "Pronunciation Bot"]
choice = st.sidebar.radio("Go to:", options)

# Initialize session state
if "lesson_completed" not in st.session_state:
    st.session_state.lesson_completed = False

# Helper: Function to extract audio from video and transcribe
def transcribe_video_audio(video_path):
    try:
        # Convert video to audio
        audio_path = "temp_audio.wav"
        clip = AudioSegment.from_file(video_path)
        clip.export(audio_path, format="wav")

        # Initialize recognizer
        recognizer = sr.Recognizer()
        audio_file = sr.AudioFile(audio_path)

        with audio_file as source:
            audio_data = recognizer.record(source)

        # Transcribe the audio
        text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return ""

# Video Lessons Section
if choice == "Video Lessons":
    st.title("Video Lessons with Live Text")
    lesson_videos = {
        "Lesson 1: Basics": "E:/videos for english learning site/lesson 1/champions anthem.mp4",
        "Lesson 2: Common Phrases": "E:/videos for english learning site/lesson 2/take it easy.mp4"
    }
    lesson_selected = st.selectbox("Choose a Lesson:", list(lesson_videos.keys()))
    video_path = lesson_videos[lesson_selected]
    st.video(video_path)

    # Simulate dynamic text appearing below the video
    st.subheader("Live Text Below Video")
    if st.button("Start Video and Text Simulation"):
        try:
            # Transcribe video audio
            transcribed_text = transcribe_video_audio(video_path)
            if transcribed_text:
                st.text_area("Live Transcription:", transcribed_text, height=200)
        except Exception as e:
            st.error(f"Error during video processing: {e}")

    # Complete Video Button
    if st.button("Complete Video and Proceed"):
        st.session_state.lesson_completed = True
        st.success("Video completed! Proceed to the quiz.")

# Quiz Section
elif choice == "Quiz Section":
    st.title("Quiz Section")
    if not st.session_state.lesson_completed:
        st.warning("Please complete a video lesson before attempting the quiz.")
    else:
        st.write("Answer the following questions:")
        q1 = st.radio("Question 1: What is the capital of France?", ["London", "Paris", "Berlin"])
        q2 = st.radio("Question 2: What is 5 + 7?", ["10", "12", "15"])

        if st.button("Submit Quiz"):
            score = 0
            if q1 == "Paris":
                score += 1
            if q2 == "12":
                score += 1
            st.success(f"You scored {score}/2!")

# Pronunciation Bot Section
elif choice == "Pronunciation Bot":
    st.title("Pronunciation Bot")
    st.write("Type a word or sentence to hear its pronunciation.")

    user_input = st.text_area("Enter text:", max_chars=500)
    if user_input and st.button("Generate Pronunciation"):
        save_path = "C:/Users/asus/AppData/Local/Programs/Python/Python312/english learning app/pronounciation bot"
        audio_path = "C:/Users/asus/AppData/Local/Programs/Python/Python312/english learning app/pronounciation bot"
        os.makedirs(save_path, exist_ok=True)
        audio_path = os.path.join(save_path, f"{user_input}_pronunciation.mp3")
        tts = gTTS(user_input, lang='en')
        tts.save(audio_path)
        st.audio(audio_path)
        st.success(f"Pronunciation saved at: {audio_path}")


