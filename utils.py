import openai
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_supported_formats():
    """
    Return list of supported audio formats by OpenAI Whisper.
    """
    return ['wav', 'mp3', 'ogg', 'm4a', 'flac']

def generate_summary(text):
    """
    Generate a summary of the transcribed text using OpenAI's GPT model.
    Returns both a short summary and key points.
    """
    try:
        prompt = f"""Por favor, analiza el siguiente texto y proporciona:
1. Un resumen conciso
2. Los puntos clave más importantes (máximo 5)

Formato de respuesta requerido (JSON):
{{
    "resumen": "El resumen aquí",
    "puntos_clave": [
        "Punto 1",
        "Punto 2",
        etc.
    ]
}}

Texto a analizar:
{text}"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en análisis y resumen de texto."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")

def format_transcription(text):
    """
    Format transcribed text using OpenAI for better presentation and speaker detection.
    """
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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