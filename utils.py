def get_supported_formats():
    """
    Return list of supported audio formats by OpenAI Whisper.
    """
    return ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']

def format_transcription(text):
    """
    Format transcribed text for display.
    """
    # Add proper spacing and formatting
    paragraphs = text.split('. ')
    formatted_text = ''

    for paragraph in paragraphs:
        if paragraph:
            # Clean up the paragraph and add proper punctuation
            cleaned = paragraph.strip()
            if not cleaned.endswith('.'):
                cleaned += '.'
            formatted_text += f"{cleaned}\n\n"

    return formatted_text