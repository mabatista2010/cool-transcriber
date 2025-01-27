from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

class Translator:
    def __init__(self):
        self.client = OpenAI()
        self.available_languages = {
            'es': 'español',
            'en': 'inglés',
            'fr': 'francés',
            'de': 'alemán',
            'it': 'italiano',
            'pt': 'portugués',
            'zh': 'chino',
            'ja': 'japonés',
            'ko': 'coreano',
            'ru': 'ruso'
        }

    def translate_text(self, text, target_language):
        """
        Traduce el texto al idioma especificado usando GPT.
        
        Args:
            text (str): Texto a traducir
            target_language (str): Código del idioma objetivo (ej: 'en', 'es', 'fr')
            
        Returns:
            str: Texto traducido
        """
        try:
            if target_language not in self.available_languages:
                raise ValueError(f"Idioma no soportado. Idiomas disponibles: {', '.join(self.available_languages.values())}")

            # Crear el prompt para la traducción
            prompt = f"Traduce el siguiente texto al {self.available_languages[target_language]}. Mantén el mismo tono y estilo:\n\n{text}"

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un traductor profesional experto."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3  # Menor temperatura para traducciones más precisas
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"Error durante la traducción: {str(e)}")

    def get_available_languages(self):
        """
        Retorna un diccionario con los idiomas disponibles
        """
        return self.available_languages 