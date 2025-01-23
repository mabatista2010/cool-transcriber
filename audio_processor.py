import os
from openai import OpenAI

class AudioTranscriber:
    def __init__(self):
        self.client = OpenAI()

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
                return self.format_transcription(response.text)

        except Exception as e:
            if "API key" in str(e):
                raise Exception("Error de API: Verifica tu API key de OpenAI")
            elif "file format" in str(e).lower():
                raise Exception("Formato de archivo no soportado")
            else:
                raise Exception(f"Error durante la transcripción: {str(e)}")

    def format_transcription(self, text):
        """
        Format the transcription using OpenAI to improve readability.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente que formatea texto transcrito. "
                        "NO agregues ni quites información, solo organiza el texto "
                        "con párrafos y puntuación adecuada."
                    },
                    {
                        "role": "user",
                        "content": f"Formatea este texto transcrito manteniendo el contenido exacto:\n\n{text}"
                    }
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return text  # En caso de error, devolver el texto original sin formato