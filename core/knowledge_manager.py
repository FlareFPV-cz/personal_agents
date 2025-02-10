from typing import Dict, List, Optional, Any
import chromadb
from networkx import DiGraph
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

class KnowledgeManager:
    """Manages knowledge components including RAG, vector storage, and knowledge graph."""

    def __init__(self, embedding_model: str = "text-embedding-3-small"):
        """Initialize knowledge management components.

        Args:
            embedding_model: The OpenAI embedding model to use
        """
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = None
        self.knowledge_graph = DiGraph()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def initialize_vector_store(self, persist_directory: str = "./vector_store"):
        """Initialize the vector store with ChromaDB.

        Args:
            persist_directory: Directory to persist vector store
        """
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )

    def add_documents(self, documents: List[str], metadata: Optional[List[Dict]] = None):
        """Add documents to the vector store.

        Args:
            documents: List of document texts
            metadata: Optional metadata for each document
        """
        chunks = self.text_splitter.split_text(documents)
        if self.vector_store is None:
            self.initialize_vector_store()
        self.vector_store.add_texts(texts=chunks, metadatas=metadata)

    def search_similar(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents in the vector store.

        Args:
            query: The search query
            k: Number of results to return

        Returns:
            List of similar documents with their metadata
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized")
        return self.vector_store.similarity_search(query, k=k)

    def add_knowledge_node(self, node_id: str, attributes: Dict[str, Any]):
        """Add a node to the knowledge graph.

        Args:
            node_id: Unique identifier for the node
            attributes: Node attributes
        """
        self.knowledge_graph.add_node(node_id, **attributes)

    def add_knowledge_relation(self, from_node: str, to_node: str, relation_type: str):
        """Add a relation between nodes in the knowledge graph.

        Args:
            from_node: Source node ID
            to_node: Target node ID
            relation_type: Type of relation
        """
        self.knowledge_graph.add_edge(from_node, to_node, relation=relation_type)

    def get_related_nodes(self, node_id: str) -> Dict[str, List[str]]:
        """Get nodes related to a given node.

        Args:
            node_id: ID of the node to find relations for

        Returns:
            Dictionary of incoming and outgoing relations
        """
        return {
            "incoming": list(self.knowledge_graph.predecessors(node_id)),
            "outgoing": list(self.knowledge_graph.successors(node_id))
        }