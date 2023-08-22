from pydantic import BaseModel, Field

from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent,AgentType,Tool
from langchain.agents.agent import AgentExecutor

import openai

from config import Config

class DocumentInput(BaseModel):
    question: str = Field()

class TextEmbedding:
    """
    Clase para el procesamiento de texto y gestión de contextos utilizando GPT-3.
    Esta clase proporciona métodos para el procesamiento de documentos, la construcción
    de índices de texto y la interacción con el modelo GPT-3 para responder preguntas
    y mantener el contexto en una conversación.

    Attributes:
        cache (TTLCache): Caché para almacenar el índice y otros datos en memoria temporal.
        service_context (ServiceContext): Contexto de servicio para el indexado de texto.
    """

    def __init__(self):
        """
        Inicializa la clase y configura la instancia del modelo.
        """
        #Creamos instancia de ChatOpenai a traves de langchain
        
        self.llm = ChatOpenAI(temperature=0, 
                                 model_name = Config.model_name, 
                                 openai_api_key= Config.api_key)     
       
    def process_text(self, docs: list) -> AgentExecutor:
        """
        Procesa los documentos y construye un índice de texto.
        Args:
            docs (list): Lista de rutas de pdf en la carpeta.
        Returns:
            AgentExecutor: Agent que se encargara de la interación con el modelo.
        """
        tools = []
        #itera sobre los documentos de la carpeta y los va vectorizando
        for file in docs:
            loader = PyPDFLoader(file)
            pages = loader.load_and_split()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(pages)
            openai.api_key = Config.api_key
            embeddings = OpenAIEmbeddings(openai_api_key = Config.api_key)
            retriever = FAISS.from_documents(docs, embeddings).as_retriever()

            # Añadimos los retrieves a los tools
            tools.append(
                Tool(
                    args_schema=DocumentInput,
                    name= file.split("\\")[-1][:-4],
                    description=f"texto que formara parte del contexto",
                    func=RetrievalQA.from_chain_type(llm=self.llm, retriever=retriever),
                )
            )
        #Inicializamos el agente
        agent = initialize_agent(
                agent=AgentType.OPENAI_FUNCTIONS,
                tools=tools,
                llm=self.llm,
                )

        return agent
    
