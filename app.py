import streamlit as st
import requests
import assemblyai as aai
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips
import librosa
import numpy as np
import soundfile as sf

# Set up API keys
assemblyai_api_key = ""
play_ht_api_key = ""
play_ht_user_id = ""


# Initialize AssemblyAI
aai.settings.api_key = assemblyai_api_key
transcriber = aai.Transcriber()

# Streamlit UI
st.title("Video Audio Replacement with AI Voice")
st.write("Upload a video file with audio that needs improvement.")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save uploaded video to a temporary file
    with open("input_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract audio from video
    video = VideoFileClip("input_video.mp4")
    video.audio.write_audiofile("input_audio.wav")

    # Transcribe audio using AssemblyAI
    st.write("Transcribing audio...")
    transcript = transcriber.transcribe("input_audio.wav")
    st.write("Transcription:")
    st.text_area("Transcription Output:", transcript.text, height=200)

    # Analyze audio speed in 1-second segments
    y, sr = librosa.load("input_audio.wav", sr=None)
    segment_length = 1  # Length of each segment in seconds
    audio_durations = []  # Store the duration of each segment

    # Calculate tempo for each segment
    for start in range(0, len(y), sr * segment_length):
        segment = y[start:start + sr * segment_length]
        if len(segment) > 0:
            duration = librosa.get_duration(y=segment, sr=sr)
            audio_durations.append(duration)

    # Generate AI voice using Play.ht
    st.write("Generating AI voice...")
    play_ht_url = 'https://api.play.ht/api/v2/tts/stream'
    headers = {
        'X-USER-ID': play_ht_user_id,
        'AUTHORIZATION': play_ht_api_key,
        'accept': 'audio/mpeg',
        'content-type': 'application/json'
    }

    data = {
        "text": transcript.text,
        "voice_engine": "Play3.0",
        "voice": "s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
        "output_format": "mp3"
    }

    response = requests.post(play_ht_url, json=data, headers=headers, stream=True)

    if response.status_code == 200:
        with open('ai_generated_audio.mp3', 'wb') as audio_file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    audio_file.write(chunk)
        st.success("AI Audio generated successfully.")

        # Analyze the AI-generated audio for duration adjustments
        ai_audio, ai_sr = librosa.load("ai_generated_audio.mp3", sr=None)
        new_audio_segments = []

        # Iterate through the segments and adjust speed to match original
        for i, original_duration in enumerate(audio_durations):
            start = i * sr * segment_length
            end = min(len(ai_audio), (i + 1) * sr * segment_length)
            ai_segment = ai_audio[start:end]
            
            # Adjust the speed of AI segment
            current_duration = librosa.get_duration(y=ai_segment, sr=ai_sr)
            speed_ratio = current_duration / original_duration
            adjusted_segment = librosa.effects.time_stretch(ai_segment, rate=speed_ratio)
            
            new_audio_segments.append(adjusted_segment)

        # Concatenate the adjusted segments
        final_audio = np.concatenate(new_audio_segments)
        sf.write("stretched_ai_audio.wav", final_audio, ai_sr)

        # Load the adjusted AI audio
        aligned_audio = AudioFileClip("stretched_ai_audio.wav")

        # Combine the new aligned audio with the video
        final_video = video.set_audio(aligned_audio)
        final_video.write_videofile("output_video_with_aligned_audio.mp4")

        # Provide download link for the final video
        with open("output_video_with_aligned_audio.mp4", "rb") as file:
            st.download_button(
                label="Download Processed Video",
                data=file,
                file_name="output_video_with_aligned_audio.mp4",
                mime="video/mp4"
            )
    else:
        st.error(f"Failed to generate audio. Status Code: {response.status_code}")
        st.error(response.text)
