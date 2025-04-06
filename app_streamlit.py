import streamlit as st
import os
import base64
from gtts import gTTS
from tempfile import NamedTemporaryFile

# Set page configuration
st.set_page_config(
    page_title="Text to Speech Converter",
    page_icon="🔊",
    layout="centered"
)

# Title and description
st.title("Text to Speech Converter")
st.markdown("""
This simple tool converts your text into speech and allows you to download the resulting MP3 file.
Just enter your text in the box below, click the 'Generate Audio' button, and download your MP3.
""")

# Function to get binary file content as base64
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

# Text area for user input
text_input = st.text_area(
    "Enter your text here:",
    height=200,
    placeholder="Type or paste the text you want to convert to speech...",
    help="The text will be converted to speech using Google's Text-to-Speech service"
)

# Language selection
language_option = st.selectbox(
    "Select language:",
    options=[
        "English (UK)", 
        "English (US)", 
        "French", 
        "German", 
        "Spanish"
    ],
    index=0
)

# Map language options to gTTS language codes
language_mapping = {
    "English (UK)": "en-uk",
    "English (US)": "en-us",
    "French": "fr",
    "German": "de",
    "Spanish": "es"
}

# Speed/rate slider
speech_speed = st.slider(
    "Speech speed:",
    min_value=0.5,
    max_value=1.5,
    value=1.0,
    step=0.1,
    help="Adjust the speed of the generated speech (may not work with all voices)"
)

# Button to generate MP3
if st.button("Generate Audio"):
    if text_input:
        try:
            with st.spinner("Generating audio file..."):
                # Create a temporary file
                with NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    temp_filename = tmp_file.name
                
                # Convert text to speech
                selected_lang = language_mapping[language_option]
                tts = gTTS(text=text_input, lang=selected_lang, slow=(speech_speed < 1.0))
                tts.save(temp_filename)
                
                # Success message
                st.success("Audio generated successfully!")
                
                # Display audio player
                st.audio(temp_filename, format='audio/mp3')
                
                # Download button
                st.markdown(get_binary_file_downloader_html(temp_filename, 'Audio File'), unsafe_allow_html=True)
                
                # Add a note about the file
                st.info("Click the download link above to save the audio file to your device.")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter some text first.")

# Add a separator
st.markdown("---")

# Footer
st.markdown("""
### About this tool
This tool uses Google's Text-to-Speech (gTTS) service to convert text to speech.
An internet connection is required for this tool to work properly.
""") 