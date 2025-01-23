import streamlit as st
import os
import tempfile
from audio_processor import AudioTranscriber
from utils import get_supported_formats, format_transcription

# Configuración de la página
st.set_page_config(
    page_title="Audio Transcription App",
    page_icon="🎙️",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .transcription-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .stExpander {
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .transcription-text {
        line-height: 1.6;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("🎙️ Audio to Text Transcription")

    # Sidebar con formatos soportados
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
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            audio_path = tmp_file.name

        try:
            # Inicializar transcriptor
            transcriber = AudioTranscriber()

            # Barra de progreso
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Procesar transcripción
            status_text.text("Processing audio file...")
            progress_bar.progress(25)

            transcription = transcriber.transcribe(audio_path)
            progress_bar.progress(100)
            status_text.text("Transcription completed!")

            # Modal con la transcripción
            with st.expander("📝 View Transcription", expanded=True):
                st.markdown("<div class='transcription-container'>", unsafe_allow_html=True)

                # Información del archivo
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**File:** {uploaded_file.name}")
                with col2:
                    st.download_button(
                        label="📥 Download",
                        data=transcription,
                        file_name="transcription.txt",
                        mime="text/plain"
                    )

                # Contenido de la transcripción
                st.markdown("<div class='transcription-text'>", unsafe_allow_html=True)
                formatted_text = format_transcription(transcription)
                st.markdown(formatted_text)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

        finally:
            # Limpiar archivo temporal
            os.unlink(audio_path)

if __name__ == "__main__":
    main()