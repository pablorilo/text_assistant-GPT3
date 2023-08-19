from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo ".env"
load_dotenv()

class Config:
    # Obtiene el nombre del modelo desde la variable de entorno "MODEL_NAME"
    model_name = os.environ.get('MODEL_NAME')
    # Obtiene la clave de la API desde la variable de entorno "API_KEY"
    api_key = os.environ.get('API_KEY')
    # Obtiene la ruta de los documentos desde la variable de entorno "DOCS_PATH"
    docs_path = os.environ.get('DOCS_PATH')

    @classmethod
    def validate_config(cls):
        """
        Valida que las variables de entorno esenciales estén configuradas correctamente.
        Lanza una excepción si alguna variable esencial está ausente o configurada incorrectamente.
        """
        if not cls.model_name:
            raise ValueError("MODEL_NAME no está configurado en las variables de entorno.")
        if not cls.api_key:
            raise ValueError("API_KEY no está configurado en las variables de entorno.")
        if not cls.docs_path:
            raise ValueError("DOCS_PATH no está configurado en las variables de entorno.")