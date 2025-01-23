import os
from openai import OpenAI

def get_supported_formats():
    """
    Return list of supported audio formats by OpenAI Whisper.
    """
    return ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']

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
                    "content": "Analiza el siguiente texto transcrito e identifica cuando hablan diferentes personas. "
                    "Etiqueta cada intervención con 'Persona 1:', 'Persona 2:', etc., basándote en cambios en el "
                    "hablante. Mantén el contenido exactamente igual, solo agrega las etiquetas de los hablantes "
                    "y mejora el formato para mayor legibilidad. Si no hay cambios claros de hablante, no agregues etiquetas."
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