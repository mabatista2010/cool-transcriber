# Audio Transcriber

Aplicación web para transcribir audio a texto y generar resúmenes usando IA.

## Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Clave API de OpenAI (para la funcionalidad de resumen)

## Instalación

1. Clonar el repositorio:
```bash
git clone <tu-repositorio>
cd AudioTranscriber
```

2. Crear un entorno virtual:
```bash
python -m venv venv
```

3. Activar el entorno virtual:
- En macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- En Windows:
  ```bash
  .\venv\Scripts\activate
  ```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración

1. Crear un archivo `.env` en la raíz del proyecto
2. Agregar tu clave API de OpenAI:
```
OPENAI_API_KEY=tu-clave-api
```

## Uso

1. Ejecutar la aplicación:
```bash
streamlit run main.py
```

2. Abrir el navegador en:
```
http://localhost:8501
```

## Funcionalidades

- Transcripción de archivos de audio a texto
- Generación de resúmenes usando IA
- Descarga de transcripciones y resúmenes
- Interfaz web responsive y PWA 