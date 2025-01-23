import streamlit as st
import os
import tempfile
from audio_processor import AudioTranscriber
from utils import get_supported_formats, format_transcription

# Configuración de la página
st.set_page_config(
    page_title="Transcripción de Audio",
    page_icon="🎙️",
    layout="wide"
)

def main():
    st.title("🎙️ Transcripción de Audio a Texto")
    st.subheader("Transforma archivos de audio en texto con detección automática de idioma")

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
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                audio_path = tmp_file.name

            # Initialize transcriber
            transcriber = AudioTranscriber()

            # Add progress bar
            with st.spinner("Procesando archivo de audio..."):
                transcription = transcriber.transcribe(audio_path)

            # Show results
            st.write("---")
            st.subheader("Resultados")

            # Show transcription in expander
            with st.expander("Transcripción", expanded=True):
                st.write(format_transcription(transcription))
                if st.button("📋 Copiar al portapapeles"):
                    st.write(transcription, to_clipboard=True)
                    st.success("¡Texto copiado al portapapeles!")

            # Download button
            st.download_button(
                "📥 Descargar transcripción",
                data=transcription,
                file_name="transcripcion.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")

        finally:
            # Clean up temporary file
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.unlink(audio_path)

if __name__ == "__main__":
    main()