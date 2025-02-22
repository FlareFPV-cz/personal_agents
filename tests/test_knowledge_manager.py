import unittest
import os
import shutil
from core.knowledge_manager import KnowledgeManager

class TestKnowledgeManager(unittest.TestCase):
    """Test cases for KnowledgeManager class."""

    def setUp(self):
        """Set up test environment."""
        self.km = KnowledgeManager()
        self.test_docs = [
            "This is a test document",
            "Another test document",
            "AI and machine learning are fascinating fields",
            "Document about natural language processing",
            "Test document for performance testing"
        ]
        self.test_metadata = [
            {"source": "test1", "author": "author1"},
            {"source": "test2", "author": "author2"},
            {"source": "test3", "author": "author3"},
            {"source": "test4", "author": "author4"},
            {"source": "test5", "author": "author5"}
        ]

    def tearDown(self):
        """Clean up test environment."""
        self.km = None

    def test_document_addition(self):
        """Test adding documents to knowledge store."""
        self.km.add_documents(self.test_docs[:2], self.test_metadata[:2])
        self.assertEqual(len(self.km.knowledge_store), 2)
        self.assertEqual(self.km.knowledge_store[0]['content'], self.test_docs[0])
        self.assertEqual(self.km.knowledge_store[0]['metadata'], self.test_metadata[0])

    def test_document_addition_without_metadata(self):
        """Test adding documents without metadata."""
        self.km.add_documents(self.test_docs[:2])
        self.assertEqual(len(self.km.knowledge_store), 2)
        self.assertEqual(self.km.knowledge_store[0]['metadata'], {})

    def test_document_addition_mismatched_metadata(self):
        """Test adding documents with mismatched metadata length."""
        self.km.add_documents(self.test_docs[:3], self.test_metadata[:2])
        self.assertEqual(len(self.km.knowledge_store), 3)
        self.assertEqual(self.km.knowledge_store[2]['metadata'], {})

    def test_similar_search_basic(self):
        """Test basic similarity search functionality."""
        self.km.add_documents(self.test_docs)
        results = self.km.search_similar("AI technology", k=2)
        self.assertGreater(len(results), 0)
        self.assertIn("AI", results[0]['content'])

    def test_similar_search_empty_query(self):
        """Test similarity search with empty query."""
        self.km.add_documents(self.test_docs)
        results = self.km.search_similar("", k=1)
        self.assertEqual(len(results), 0)

    def test_similar_search_no_results(self):
        """Test similarity search with no matching results."""
        self.km.add_documents(self.test_docs)
        results = self.km.search_similar("xyz123", k=1)
        self.assertEqual(len(results), 0)

    def test_knowledge_graph_operations(self):
        """Test knowledge graph node and relation operations."""
        # Test adding nodes
        self.km.add_knowledge_node("node1", {"type": "concept", "name": "AI"})
        self.km.add_knowledge_node("node2", {"type": "concept", "name": "ML"})
        self.km.add_knowledge_node("node3", {"type": "concept", "name": "NLP"})

        # Test adding relations
        self.km.add_knowledge_relation("node1", "node2", "related_to")
        self.km.add_knowledge_relation("node2", "node3", "includes")
        self.km.add_knowledge_relation("node3", "node1", "part_of")

        # Test getting related nodes
        relations = self.km.get_related_nodes("node1")
        self.assertIn("node2", relations["outgoing"])
        self.assertIn("node3", relations["incoming"])

    def test_error_handling(self):
        """Test error handling in knowledge graph operations."""
        # Test nonexistent node
        with self.assertRaises(ValueError):
            self.km.get_related_nodes("nonexistent_node")

        # Test invalid relation
        self.km.add_knowledge_node("node1", {"type": "concept"})
        self.km.add_knowledge_node("node2", {"type": "concept"})
        with self.assertRaises(ValueError):
            self.km.add_knowledge_relation("node1", "nonexistent", "related_to")

    def test_performance(self):
        """Test performance with larger datasets."""
        # Add many documents
        large_docs = [f"Document {i} content" for i in range(100)]
        large_metadata = [{"source": f"source{i}"} for i in range(100)]
        self.km.add_documents(large_docs, large_metadata)

        # Test search performance
        results = self.km.search_similar("content", k=10)
        self.assertLessEqual(len(results), 10)

        # Test graph performance
        for i in range(50):
            self.km.add_knowledge_node(f"perf_node_{i}", {"type": "test"})
        
        for i in range(49):
            self.km.add_knowledge_relation(f"perf_node_{i}", f"perf_node_{i+1}", "next")

        relations = self.km.get_related_nodes("perf_node_0")
        self.assertEqual(len(relations["outgoing"]), 1)

if __name__ == "__main__":
    unittest.main()