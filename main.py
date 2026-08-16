import os
from dotenv import load_dotenv
from config.config_loader import OmegaConfigLoader
from src.vectordb import QdrantVectorStore
from src.retrieval import QdrantRetriever
from src.ingestion import FileLoader
from src.chunking import MarkDownChunker
from src.embeddings import ModelEmbedder
from src.prompts import PromptAssistance
from src.llm import ThinkingFromKnowledgeBase
from abc import ABC, abstractmethod

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

        self.api_key_vectordb=self.config["vectordb"][self.vectordb]["api_key"]
        self.base_url_vectordb=self.config["vectordb"][self.vectordb]["endpoint"]

        self.base_url_embedded=self.config['models'][self.model]['embedded']['base_url']
        self.model_embedded=self.config['models'][self.model]['embedded']['model']
        self.api_key_embedded=self.config['models'][self.model]['embedded']['api_key']
        
        self.model_llm_client=self.config['models'][self.model]['llm_client']['model']
        self.base_url_llm_client=self.config['models'][self.model]['llm_client']['base_url']
        self.api_key_llm_client=self.config['models'][self.model]['llm_client']['api_key']

        self.embedded=ModelEmbedder(
            model=self.model_embedded,
            base_url=self.base_url_embedded,
            api_key=self.api_key_embedded
        )
        self.dimensions = self.embedded.get_vectorspace_dimensions

        self.prompt_template = PromptAssistance()
        self.vector_store=QdrantVectorStore(
            api_key=self.api_key_vectordb,
            endpoint=self.base_url_vectordb
        )
        self.retriever = QdrantRetriever(
            vector_store=self.vector_store,
            embedder=self.embedded
        )
        self.llm_client=ThinkingFromKnowledgeBase(
            api_key=self.api_key_llm_client,
            base_url=self.base_url_llm_client,
            model=self.model_llm_client,
            provider=self.model
        )
    @abstractmethod 
    def query(
        self, 
        collection_name:str,
        text:str
    ):
        pass 

class AskAndAnswer(ConstructorLoops):
    def query(self, text:str, collection_name:str):
        retrieved_chunks = self.retriever.retrieve(
            user_id=self.user_id,
            collection_name=collection_name,
            query=text,
            top_k=5
        )
        if isinstance(retrieved_chunks, list) and len(retrieved_chunks) > 0 and isinstance(retrieved_chunks[0], dict):
            context_str = "\n---\n".join([chunk.get("text", "") for chunk in retrieved_chunks])
        else:
            context_str = str(retrieved_chunks)

        messages = self.prompt_template.build(
            template_name="rag_assistance",
            context=context_str,
            query=text
        )

        response=self.llm_client.generate(
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        return response

class QdrantCollection(ConstructorLoops):
    def query(self, text:str, collection_name:str) -> None:
        pass

    def create(self, collection_name):
        return self.vector_store.create_collection(
            user_id=self.user_id,
            vector_size=self.dimensions,
            collection_name=collection_name
        )

    def delete(self, collection_name:str):
        return self.vector_store.delete_collection(
            user_id=self.user_id,
            collection_name=collection_name
        )
    
def main():
    load_dotenv()
    model_chosen = "deepseek"
    # load config
    config = OmegaConfigLoader(config_path="config/config.yml").load(
        vectordb={
            "qdrant":{
                "endpoint": os.getenv("QDRANT_ENDPOINT"),
                "api_key": os.getenv("QDRANT_API_KEY")
            }
        },
        models={
            model_chosen: {
                "llm_client": {
                    "max_tokens": 500,
                    "temperature": 0.7,
                    "api_key": os.getenv(f"{model_chosen.upper()}_API_KEY")
                }
            }
        }
    )
    user_id = 'huypham'
    collection_name = "AI"
    user_name = 'user_default_user_documents'
    question = "Hello ! vectorDB là gì"

    # Create Collection
    QdrantCollection(
        config=config,
        user_id=user_id,
        user_name=user_name,
        model=model_chosen
    ).create(collection_name=collection_name)


    rag_pipeline = AskAndAnswer(
        config=config,
        user_id=user_id,
        user_name=user_name,
        model=model_chosen
    )
    response = rag_pipeline.query(
        text=question,
        collection_name=collection_name
    )   
    
    print("Repsonding: \n")
    print(response.text)

if __name__ == "__main__":
    main()  