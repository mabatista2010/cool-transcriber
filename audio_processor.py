import os
from openai import OpenAI
from pytube import YouTube
import tempfile

class AudioTranscriber:
    def __init__(self):
        self.client = OpenAI()

    def download_youtube_audio(self, url):
        """
        Download audio from YouTube video.
        Returns the path to the downloaded audio file.
        """
        try:
            # Create YouTube object
            yt = YouTube(url)
            # Get audio stream
            audio_stream = yt.streams.filter(only_audio=True).first()

            # Create temporary file
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, "audio.mp4")

            # Download audio
            audio_stream.download(output_path=temp_dir, filename="audio.mp4")
            return temp_path

        except Exception as e:
            raise Exception(f"Error al descargar el audio de YouTube: {str(e)}")

    def transcribe(self, input_path, is_youtube_url=False):
        """
        Transcribe audio file to text using OpenAI Whisper API.
        Auto-detects the language of the audio.
        """
        try:
            # If input is YouTube URL, download audio first
            audio_path = self.download_youtube_audio(input_path) if is_youtube_url else input_path

            with open(audio_path, "rb") as audio_file:
                # Use Whisper API to transcribe with auto language detection
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )

                # Clean up downloaded YouTube audio if necessary
                if is_youtube_url and os.path.exists(audio_path):
                    os.unlink(audio_path)
                    os.rmdir(os.path.dirname(audio_path))

                return response

        except Exception as e:
            if "API key" in str(e):
                raise Exception("Error de API: Verifica tu API key de OpenAI")
            elif "file format" in str(e).lower():
                raise Exception("Formato de archivo no soportado")
            else:
                raise Exception(f"Error durante la transcripción: {str(e)}")