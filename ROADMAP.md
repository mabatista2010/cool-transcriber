# Roadmap: Transcriptor y Traductor de Videos

## 1. Funcionalidad Actual ✅
- Descarga de videos de YouTube
- Extracción de audio
- Transcripción usando OpenAI Whisper
- Sistema de caché para transcripciones
- Interfaz web con Streamlit

## 2. Nueva Funcionalidad: Subtítulos Multilenguaje 🚀

### 2.1 Interfaz de Usuario
- [ ] Añadir selector de idioma para subtítulos
- [ ] Añadir selector de formato (SRT, VTT)
- [ ] Implementar vista previa del video con subtítulos
- [ ] Agregar opciones de personalización de subtítulos

### 2.2 Backend
- [ ] Implementar traducción usando OpenAI
- [ ] Generar timestamps para subtítulos
- [ ] Crear convertidor a formatos SRT/VTT
- [ ] Integrar FFmpeg para manipulación de video

### 2.3 Características de Subtítulos
- [ ] Generación en idioma original
- [ ] Traducción a múltiples idiomas
- [ ] Exportación en diferentes formatos
- [ ] Incrustación en video

### 2.4 Características Adicionales
- [ ] Previsualización en tiempo real
- [ ] Editor de timestamps
- [ ] Descarga de subtítulos por separado
- [ ] Exportación de video con subtítulos

## 3. Mejoras Técnicas Pendientes
- [ ] Optimización de procesamiento de videos largos
- [ ] Mejora del sistema de caché
- [ ] Manejo de errores mejorado
- [ ] Documentación de API

## 4. Flujo de Trabajo
1. Video YouTube → Descarga
2. Video → Extracción de Audio
3. Audio → Transcripción
4. Texto → Traducción
5. Texto Traducido → Generación de Subtítulos
6. Subtítulos → Formato Final (SRT/VTT/Incrustado)

## 5. Tecnologías a Utilizar
- OpenAI API (Whisper + GPT para traducción)
- FFmpeg (manipulación de video)
- yt-dlp (descarga de YouTube)
- Streamlit (interfaz)
- Python (backend)

## 6. Prioridades de Implementación
1. Implementación básica de traducción
2. Generación de subtítulos SRT
3. Selector de idiomas en UI
4. Vista previa de subtítulos
5. Características avanzadas 