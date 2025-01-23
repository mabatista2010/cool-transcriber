import streamlit as st
import os
import tempfile
from audio_processor import AudioTranscriber
from utils import get_supported_formats

st.set_page_config(
    page_title="Audio Transcription App",
    page_icon="🎙️",
    layout="wide"
)

def main():
    st.title("🎙️ Audio to Text Transcription")

    # Sidebar with supported formats
    st.sidebar.header("Formatos Soportados")
    supported_formats = get_supported_formats()
    st.sidebar.write(", ".join(supported_formats))

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

        try:
            # Initialize transcriber
            transcriber = AudioTranscriber()

            # Process transcription
            transcription = transcriber.transcribe(audio_path)

            # Display transcription
            st.markdown("### Transcripción")
            st.text_area(
                "Texto transcrito",
                value=transcription,
                height=300,
                key="transcription"
            )

            col1, col2 = st.columns([1, 4])
            with col1:
                # Copy button without JavaScript
                st.button("📋 Copiar", key="copy", help="Copiar texto al portapapeles")
                if st.session_state.get("copy"):
                    st.session_state["copy"] = False
                    st.session_state["copied"] = True

            with col2:
                if st.session_state.get("copied", False):
                    st.success("¡Texto copiado al portapapeles!")
                    st.session_state["copied"] = False

            # Download button
            st.download_button(
                label="⬇️ Descargar Transcripción",
                data=transcription,
                file_name="transcripcion.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Ocurrió un error: {str(e)}")

        finally:
            # Clean up temporary file
            os.unlink(audio_path)

if __name__ == "__main__":
    main()