import streamlit as st
import os
import tempfile
import json
from audio_processor import AudioTranscriber
from utils import get_supported_formats, format_transcription, generate_summary

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
    .new-transcription-button {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

def clear_state():
    """Clear all session state variables"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def main():
    st.title("🎙️ Audio to Text Transcription")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload your audio file",
        type=get_supported_formats(),
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
            progress_bar.progress(75)

            progress_bar.progress(100)
            status_text.text("Processing completed!")

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

            # Botón para generar resumen al final de la transcripción
            if st.button("🤖 Generate AI Summary"):
                status_text.text("Generating summary...")
                summary_json = generate_summary(transcription)

                try:
                    summary_data = json.loads(summary_json)

                    # Guardar el resumen en el estado de la sesión
                    st.session_state.summary_data = summary_data
                    st.session_state.summary_text = f"""RESUMEN DE LA TRANSCRIPCIÓN

🔍 RESUMEN:
{summary_data['resumen']}

📌 PUNTOS CLAVE:
"""
                    for i, punto in enumerate(summary_data['puntos_clave'], 1):
                        st.session_state.summary_text += f"{i}. {punto}\n"

                except json.JSONDecodeError:
                    st.error("Error processing the summary response. Please try again.")

            # Mostrar el resumen si existe en el estado de la sesión
            if 'summary_data' in st.session_state:
                with st.expander("📋 AI Summary", expanded=True):
                    st.markdown("<div class='summary-container'>", unsafe_allow_html=True)

                    st.subheader("🔍 Summary")
                    st.write(st.session_state.summary_text)

                    st.subheader("📌 Key Points")
                    st.markdown("<ul class='key-points'>", unsafe_allow_html=True)
                    for punto in st.session_state.summary_data['puntos_clave']:
                        st.markdown(f"<li>{punto}</li>", unsafe_allow_html=True)
                    st.markdown("</ul>", unsafe_allow_html=True)

                    # Botón para descargar el resumen
                    st.download_button(
                        label="📥 Download Summary",
                        data=st.session_state.summary_text,
                        file_name="summary.txt",
                        mime="text/plain"
                    )

                    st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

        finally:
            # Limpiar archivo temporal
            os.unlink(audio_path)

    # Botón para nueva transcripción centrado
    st.markdown("<div class='new-transcription-button'>", unsafe_allow_html=True)
    if st.button("🔁 Nueva transcripción", use_container_width=False):
        clear_state()
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()