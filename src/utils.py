import typer  # pip install "typer[all]"
from rich import print  # pip install rich
from rich.table import Table
from rich.prompt import Prompt, Confirm

from langchain import PromptTemplate
from langchain.agents.agent import AgentExecutor
import typer  
import click
from config import Config


def print_welcome_message() -> None:
    """función que genera el texto inicial del programa """
    title = ">>>>>>>>>>>>>>>>>> 💬 Text Assistant 💬 <<<<<<<<<<<<<<<<<<"
    centered_title = title.center(150)
    print(f"[bold blue_violet] {centered_title} [/bold blue_violet]\n")
    print("[blue_violet]Bienvenido al sistema de asistencia documental impulsado por el poder de OpenAI's GPT-3.5 Turbo.\
Esto significa que puedes cargar tus documentos, extraer información esencial y realizar consultas inteligentes, todo en un solo lugar.\
Este sistema te permitirá buscar y analizar documentos. Ingresa tus preguntas y obtén respuestas informadas y precisas además de las páginas\
y nombres de los documentos que se ha utilizado para generar la respuesta, esta información aparecerá entre paréntesis al final de la respuesta.\n\nTabla de comandos:\n")

    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la aplicación")  
    table.add_row("lng", "Cambiar idioma de respuesta")   
    print(table)    

def get_language_choice() -> str:
    """función que imprime en pantalla las opciones de idioma (Español, Aleman, Inglés)
    Returns:
         str: texto que se enviará al prompt""" 
    lng_options = Config.lng_dict
    template = '''Quiero que a partir de ahora respondas en {choice} y en relación al contexto pasado'''
    promp_temp = PromptTemplate(
                                template= template,
                                input_variables = ["choice"]
                                )
    while True:
        #Creamos las opciones
        click_choice = click.Choice(lng_options.keys())
        #Solicitamos al usuario que seleccione un idioma
        print("\n🌍 ¿En qué idioma deseas la respuesta?:\n")
        #Gneramos las opciones en base al lng_dict
        opt = "\n".join([f"{key} - {value}" for key, value in lng_options.items()])
        opt += "\n\nOpciones"
        choice = typer.prompt(opt,
                              show_choices=True,
                              type=click_choice
                              )
        #retornamos opción                
        if choice in lng_options.keys():
            print(f"[cornflower_blue]\nIdioma seleccionado: {lng_options[choice]}\n")
            prompt_value = promp_temp.format(choice=lng_options[choice])
            return prompt_value
        else:
            typer.echo(f"Por favor, ingresa una opción válida {lng_options.keys()}.")    

def __prompt() -> str:
    """
    Solicita una pregunta al usuario y gestiona la opción de salida.
    Returns:
        str: La pregunta ingresada por el usuario.
    """
    # Solicitar una pregunta al usuario utilizando la librería Prompt de rich
    prompt = Prompt.ask("\n[bold cornflower_blue] Pregunta ")

    # Verificar si el usuario quiere salir
    if prompt == "exit":
        exit = Confirm.ask("✋ ¿Estás seguro de que quieres salir?")
        if exit:
            print("👋 ¡Hasta pronto!")
            raise typer.Abort() # Terminar la ejecución del programa
        return __prompt()
    return prompt   

def extract_pages_by_filename(document_dict: dict) -> dict:
    """
    Extrae las etiquetas de página de un diccionario de documentos y las organiza por nombre de archivo.
    La información incluye el 'file_name' (nombre del archivo del documento) y 'page_label' (etiqueta de la página del documento).
    Args:
        document_dict (dict): Un diccionario que contiene información de los documentos.

    Returns:
        dict: Un diccionario donde los nombres de archivo son claves y las etiquetas de página asociadas se almacenan en listas.
    """
    # Inicializa un diccionario vacío para almacenar etiquetas de página por nombre de archivo
    pages_by_file = {}
    # Itera a través de cada entrada de documento en el diccionario de entrada
    for doc_id, info in document_dict.items():
        if 'file_name' not in info:
            continue  
        filename = info['file_name']
        if 'page_label'not in info:
            info['page_label'] = "1"
        page_label = info['page_label']
        if filename not in pages_by_file:
            pages_by_file[filename] = []
        #Almacenamos el nombre del documento y las páginas
        pages_by_file[filename].append(page_label)

    return pages_by_file   

def answer_question_from_file(agent: AgentExecutor, question:str) :    
        """
    Responde a una pregunta utilizando un índice vectorial y un motor de consultas.
    Args:
        agent (AgentExecutor): Instancia de AgentExecutor.
        question (str): La pregunta para la cual se busca una respuesta.
    Returns:
        str: La respuesta encontrada a la pregunta.
    """
        result = agent({"input": question})
                       
        return result
        





