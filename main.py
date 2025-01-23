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

    # Add tabs for file upload and YouTube URL
    tab1, tab2 = st.tabs(["Archivo de Audio", "Video de YouTube"])

    with tab1:
        # File upload
        uploaded_file = st.file_uploader(
            "Sube tu archivo de audio",
            type=supported_formats,
            help="Sube un archivo de audio para transcribir"
        )

        if uploaded_file is not None:
            # Create a temporary file to store the uploaded audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                audio_path = tmp_file.name

            process_transcription(audio_path, is_youtube_url=False)

            # Clean up temporary file
            os.unlink(audio_path)

    with tab2:
        # YouTube URL input
        youtube_url = st.text_input(
            "URL del video de YouTube",
            help="Ingresa la URL de un video de YouTube para transcribir su audio"
        )

        if youtube_url:
            process_transcription(youtube_url, is_youtube_url=True)

def process_transcription(input_path, is_youtube_url=False):
    try:
        # Initialize transcriber
        transcriber = AudioTranscriber()

        # Add progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Process transcription
        status_text.text("Procesando audio...")
        progress_bar.progress(25)

        transcription = transcriber.transcribe(input_path, is_youtube_url)
        progress_bar.progress(100)
        status_text.text("¡Transcripción completada!")

        # Display results
        st.subheader("Resultado de la Transcripción")
        formatted_text = format_transcription(transcription)
        st.markdown(formatted_text)

        # Download button
        st.download_button(
            label="Descargar Transcripción",
            data=transcription,
            file_name="transcripcion.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"Ocurrió un error: {str(e)}")

if __name__ == "__main__":
    main()