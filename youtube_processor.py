import yt_dlp
import tempfile
import os
from typing import Dict, Optional

class YouTubeProcessor:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    def get_video_info(self, url: str) -> Dict:
        """Obtener información del video de YouTube."""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', ''),
                    'thumbnail': info.get('thumbnail', ''),
                    'duration': info.get('duration', 0),
                    'views': info.get('view_count', 0),
                    'channel': info.get('uploader', '')
                }
        except Exception as e:
            raise Exception(f"Error al obtener información del video: {str(e)}")

    def download_audio(self, url: str) -> Optional[str]:
        """Descargar el audio del video de YouTube."""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')
                
                ydl_opts = {
                    **self.ydl_opts,
                    'outtmpl': output_template,
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    audio_file = os.path.join(temp_dir, f"{info['title']}.mp3")
                    
                    if os.path.exists(audio_file):
                        # Crear un archivo temporal permanente para el audio
                        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                        with open(audio_file, 'rb') as f:
                            temp_audio.write(f.read())
                        return temp_audio.name
                    
            return None
        except Exception as e:
            raise Exception(f"Error al descargar el audio: {str(e)}")

    def format_duration(self, seconds: int) -> str:
        """Formatear la duración del video en formato HH:MM:SS."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}" 