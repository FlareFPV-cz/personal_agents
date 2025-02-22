from core.knowledge_manager import KnowledgeManager
from typing import Dict, List
from datetime import datetime

def demonstrate_document_management():
    """Demonstrate document management capabilities."""
    km = KnowledgeManager()
    
    # Add research papers with metadata
    papers = [
        "Deep learning has revolutionized artificial intelligence and machine learning.",
        "Natural language processing enables computers to understand human language.",
        "Knowledge graphs represent semantic relationships between entities."
    ]
    
    metadata = [
        {"author": "Smith, J.", "year": 2023, "topic": "deep learning"},
        {"author": "Johnson, A.", "year": 2022, "topic": "NLP"},
        {"author": "Brown, R.", "year": 2023, "topic": "knowledge graphs"}
    ]
    
    km.add_documents(papers, metadata)
    print("Added research papers to knowledge store\n")
    
    # Search for relevant papers
    query = "machine learning AI"
    results = km.search_similar(query, k=2)
    print(f"Search results for '{query}':\n")
    for doc in results:
        print(f"Content: {doc['content']}")
        print(f"Metadata: {doc['metadata']}\n")

def demonstrate_knowledge_graph():
    """Demonstrate knowledge graph capabilities."""
    km = KnowledgeManager()
    
    # Create knowledge graph of AI concepts
    concepts = [
        ("ai", {"name": "Artificial Intelligence", "type": "field"}),
        ("ml", {"name": "Machine Learning", "type": "subfield"}),
        ("dl", {"name": "Deep Learning", "type": "technique"}),
        ("nlp", {"name": "Natural Language Processing", "type": "application"})
    ]
    
    # Add nodes
    for node_id, attrs in concepts:
        km.add_knowledge_node(node_id, attrs)
    
    # Add relationships
    relationships = [
        ("ai", "ml", "includes"),
        ("ml", "dl", "uses"),
        ("ai", "nlp", "enables"),
        ("ml", "nlp", "supports")
    ]
    
    for from_node, to_node, rel_type in relationships:
        km.add_knowledge_relation(from_node, to_node, rel_type)
    
    # Explore relationships
    print("Knowledge Graph Relationships:\n")
    for node_id, attrs in concepts:
        relations = km.get_related_nodes(node_id)
        print(f"Node: {attrs['name']}")
        print(f"Incoming connections: {relations['incoming']}")
        print(f"Outgoing connections: {relations['outgoing']}\n")

def main():
    print("=== Document Management Demo ===")
    demonstrate_document_management()
    
    print("\n=== Knowledge Graph Demo ===")
    demonstrate_knowledge_graph()

if __name__ == "__main__":
    main()