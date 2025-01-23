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

            # Add progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Process transcription
            status_text.text("Procesando archivo de audio...")
            progress_bar.progress(25)

            transcription = transcriber.transcribe(audio_path)
            progress_bar.progress(100)
            status_text.text("¡Transcripción completada!")

            # Display results in tabs
            tab1, tab2 = st.tabs(["📝 Previsualización", "📋 Texto Completo"])

            with tab1:
                st.markdown("### Previsualización")
                preview_length = min(500, len(transcription))
                st.markdown(transcription[:preview_length] + ("..." if len(transcription) > 500 else ""))

            with tab2:
                st.markdown("### Transcripción Completa")
                st.text_area(
                    "Texto transcrito",
                    value=transcription,
                    height=300,
                    key="transcription"
                )

                # Copy button
                if st.button("📋 Copiar al Portapapeles"):
                    st.write('<script>navigator.clipboard.writeText(`' + 
                            transcription.replace('`', '\\`') + 
                            '`);</script>', unsafe_allow_html=True)
                    st.success("¡Texto copiado al portapapeles!")

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