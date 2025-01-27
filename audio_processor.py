import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
load_dotenv()

class AudioTranscriber:
    def __init__(self):
        self.client = OpenAI()
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_path(self, audio_path):
        """Genera una ruta única para el caché basada en el nombre y tamaño del archivo"""
        file_stats = os.stat(audio_path)
        cache_key = f"{Path(audio_path).stem}_{file_stats.st_size}"
        return self.cache_dir / f"{cache_key}.json"

    def get_from_cache(self, audio_path):
        """Intenta obtener la transcripción del caché"""
        cache_path = self.get_cache_path(audio_path)
        if cache_path.exists():
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)['transcription']
        return None

    def save_to_cache(self, audio_path, transcription):
        """Guarda la transcripción en el caché"""
        cache_path = self.get_cache_path(audio_path)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump({'transcription': transcription}, f, ensure_ascii=False)

    def transcribe(self, audio_path):
        """
        Transcribe audio file to text using OpenAI Whisper API.
        Auto-detects the language of the audio.
        """
        try:
            # Primero intentamos obtener del caché
            cached_result = self.get_from_cache(audio_path)
            if cached_result:
                return cached_result

            # Si no está en caché, transcribimos
            with open(audio_path, "rb") as audio_file:
                # Seleccionar modelo según el tamaño del archivo
                file_size = os.path.getsize(audio_path)
                model = "whisper-1"
                if file_size < 1024 * 1024:  # Si es menor a 1MB
                    model = "whisper-1"  # Usar modelo más ligero para archivos pequeños

                response = self.client.audio.transcriptions.create(
                    model=model,
                    file=audio_file,
                    response_format="text"
                )
                
                # Guardar en caché
                self.save_to_cache(audio_path, response)
                return response

        except Exception as e:
            if "API key" in str(e):
                raise Exception("Error de API: Verifica tu API key de OpenAI")
            elif "file format" in str(e).lower():
                raise Exception("Formato de archivo no soportado")
            else:
                raise Exception(f"Error durante la transcripción: {str(e)}")