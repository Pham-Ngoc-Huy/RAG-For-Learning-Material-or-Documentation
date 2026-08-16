import os
import json
from config.config_loader import OmegaConfigLoader
from src.vectordb import QdrantVectorStore
from src.retrieval import QdrantRetriever
from src.ingestion import FileLoader
from src.chunking import MarkDownChunker
from src.embeddings import ModelEmbedder
from src.prompts import PromptAssistance
from src.llm import ThinkingFromKnowledgeBase
from abc import ABC, abstractmethod
# Input Era:

model_chosen=input()
class ConstructorLoops(ABC):
    def __init__(
        self,
        config,
        user_id,
        user_name,
        model
    ):
        self.config=config
        self.user_id=user_id
        self.user_name=user_name
        self.model=model
        self.vectordb="qdrant"

        self.api_key_model=self.config['models'][self.model]['api_key']

        self.embedded_base_url=self.config['models'][self.model]['embedded']['base_url']
        self.embedded_model=self.config['models'][self.model]['embedded']['model']
        
        self.model_llm_client=self.config['models'][self.model]['llm_client']['model']
        self.base_url_llm_client=self.config['models'][self.model]['llm_client']['base_url']

        self.embedded=ModelEmbedder(
            model=self.embedded_model,
            base_url=self.embedded_base_url,
            api_key=self.api_key_model
        )
        self.dimensions=self.embedded._dimensions

        self.prompt_template = PromptAssistance()
        self.vector_store=QdrantVectorStore(
            api_key=self.config["vectordb"][self.vectordb]["api_key"],
            endpoint=self.config["vectordb"][self.vectordb]["endpoint"]
        )
        self.retriever = QdrantRetriever(
            vector_store=self.vector_store,
            embedder=self.embedded
        )
        self.llm_client=ThinkingFromKnowledgeBase(
            api_key=self.api_key_model,
            base_url=self.base_url_llm_client,
            model=self.model_llm_client,
            provider=self.model
        )
    @abstractmethod 
    def query(self, text:str):
        pass 

class AskAndAnswer(ConstructorLoops):
    def query(self, text):
        retrieved_chunks = self.retriever.retrieve(
            user_id=self.user_id,
            query=text,
            top_k=5
        )
        formatted_prompt = self.prompt_template.build(
            template_name="rag_assistance"
            # retrieve chunks
        )

        messages = {"role": self.user_name, "content": formatted_prompt}

        response=self.llm_client.generate(
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        return response
        
def main():

    # load config
    config = OmegaConfigLoader(
        config_path="config/config.yml",
        vectordb={
            "qdrant.endpoint": os.getenv("QDRANT_ENDPOINT"),
            "qdrant.api_key": os.getenv("QDRANT_API_KEY")
        },
        models={
            f"{model_chosen}.api_key": os.getenv(f"{model_chosen.upper()}_API_KEY")
            f"{model_chosen}.llm_client.max_tokens": 500
            f"{model_chosen}.llm_client.temperature": 0.7
        }
    )
    user_id = '1'
    user_name = 'Huy'
    model = 'deepseek'
    query = "Hello !"
    response=AskAndAnswer(
        config=config,
        user_id=user_id,
        user_name=user_name,
        model=model
    ).build(query=query)