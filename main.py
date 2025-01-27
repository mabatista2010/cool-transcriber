import streamlit as st
import os
import tempfile
import json
from audio_processor import AudioTranscriber
from youtube_processor import YouTubeProcessor
from utils import get_supported_formats, format_transcription, generate_summary

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
    .video-info {
        background-color: #fff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .video-thumbnail {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

def process_transcription(audio_path, progress_bar, status_text):
    """Procesar la transcripción de un archivo de audio."""
    try:
        transcriber = AudioTranscriber()
        status_text.text("Processing audio file...")
        progress_bar.progress(25)

        transcription = transcriber.transcribe(audio_path)
        progress_bar.progress(75)

        progress_bar.progress(100)
        status_text.text("Processing completed!")

        return transcription
    except Exception as e:
        raise Exception(f"Error processing transcription: {str(e)}")

def show_transcription_ui(transcription, file_name):
    """Mostrar la interfaz de transcripción."""
    with st.expander("📝 View Transcription", expanded=True):
        st.markdown("<div class='transcription-container'>", unsafe_allow_html=True)

        # Información del archivo
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**File:** {file_name}")
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

def show_summary_ui(transcription, status_text):
    """Mostrar la interfaz del resumen."""
    if st.button("🤖 Generate AI Summary"):
        status_text.text("Generating summary...")
        summary_json = generate_summary(transcription)

        try:
            summary_data = json.loads(summary_json)
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

                st.download_button(
                    label="📥 Download Summary",
                    data=summary_text,
                    file_name="summary.txt",
                    mime="text/plain"
                )

                st.markdown("</div>", unsafe_allow_html=True)
        except json.JSONDecodeError:
            st.error("Error processing the summary response. Please try again.")

def process_file_upload():
    """Procesar la carga de archivos de audio."""
    uploaded_file = st.file_uploader(
        "Upload your audio file",
        type=get_supported_formats(),
        help="Upload an audio file to transcribe"
    )

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            audio_path = tmp_file.name

        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            transcription = process_transcription(audio_path, progress_bar, status_text)
            show_transcription_ui(transcription, uploaded_file.name)
            show_summary_ui(transcription, status_text)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

        finally:
            os.unlink(audio_path)

def process_youtube_url():
    """Procesar URL de YouTube."""
    youtube_url = st.text_input("🎥 Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    
    if youtube_url:
        try:
            yt_processor = YouTubeProcessor()
            
            # Obtener información del video
            with st.spinner("Loading video information..."):
                video_info = yt_processor.get_video_info(youtube_url)
            
            # Mostrar información del video
            st.markdown("<div class='video-info'>", unsafe_allow_html=True)
            
            # Thumbnail y título
            st.image(video_info['thumbnail'], use_column_width=True)
            st.title(video_info['title'])
            
            # Información adicional
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Canal:** {video_info['channel']}")
                st.markdown(f"**Duración:** {yt_processor.format_duration(video_info['duration'])}")
            with col2:
                st.markdown(f"**Vistas:** {video_info['views']:,}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Botón para transcribir
            if st.button("🎙️ Transcribe Video"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with st.spinner("Downloading audio..."):
                    audio_path = yt_processor.download_audio(youtube_url)
                    if audio_path:
                        try:
                            transcription = process_transcription(audio_path, progress_bar, status_text)
                            show_transcription_ui(transcription, video_info['title'])
                            show_summary_ui(transcription, status_text)
                        finally:
                            if os.path.exists(audio_path):
                                os.unlink(audio_path)
                    else:
                        st.error("Error downloading audio from YouTube")
                        
        except Exception as e:
            st.error(f"Error processing YouTube video: {str(e)}")

def main():
    st.title("🎙️ Audio to Text Transcription")
    
    # Crear pestañas
    tab1, tab2 = st.tabs(["📁 Upload Audio", "🎥 YouTube"])
    
    # Pestaña de carga de archivos
    with tab1:
        process_file_upload()
    
    # Pestaña de YouTube
    with tab2:
        process_youtube_url()

if __name__ == "__main__":
    main()