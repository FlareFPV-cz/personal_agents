import unittest
import os
import shutil
from core.knowledge_manager import KnowledgeManager

class TestKnowledgeManager(unittest.TestCase):
    """Test cases for KnowledgeManager class."""

    def setUp(self):
        """Set up test environment."""
        self.test_persist_dir = "./test_vector_store"
        self.km = KnowledgeManager()

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_persist_dir):
            shutil.rmtree(self.test_persist_dir)

    def test_vector_store_initialization(self):
        """Test vector store initialization."""
        self.km.initialize_vector_store(self.test_persist_dir)
        self.assertIsNotNone(self.km.vector_store)

    def test_document_addition(self):
        """Test adding documents to vector store."""
        test_docs = ["This is a test document", "Another test document"]
        test_metadata = [{"source": "test1"}, {"source": "test2"}]
        self.km.add_documents(test_docs, test_metadata)
        self.assertIsNotNone(self.km.vector_store)

    def test_similar_search(self):
        """Test similarity search functionality."""
        test_docs = ["AI and machine learning are fascinating fields"]
        self.km.add_documents(test_docs)
        results = self.km.search_similar("AI technology", k=1)
        self.assertEqual(len(results), 1)

    def test_knowledge_graph_operations(self):
        """Test knowledge graph node and relation operations."""
        # Test adding nodes
        self.km.add_knowledge_node("node1", {"type": "concept", "name": "AI"})
        self.km.add_knowledge_node("node2", {"type": "concept", "name": "ML"})

        # Test adding relations
        self.km.add_knowledge_relation("node1", "node2", "related_to")

        # Test getting related nodes
        relations = self.km.get_related_nodes("node1")
        self.assertIn("node2", relations["outgoing"])
        self.assertEqual(len(relations["incoming"]), 0)

    def test_error_handling(self):
        """Test error handling in vector store operations."""
        with self.assertRaises(ValueError):
            self.km.search_similar("test query")

if __name__ == "__main__":
    unittest.main()