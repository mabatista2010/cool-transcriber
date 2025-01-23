import streamlit as st
import os
import tempfile
import pyperclip
from audio_processor import AudioTranscriber
from utils import get_supported_formats, format_transcription

st.set_page_config(
    page_title="Audio Transcription App",
    page_icon="🎙️",
    layout="wide"
)

def show_transcription_modal(transcription):
    """Display transcription in an elegant container with actions."""
    st.markdown("### 📝 Resultado de la Transcripción")

    # Container with custom styling for the transcription
    with st.container(border=True):
        st.markdown(
            f"""
            <div style='background-color: #F0F2F6; padding: 20px; border-radius: 10px;'>
                {format_transcription(transcription)}
            </div>
            """,
            unsafe_allow_html=True
        )

    # Create two columns for the buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 Copiar al Portapapeles", key="copy_btn"):
            pyperclip.copy(transcription)
            st.toast("¡Transcripción copiada al portapapeles!", icon="✅")

    with col2:
        st.download_button(
            label="⬇️ Descargar Transcripción",
            data=transcription,
            file_name="transcripcion.txt",
            mime="text/plain",
            key="download_btn"
        )

def main():
    st.title("🎙️ Audio to Text Transcription")

    # Sidebar with supported formats
    st.sidebar.header("Formatos Soportados")
    supported_formats = get_supported_formats()
    st.sidebar.write(", ".join(supported_formats))

    # File upload with improved styling
    st.markdown("""
    <style>
    .stFileUploader > div > div > button {
        background-color: #FF4B4B;
        color: white;
    }
    .stProgress .st-bo {
        background-color: #FF4B4B;
    }
    </style>
    """, unsafe_allow_html=True)

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

        try:
            # Initialize transcriber
            transcriber = AudioTranscriber()

            # Add progress bar with custom styling
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Process transcription with improved status messages
            status_text.text("🎵 Procesando archivo de audio...")
            progress_bar.progress(25)

            transcription = transcriber.transcribe(audio_path)
            progress_bar.progress(100)
            status_text.text("✨ ¡Transcripción completada!")

            # Show the transcription in the elegant container
            show_transcription_modal(transcription)

        except Exception as e:
            st.error(f"❌ Ocurrió un error: {str(e)}")

        finally:
            # Clean up temporary file
            os.unlink(audio_path)

if __name__ == "__main__":
    main()