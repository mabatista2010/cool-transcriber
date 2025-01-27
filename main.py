import streamlit as st
import os
import tempfile
import json
from audio_processor import AudioTranscriber
from utils import get_supported_formats, format_transcription, generate_summary, download_youtube_audio

# Configuración de la página
st.set_page_config(
    page_title="Audio Transcription App",
    page_icon="🎙️",
    layout="wide"
)

# PWA Metadata y Service Worker
st.markdown("""
    <head>
        <link rel="manifest" href="/static/manifest.json">
        <meta name="theme-color" content="#f0f2f6">
        <link rel="apple-touch-icon" href="/static/icon-192x192.png">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
        <script>
            if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                    navigator.serviceWorker.register('/static/sw.js')
                        .then(function(registration) {
                            console.log('ServiceWorker registration successful');
                        })
                        .catch(function(err) {
                            console.log('ServiceWorker registration failed: ', err);
                        });
                });
            }
        </script>
    </head>
""", unsafe_allow_html=True)

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
    .summary-container {
        background-color: #e6f3ff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .key-points {
        margin-top: 15px;
        padding-left: 20px;
    }
    .key-points li {
        margin-bottom: 8px;
    }
    .youtube-input {
        margin-top: 20px;
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("🎙️ Audio to Text Transcription")

    # Tabs para elegir el método de entrada
    tab1, tab2 = st.tabs(["📁 Subir Archivo", "🎥 Video de YouTube"])

    with tab1:
        # File upload
        uploaded_file = st.file_uploader(
            "Upload your audio file",
            type=get_supported_formats(),
            help="Upload an audio file to transcribe"
        )
        process_audio(uploaded_file)

    with tab2:
        # YouTube URL input
        st.markdown("<div class='youtube-input'>", unsafe_allow_html=True)
        youtube_url = st.text_input(
            "Ingresa el URL del video de YouTube",
            placeholder="https://www.youtube.com/watch?v=..."
        )

        if youtube_url:
            try:
                with st.spinner("Descargando audio del video..."):
                    audio_path, video_title = download_youtube_audio(youtube_url)
                    st.success(f"Video descargado: {video_title}")
                    process_audio(audio_path, is_temp_file=True, title=video_title)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        st.markdown("</div>", unsafe_allow_html=True)

def process_audio(input_file, is_temp_file=False, title=None):
    if input_file is not None:
        try:
            # Inicializar transcriptor
            transcriber = AudioTranscriber()

            # Barra de progreso
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Si es un archivo subido, crear archivo temporal
            if not is_temp_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(input_file.name)[1]) as tmp_file:
                    tmp_file.write(input_file.getvalue())
                    audio_path = tmp_file.name
            else:
                audio_path = input_file

            # Procesar transcripción
            status_text.text("Processing audio file...")
            progress_bar.progress(25)

            transcription = transcriber.transcribe(audio_path)
            progress_bar.progress(75)

            progress_bar.progress(100)
            status_text.text("Processing completed!")

            # Modal con la transcripción
            with st.expander("📝 View Transcription", expanded=True):
                st.markdown("<div class='transcription-container'>", unsafe_allow_html=True)

                # Información del archivo
                col1, col2 = st.columns([3, 1])
                with col1:
                    display_name = title if title else (input_file.name if not is_temp_file else "YouTube Audio")
                    st.markdown(f"**File:** {display_name}")
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

            # Botón para generar resumen al final de la transcripción
            if st.button("🤖 Generate AI Summary"):
                status_text.text("Generating summary...")
                summary_json = generate_summary(transcription)

                try:
                    summary_data = json.loads(summary_json)

                    # Mostrar el resumen en un nuevo expander
                    with st.expander("📋 AI Summary", expanded=True):
                        st.markdown("<div class='summary-container'>", unsafe_allow_html=True)

                        st.subheader("🔍 Summary")
                        summary_text = f"""RESUMEN DE LA TRANSCRIPCIÓN

🔍 RESUMEN:
{summary_data['resumen']}

📌 PUNTOS CLAVE:
"""
                        for i, punto in enumerate(summary_data['puntos_clave'], 1):
                            summary_text += f"{i}. {punto}\n"

                        st.write(summary_text)

                        st.subheader("📌 Key Points")
                        st.markdown("<ul class='key-points'>", unsafe_allow_html=True)
                        for punto in summary_data['puntos_clave']:
                            st.markdown(f"<li>{punto}</li>", unsafe_allow_html=True)
                        st.markdown("</ul>", unsafe_allow_html=True)

                        # Botón para descargar el resumen
                        st.download_button(
                            label="📥 Download Summary",
                            data=summary_text,
                            file_name="summary.txt",
                            mime="text/plain"
                        )

                        st.markdown("</div>", unsafe_allow_html=True)
                except json.JSONDecodeError:
                    st.error("Error processing the summary response. Please try again.")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

        finally:
            # Limpiar archivo temporal
            if not is_temp_file and 'audio_path' in locals():
                os.unlink(audio_path)
            elif is_temp_file and os.path.exists(input_file):
                os.unlink(input_file)

if __name__ == "__main__":
    main()