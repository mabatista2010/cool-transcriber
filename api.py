import os
import tempfile
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from audio_processor import AudioTranscriber
from utils import format_transcription, generate_summary, get_supported_formats

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Audio Transcription API",
    description="API para transcripción de audio usando IA",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

# Configurar CORS con opciones más específicas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://0.0.0.0:5000"],  # Streamlit server
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Agregamos GET para la documentación
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Audio Transcription API - Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    return get_openapi(
        title="Audio Transcription API",
        version="1.0.0",
        description="API para transcripción de audio usando IA",
        routes=app.routes,
    )

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint para procesar archivos de audio y generar transcripciones.

    Parameters:
    - file: Archivo de audio a transcribir (mp3, mp4, mpeg, mpga, m4a, wav, webm)

    Returns:
    - success: bool - Indica si la operación fue exitosa
    - filename: str - Nombre del archivo procesado
    - transcription: str - Texto transcrito y formateado
    - summary: dict - Resumen del contenido con puntos clave
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
        if 'tmp' in locals() and os.path.exists(tmp.name):
            os.unlink(tmp.name)
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando el archivo: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando servidor FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")