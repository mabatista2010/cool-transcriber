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
        # Crear directorio temporal si no existe
        temp_dir = tempfile.gettempdir()

        # Descargar audio
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Descargar en archivo temporal
        temp_file = os.path.join(temp_dir, f"yt_audio_{os.urandom(4).hex()}.mp4")
        audio_stream.download(filename=temp_file)

        return temp_file, yt.title

    except Exception as e:
        raise Exception(f"Error descargando audio de YouTube: {str(e)}")

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