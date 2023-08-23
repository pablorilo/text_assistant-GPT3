from llama_index import VectorStoreIndex, LLMPredictor, ServiceContext
from llama_index import OpenAIEmbedding, Document
from langchain.chat_models import ChatOpenAI
from config import Config
from cachetools import TTLCache
import openai
from config import Config

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
        Inicializa la clase y configura las instancias necesarias.
        """
        openai.api_key = Config.api_key
        #Creamos instancia de ChatOpenai a traves de langchain
        """chat_openai = ChatOpenAI(temperature=0, 
                                 model_name = Config.model_name, 
                                 openai_api_key= Config.api_key)
        #Instanciamos el modelo
        llm_predictor = LLMPredictor(llm=chat_openai) 
        #Indexamos el contenido de los PDF´s
        self.service_context = ServiceContext.from_defaults()"""
        self.cache = TTLCache(maxsize=100, ttl=3600)

    def process_text(self, docs: list) -> VectorStoreIndex:
        """
        Procesa los documentos y construye un índice de texto.
        Args:
            docs (list): Lista de documentos a ser indexados.
        Returns:
            VectorStoreIndex: Índice de texto construido a partir de los documentos.
        """
        # Intenta obtener el índice desde el caché
        self.index = self.cache.get("index")
        if self.index is None: # Si no hay índice en caché, crea un nuevo índice y lo guarda en caché
            self.index= VectorStoreIndex.from_documents(docs, service_context=self.service_context)
            self.cache["index"] = self.index
            self.index_init = self.index
        return self.index
    
    def add_dialog_to_context(self, docs: list) -> None:
        """
        Agrega documentos al contexto de la conversación.
        Args:
            docs (list): Lista de documentos a ser agregados al contexto.
        """
        embed_model = OpenAIEmbedding()
        doc_chunks = []
        for i, text in enumerate(docs):
            embedding = embed_model.get_text_embedding(text)
            doc = Document(text=text, embedding= embedding)
            doc_chunks.append(doc)

        for doc_chunk in doc_chunks:
            self.index.insert(doc_chunk)

    def reinitial_context(self):
        """
        Reinicia el contexto de la conversación al estado inicial.
        """
        self.index = self.index_init