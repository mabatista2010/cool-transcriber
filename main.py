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
    st.write("---")
    st.subheader("📝 Resultado de la Transcripción")

    # Container for transcription
    with st.container():
        st.markdown(
            f"""
            <div style='background-color: #F0F2F6; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                {format_transcription(transcription)}
            </div>
            """,
            unsafe_allow_html=True
        )

        # Buttons for actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copiar al Portapapeles", key="copy_btn", use_container_width=True):
                pyperclip.copy(transcription)
                st.success("¡Transcripción copiada al portapapeles! ✅")

        with col2:
            st.download_button(
                label="⬇️ Descargar Transcripción",
                data=transcription,
                file_name="transcripcion.txt",
                mime="text/plain",
                key="download_btn",
                use_container_width=True
            )

def main():
    st.title("🎙️ Audio to Text Transcription")

    # Sidebar with supported formats
    st.sidebar.header("Formatos Soportados")
    supported_formats = get_supported_formats()
    st.sidebar.write(", ".join(supported_formats))

    # Custom CSS
    st.markdown("""
    <style>
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
    }
    .stDownloadButton > button {
        background-color: #FF4B4B;
        color: white;
    }
    .stProgress .st-bo {
        background-color: #FF4B4B;
    }
    div[data-testid="stFileUploader"] > section > input + div > button {
        background-color: #FF4B4B;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Sube tu archivo de audio",
        type=supported_formats,
        help="Sube un archivo de audio para transcribir"
    )

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            audio_path = tmp_file.name

        try:
            transcriber = AudioTranscriber()

            with st.spinner("🎵 Procesando archivo de audio..."):
                transcription = transcriber.transcribe(audio_path)
                st.success("✨ ¡Transcripción completada!")

                # Show the transcription in the elegant container
                show_transcription_modal(transcription)

        except Exception as e:
            st.error(f"❌ Ocurrió un error: {str(e)}")

        finally:
            # Clean up temporary file
            os.unlink(audio_path)

if __name__ == "__main__":
    main()