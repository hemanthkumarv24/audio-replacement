#  Video Audio Replacement with AI Voice
This project allows users to replace the audio of a video file with an AI-generated voice. Built using Streamlit, AssemblyAI, Play.ht, and MoviePy, it enables transcription, speed analysis, and audio synchronization, creating a final video with enhanced AI audio.

## Features
Video Upload: Upload a video file (.mp4, .mov, .avi).
Audio Extraction: Extracts the audio track from the uploaded video.
Audio Transcription: Converts audio to text using AssemblyAI.
AI Audio Generation: Synthesizes a new AI voice based on transcription text with Play.ht.
Speed Analysis: Matches the AI-generated audio to the original audio's speed.
Video Rendering: Merges AI audio back into the video.
Download Option: Download the final video with the synchronized AI audio.
Requirements
Python 3.8+
Streamlit
AssemblyAI SDK
MoviePy
Librosa
NumPy
Soundfile
Requests
Setup
Clone the repository:


git clone https://github.com/your_username/video-audio-replacement.git
cd video-audio-replacement
Install dependencies:


pip install -r requirements.txt
Set up API keys in the script (Replace placeholder keys with your AssemblyAI and Play.ht credentials).

Run the application:


streamlit run app.py
Usage
Open the Streamlit app in a browser.
Upload a video file you wish to process.
Wait for the audio extraction, transcription, and AI audio generation to complete.
Download the processed video with AI-generated audio.
File Structure
app.py: Main application file.
requirements.txt: Lists all required Python packages.
API Reference
AssemblyAI: Used for transcribing audio.
Play.ht: Used to generate AI audio from the transcription.
Notes
File Size: Processing may take a while for larger files.
Audio Length: Works best with shorter audio segments for alignment accuracy.
License
This project is licensed under the MIT License.
