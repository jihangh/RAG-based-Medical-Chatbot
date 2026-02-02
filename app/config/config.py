import yaml
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from openai import OpenAI
from langchain_openai import ChatOpenAI

load_dotenv()  # Loads .env automatically

@dataclass
class RAGConfig:
    url: str
    pdfname: str
    chunk_size: int
    chunk_overlap: int
    pinecone_vector_client: Pinecone
    index_name: str
    name_space: str
    openai_client: OpenAI
    dense_model: str
    dim: int
    batch_size: int
    sleep_time: float
    top_ret_doc: int
    alpha: float
    model_name: str  # Name of the LLM model (from YAML)
    model_temperature: float  # Temperature for the LLM model (from YAML)

    @staticmethod
    def from_yaml(path: str) -> "RAGConfig":
        """Load RAG configuration from a YAML file and .env secrets."""
        # Load non-secret parameters from YAML
        with open(path, "r") as f:
            cfg = yaml.safe_load(f)

        # Load secrets from .env
        pinecone_api_key = os.environ["PINECONE_API_KEY"]
        openai_api_key = os.environ["OPENAI_API_KEY"]

        return RAGConfig(
            url=cfg["knowledge_base"]["url"],
            pdfname=cfg["knowledge_base"]["pdfname"],
            chunk_size=cfg["knowledge_base"]["chunk_size"],
            chunk_overlap=cfg["knowledge_base"]["chunk_overlap"],
            pinecone_vector_client=Pinecone(api_key=pinecone_api_key),
            index_name=cfg["pinecone"]["index_name"],
            name_space=cfg["pinecone"]["name_space"],
            openai_client=OpenAI(api_key=openai_api_key),
            dense_model=cfg["retriever"]["dense_model"],
            dim=cfg["retriever"]["dim"],
            batch_size=cfg["vector_store"]["batch_size"],
            sleep_time=cfg["vector_store"]["sleep_time"],
            top_ret_doc=cfg["retriever"]["top_ret_doc"],
            alpha=cfg["retriever"]["alpha"],
            model_name=cfg["openai"]["model"],
            model_temperature=cfg["openai"]["temperature"]
        )

    def get_llm(self) -> ChatOpenAI:
        """Create the ChatOpenAI model object from the stored model name."""
        return ChatOpenAI(model=self.model_name, 
                          temperature=self.model_temperature)
