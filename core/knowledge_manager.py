from typing import Dict, List, Optional, Any
from collections import defaultdict
from datetime import datetime
from math import log

class KnowledgeManager:
    """Manages knowledge components using in-memory storage."""

    def __init__(self):
        """Initialize knowledge management components."""
        self.knowledge_store = []
        self.knowledge_graph = {}
        self.knowledge_index = defaultdict(list)  # For text search

    def add_documents(self, documents: List[str], metadata: Optional[List[Dict]] = None) -> None:
        """Add documents to the knowledge store.

        Args:
            documents: List of document texts
            metadata: Optional metadata for each document
        """
        for i, doc in enumerate(documents):
            # Create document entry
            doc_id = f"doc_{len(self.knowledge_store)}"
            doc_entry = {
                'id': doc_id,
                'content': doc,
                'metadata': metadata[i] if metadata and i < len(metadata) else {},
                'timestamp': datetime.now().isoformat(),
                'type': 'document'
            }
            
            # Add to knowledge store
            self.knowledge_store.append(doc_entry)
            
            # Index document words for search
            words = doc.lower().split()
            for word in words:
                self.knowledge_index[word].append(doc_id)

    def search_similar(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents using semantic matching.

        Args:
            query: The search query
            k: Number of results to return

        Returns:
            List of similar documents with their metadata
        """
        # Split query into words and find matching documents
        query_words = query.lower().split()
        matching_docs = defaultdict(float)
        
        # Calculate TF-IDF scores
        doc_count = len(self.knowledge_store)
        for word in query_words:
            # Calculate IDF
            doc_freq = len(self.knowledge_index.get(word, []))
            if doc_freq > 0:
                idf = 1 + log(doc_count / doc_freq)
                
                # Calculate TF for each document
                for doc_id in self.knowledge_index.get(word, []):
                    doc = next(d for d in self.knowledge_store if d['id'] == doc_id)
                    tf = doc['content'].lower().count(word) / len(doc['content'].split())
                    matching_docs[doc_id] += tf * idf
        
        # Sort by TF-IDF score
        sorted_docs = sorted(matching_docs.items(), 
                           key=lambda x: x[1], 
                           reverse=True)
        
        # Get top k results
        results = []
        if query_words:  # Only return results if query is not empty
            for doc_id, score in sorted_docs[:k]:
                if score > 0:  # Only include documents with matching words
                    doc = next(d for d in self.knowledge_store if d['id'] == doc_id)
                    results.append(doc)
        
        return results

    def add_knowledge_node(self, node_id: str, attributes: Dict[str, Any]) -> None:
        """Add a node to the knowledge graph.

        Args:
            node_id: Unique identifier for the node
            attributes: Node attributes
        """
        self.knowledge_graph[node_id] = {
            'attributes': attributes,
            'connections': {'incoming': [], 'outgoing': []}
        }

    def add_knowledge_relation(self, from_node: str, to_node: str, relation_type: str) -> None:
        """Add a relation between nodes in the knowledge graph.

        Args:
            from_node: Source node ID
            to_node: Target node ID
            relation_type: Type of relation
        """
        if from_node not in self.knowledge_graph or to_node not in self.knowledge_graph:
            raise ValueError("Both nodes must exist in the knowledge graph")
            
        self.knowledge_graph[from_node]['connections']['outgoing'].append({
            'to': to_node,
            'type': relation_type
        })
        self.knowledge_graph[to_node]['connections']['incoming'].append({
            'from': from_node,
            'type': relation_type
        })

    def get_related_nodes(self, node_id: str) -> Dict[str, List[str]]:
        """Get nodes related to a given node.

        Args:
            node_id: ID of the node to find relations for

        Returns:
            Dictionary of incoming and outgoing relations
        """
        if node_id not in self.knowledge_graph:
            raise ValueError(f"Node {node_id} not found in knowledge graph")
            
        node = self.knowledge_graph[node_id]
        return {
            'incoming': [conn['from'] for conn in node['connections']['incoming']],
            'outgoing': [conn['to'] for conn in node['connections']['outgoing']]
        }