import os
from openai import OpenAI

class AudioTranscriber:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Error: No se encontró la API key de OpenAI")
        self.client = OpenAI(api_key=api_key)

    def transcribe(self, audio_path):
        """
        Transcribe audio file to text using OpenAI Whisper API.
        Auto-detects the language of the audio.
        """
        try:
            with open(audio_path, "rb") as audio_file:
                # Use Whisper API to transcribe with auto language detection
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
                return response

        except Exception as e:
            if "API key" in str(e):
                raise ValueError("Error de API: Verifica tu API key de OpenAI")
            elif "file format" in str(e).lower():
                raise ValueError("Formato de archivo no soportado")
            else:
                raise ValueError(f"Error durante la transcripción: {str(e)}")