import os
from openai import OpenAI
from pytube import YouTube
import tempfile

def get_supported_formats():
    """
    Return list of supported audio formats by OpenAI Whisper.
    """
    return ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']

def download_youtube_audio(url):
    """
    Download audio from YouTube video.
    Returns the path to the downloaded audio file.
    """
    try:
        # Validar el formato de la URL
        if not url.startswith('http'):
            raise Exception("URL inválida. Debe comenzar con http:// o https://")

        # Crear directorio temporal si no existe
        temp_dir = tempfile.gettempdir()

        print(f"Intentando descargar video de: {url}")  # Debug info

        # Intentar crear objeto YouTube con más opciones
        yt = YouTube(
            url,
            use_oauth=False,
            allow_oauth_cache=True
        )

        print(f"Título del video: {yt.title}")  # Debug info
        print(f"Duración: {yt.length} segundos")  # Debug info

        # Obtener el stream de audio
        print("Buscando stream de audio...")  # Debug info
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        if not audio_stream:
            raise Exception("No se encontró un stream de audio compatible")

        print(f"Stream seleccionado: {audio_stream}")  # Debug info

        # Generar nombre único para el archivo temporal
        temp_file = os.path.join(temp_dir, f"yt_audio_{os.urandom(4).hex()}.mp4")

        print(f"Descargando audio a: {temp_file}")  # Debug info
        # Descargar el audio
        audio_stream.download(filename=temp_file)

        if not os.path.exists(temp_file):
            raise Exception("El archivo no se descargó correctamente")

        print("Descarga completada exitosamente")  # Debug info
        return temp_file, yt.title

    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
            raise Exception(
                "Error 403: YouTube está bloqueando la descarga. "
                "Esto puede deberse a restricciones del video o límites de rate. "
                "Por favor, intenta con otro video o espera unos minutos."
            )
        elif "Video unavailable" in error_msg:
            raise Exception(
                "El video no está disponible. "
                "Verifica que el video exista y sea público."
            )
        else:
            raise Exception(f"Error descargando audio de YouTube: {error_msg}")

def generate_summary(text):
    """
    Generate a summary of the transcribed text using OpenAI's GPT model.
    Returns both a short summary and key points.
    """
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                    "role": "system",
                    "content": "Analiza el siguiente texto transcrito y proporciona:"
                    "\n1. Un resumen conciso (máximo 3 párrafos)"
                    "\n2. Los puntos clave más importantes (máximo 5 puntos)"
                    "\nResponde en formato JSON con las claves 'resumen' y 'puntos_clave'"
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        return {"error": f"Error generando el resumen: {str(e)}"}

def format_transcription(text):
    """
    Format transcribed text using OpenAI for better presentation and speaker detection.
    """
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {
                    "role": "system",
                    "content": "Analiza el siguiente texto transcrito. Primero, determina si hay evidencia clara "
                    "de múltiples personas hablando (por ejemplo, diálogo, diferentes puntos de vista o estilos de habla). "
                    "Si y SOLO SI detectas múltiples hablantes con certeza, etiqueta cada intervención con 'Persona 1:', "
                    "'Persona 2:', etc. Si no hay evidencia clara de múltiples hablantes, simplemente mejora el formato "
                    "y la legibilidad del texto sin agregar etiquetas. Mantén el contenido exactamente igual."
                },
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=5000
        )

        formatted_text = response.choices[0].message.content
        return formatted_text

    except Exception as e:
        # Si hay un error con OpenAI, retorna el texto original con formato básico
        paragraphs = text.split('. ')
        formatted_text = ''

        for paragraph in paragraphs:
            if paragraph:
                cleaned = paragraph.strip()
                if not cleaned.endswith('.'):
                    cleaned += '.'
                formatted_text += f"{cleaned}\n\n"

        return formatted_text