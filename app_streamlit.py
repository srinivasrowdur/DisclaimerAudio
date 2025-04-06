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

# Create two columns for language settings
col1, col2 = st.columns(2)

# Column 1: Language selection
with col1:
    st.subheader("Input Language")
    st.markdown("Select the language of your input text:")
    
    language_option = st.selectbox(
        "Text Language:",
        options=[
            "English", 
            "French", 
            "German", 
            "Spanish",
            "Italian",
            "Portuguese"
        ],
        index=0,
        help="Select the language that your text is written in"
    )

# Column 2: Accent/Dialect selection (only shown for English)
with col2:
    st.subheader("Voice Accent")
    
    if language_option == "English":
        accent_option = st.selectbox(
            "English Accent:",
            options=[
                "British (UK)",
                "American (US)",
                "Australian",
                "Indian",
                "Irish"
            ],
            index=0,
            help="Select the accent for the generated speech"
        )
        
        # Map accent options to gTTS language codes
        accent_mapping = {
            "British (UK)": "en-gb",
            "American (US)": "en-us",
            "Australian": "en-au",
            "Indian": "en-in",
            "Irish": "en-ie"
        }
        selected_lang_code = accent_mapping[accent_option]
    else:
        # Map language options to gTTS language codes
        language_mapping = {
            "English": "en",
            "French": "fr",
            "German": "de",
            "Spanish": "es",
            "Italian": "it",
            "Portuguese": "pt"
        }
        selected_lang_code = language_mapping[language_option]
        
        st.info(f"Your text will be read with a native {language_option} voice.")

# Speed/rate slider
speech_speed = st.slider(
    "Speech speed:",
    min_value=0.5,
    max_value=1.5,
    value=1.0,
    step=0.1,
    help="Adjust the speed of the generated speech (only slow/normal options available with Google TTS)"
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
                tts = gTTS(text=text_input, lang=selected_lang_code, slow=(speech_speed < 1.0))
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
- You must enter text in the **same language** you select
- For English text, you can choose different accents
- An internet connection is required for this tool to work
""") 