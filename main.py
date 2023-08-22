import typer
import os
import glob

from src.utils import answer_question_from_file
from rich import print  # pip install rich


from config import Config
from src.process import TextEmbedding
from src.utils import print_welcome_message,answer_question_from_file, __prompt, get_language_choice

def main():
  """
    Función principal para la ejecución del programa.
  """
  # Validamos la configuración de las variables de entorno
  Config.validate_config()
  # Cargar datos de documentos desde el directorio especificado
  archivos_pdf = glob.glob(os.path.join(Config.docs_path, "*.pdf"))
  #Creamos instancia de la clase que se encarga del embedding
  text_processor = TextEmbedding()
  #Procesar los documentos y construir un índice de texto
  agent = text_processor.process_text(archivos_pdf)

  #LLmamaos al metodo que genera la bienvenida a la interface
  print_welcome_message()
   # Obtener la selección de idioma del usuario
  lng_prompt = get_language_choice()
  answer_question_from_file(agent, lng_prompt)
  print("[bold cornflower_blue]En qué puedo ayudarte?")

  while True:     
    question = __prompt()
    if question == 'lng':
       # Cambiar el idioma si el usuario lo solicita
       lng_prompt = get_language_choice()
       answer_question_from_file(agent, lng_prompt)
       question = __prompt()
    # Obtener respuesta a la pregunta del archivo utilizando el índice
    response = answer_question_from_file(agent, question)
    # Mostrar la respuesta y la información de las páginas en la interfaz de línea de comandos
    print(f"\n[bold green] Respuesta:[/bold green] [green]{response['output']}[/green]\n")

    
if __name__ == "__main__":
    #Ejecutamos el programa sobre typer
    typer.run(main)