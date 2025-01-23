import os
from openai import OpenAI

class AudioTranscriber:
    def __init__(self):
        self.client = OpenAI()

    def transcribe(self, audio_path):
        """
        Transcribe audio file to text using OpenAI Whisper API.
        """
        try:
            with open(audio_path, "rb") as audio_file:
                # Use Whisper API to transcribe
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="es",
                    response_format="text"
                )
                return response

        except Exception as e:
            if "API key" in str(e):
                raise Exception("Error de API: Verifica tu API key de OpenAI")
            elif "file format" in str(e).lower():
                raise Exception("Formato de archivo no soportado")
            else:
                raise Exception(f"Error durante la transcripción: {str(e)}")