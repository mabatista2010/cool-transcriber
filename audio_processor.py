import speech_recognition as sr
from pydub import AudioSegment
import os

class AudioTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def transcribe(self, audio_path):
        """
        Transcribe audio file to text.
        """
        # Convert audio to wav format if needed
        file_ext = os.path.splitext(audio_path)[1].lower()
        if file_ext != '.wav':
            audio = AudioSegment.from_file(audio_path)
            wav_path = audio_path + '.wav'
            audio.export(wav_path, format='wav')
            audio_path = wav_path
        
        # Perform transcription
        with sr.AudioFile(audio_path) as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source)
            # Record audio data
            audio_data = self.recognizer.record(source)
            
            # Attempt transcription
            try:
                text = self.recognizer.recognize_google(audio_data)
                return text
            except sr.UnknownValueError:
                raise Exception("Speech recognition could not understand the audio")
            except sr.RequestError as e:
                raise Exception(f"Could not request results from speech recognition service: {str(e)}")
            finally:
                # Clean up temporary wav file if created
                if file_ext != '.wav' and os.path.exists(wav_path):
                    os.unlink(wav_path)
