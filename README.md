# Text Assistant

### Chat Bot de Manejo de Archivos de Texto y PDF! Este chat bot está diseñado para interactuar contigo y responder preguntas relacionadas con los archivos de texto y PDF alojados en tu computadora. Puedes realizar consultas y obtener información sobre los documentos almacenados en tu sistema.

## Funcionalidades

- **Consulta de Documentos:** El chat bot puede responder a preguntas sobre documentos de texto y PDF presentes en la ubicación especificada.
- **Elegir idioma de respuesta:** Al iniciar el chat se configura el lenguaje de respuesta.

## Diseño de carpetas
<pre>
text_assistant-GPT3/
    ├── src/
    │   ├── utils/
    │   └── process/
    ├── Config
    ├── Main
    ├── README.md
    ├── requirements.txt
    ├── setup.py
</pre>

   - **utils**: Fichero que contiene diferentes métodos de la app
   - **process**: Fichero que realizar el embedding de los datos
   - **config**: Fichero con la configuración de las variables de entorno
   - **main**: Punto de entrada principal para el programa
   - **README.md**: Este archivo es la documentación principal de tu proyecto.
   - **requirements.txt**: Este archivo enumera las dependencias (bibliotecas y paquetes) necesarias para ejecutar tu proyecto.
   - **setup.py**: Contiene información sobre el programa   

## Configuración

1. Clona este repositorio en tu máquina local.
    ```
    git clone https://github.com/pablorilo/text_assistant-GPT3.git
    ```

2. Instala las dependencias necesarias ejecutando el siguiente comando en tu terminal:

    En windowns:

    ``` 
    pip install -r requirements.txt
    ```
3. Crea un archivo `.env` en la raíz del proyecto y configura las variables de entorno necesarias:
<pre>
    MODEL_NAME=nombre_del_modelo_gpt3
    API_KEY=tu_clave_de_api_de_openai
    DOCS_PATH=ruta_a_tus_documentos      
</pre>

## Uso

1. Abre una terminal y navega hasta el directorio del proyecto.
2. Ejecuta el siguiente comando para iniciar el chat bot:
    ```
    python main.py    
    ```
3. Sigue las instrucciones en la pantalla para interactuar con el chat bot. Puedes hacer preguntas sobre archivos de texto y PDF, cambiar el idioma de las respuestas y más.
