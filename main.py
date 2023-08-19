import typer

from src.utils import answer_question_from_file
from rich import print  # pip install rich
from llama_index import  SimpleDirectoryReader

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
  docs = SimpleDirectoryReader(Config.docs_path).load_data()
  #Creamos instancia de la clase que se encarga del embedding
  text_processor = TextEmbedding()
  #Procesar los documentos y construir un índice de texto
  index = text_processor.process_text(docs)
  #LLmamaos al metodo que genera la bienvenida a la interface
  print_welcome_message()
   # Obtener la selección de idioma del usuario
  lng = get_language_choice()

  while True:     
    question = __prompt()
    if question == 'lng':
       # Cambiar el idioma si el usuario lo solicita
       lng = get_language_choice()
       question = __prompt()
    # Agregar el idioma a la pregunta para el contexto
    question = f'{question}, {lng}'
    # Obtener respuesta a la pregunta del archivo utilizando el índice
    response = answer_question_from_file(index, question)
    answer = response[0]
    document_page = response[1]
    #montamos las referencias sobre las que se creó la respuesta
    file_pages = [f"{filename} -> pág.({', '.join(pages)})" for filename, pages in document_page.items()]
    file_pages_string = ", ".join(file_pages)
    #Añadimos al contexto el diálogo
    text_processor.add_dialog_to_context([question,answer])
    # Mostrar la respuesta y la información de las páginas en la interfaz de línea de comandos
    print(f"\n[bold green] Respuesta:[/bold green] [green]{answer}[/green]\n\n[green] ({file_pages_string})[/green]")

    
if __name__ == "__main__":
    #Ejecutamos el programa sobre typer
    typer.run(main)