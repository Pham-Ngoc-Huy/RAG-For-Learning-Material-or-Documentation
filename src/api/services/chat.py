from abc import ABC, abstractmethod

from src.actions.construction import AskAndAnswer


class ChatService(ABC):
    @abstractmethod
    async def chat(
        self,
        user_id: str,
        user_name: str,
        collection_name: str,
        question: str,
        model: str,
    ) -> dict:
        pass


class ChatWithRAGAssistance(ChatService):
    def __init__(self, config):
        self.config = config

    async def chat(
        self,
        user_id: str,
        user_name: str,
        collection_name: str,
        question: str,
        model: str,
    ) -> dict:
        rag_pipeline = AskAndAnswer(
            config=self.config,
            user_id=user_id,
            user_name=user_name,
            model=model,
        )
        response = rag_pipeline.query(text=question, collection_name=collection_name)

        return {
            "answer": response.text,
            "provider": response.provider,
            "model": response.model,
        }
