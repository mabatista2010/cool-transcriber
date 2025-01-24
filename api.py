import os
import tempfile
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from audio_processor import AudioTranscriber
from utils import format_transcription, generate_summary, get_supported_formats

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Audio Transcription API")

# Configurar CORS con opciones más específicas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://0.0.0.0:5000"],  # Streamlit server
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint para procesar archivos de audio y generar transcripciones.
    """
    logger.info(f"Recibiendo archivo: {file.filename}")

    # Verificar formato del archivo
    file_extension = os.path.splitext(file.filename)[1].lower().replace('.', '')
    if file_extension not in get_supported_formats():
        raise HTTPException(
            status_code=400,
            detail=f"Formato no soportado. Formatos permitidos: {', '.join(get_supported_formats())}"
        )

    try:
        # Crear un archivo temporal para guardar el audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp:
            logger.info(f"Creando archivo temporal: {tmp.name}")
            content = await file.read()
            tmp.write(content)
            tmp.flush()

            # Procesar el archivo
            transcriber = AudioTranscriber()
            logger.info("Iniciando transcripción...")
            transcription = transcriber.transcribe(tmp.name)

            # Formatear la transcripción
            logger.info("Formateando transcripción...")
            formatted_text = format_transcription(transcription)

            # Generar resumen
            logger.info("Generando resumen...")
            summary = generate_summary(transcription)

            # Limpiar el archivo temporal
            logger.info("Limpiando archivo temporal...")
            os.unlink(tmp.name)

            return JSONResponse(
                content={
                    "success": True,
                    "filename": file.filename,
                    "transcription": formatted_text,
                    "summary": summary
                },
                status_code=200
            )

    except Exception as e:
        logger.error(f"Error procesando archivo: {str(e)}")
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando el archivo: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando servidor FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")