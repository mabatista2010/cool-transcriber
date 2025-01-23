import streamlit as st
import os
import tempfile
from audio_processor import AudioTranscriber
from utils import get_supported_formats, format_transcription

st.set_page_config(
    page_title="Audio Transcription App",
    page_icon="🎙️",
    layout="wide"
)

def main():
    st.title("🎙️ Audio to Text Transcription")
    
    # Sidebar with supported formats
    st.sidebar.header("Supported Formats")
    supported_formats = get_supported_formats()
    st.sidebar.write(", ".join(supported_formats))
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your audio file",
        type=supported_formats,
        help="Upload an audio file to transcribe"
    )
    
    if uploaded_file is not None:
        # Create a temporary file to store the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            audio_path = tmp_file.name
        
        try:
            # Initialize transcriber
            transcriber = AudioTranscriber()
            
            # Add progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Process transcription
            status_text.text("Processing audio file...")
            progress_bar.progress(25)
            
            transcription = transcriber.transcribe(audio_path)
            progress_bar.progress(100)
            status_text.text("Transcription completed!")
            
            # Display results
            st.subheader("Transcription Result")
            formatted_text = format_transcription(transcription)
            st.markdown(formatted_text)
            
            # Download button
            st.download_button(
                label="Download Transcription",
                data=transcription,
                file_name="transcription.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        
        finally:
            # Clean up temporary file
            os.unlink(audio_path)
            
if __name__ == "__main__":
    main()
