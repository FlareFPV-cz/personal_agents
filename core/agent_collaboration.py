from typing import Dict, Any, List, Optional
from core.base_agent import BaseAgent
from utils.error_handler import CollaborationError

class AgentCollaboration:
    """Manages collaboration and communication between agents."""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: List[Dict[str, Any]] = []
        self.knowledge_store: List[Dict[str, Any]] = []
        self.knowledge_graph: Dict[str, Dict[str, Any]] = {}

    def register_agent(self, agent_id: str, agent: BaseAgent) -> None:
        """Register an agent for collaboration.

        Args:
            agent_id: Unique identifier for the agent
            agent: Instance of BaseAgent or its subclasses
        """
        if not isinstance(agent, BaseAgent):
            raise CollaborationError(f"Invalid agent type for {agent_id}")
        self.agents[agent_id] = agent

    def send_message(self, from_agent: str, to_agent: str, message: Dict[str, Any]) -> None:
        """Send a message from one agent to another.

        Args:
            from_agent: ID of the sending agent
            to_agent: ID of the receiving agent
            message: Message content and metadata
        """
        if from_agent not in self.agents or to_agent not in self.agents:
            raise CollaborationError("Invalid agent ID")

        self.message_queue.append({
            'from': from_agent,
            'to': to_agent,
            'content': message,
            'status': 'pending'
        })

    def process_messages(self) -> List[Dict[str, Any]]:
        """Process pending messages in the queue.

        Returns:
            List of processed messages with results
        """
        processed_messages = []

        for message in self.message_queue:
            if message['status'] == 'pending':
                try:
                    receiving_agent = self.agents[message['to']]
                    result = receiving_agent.run(**message['content'])
                    message['status'] = 'completed'
                    message['result'] = result
                except Exception as e:
                    message['status'] = 'failed'
                    message['error'] = str(e)
                processed_messages.append(message)

        return processed_messages

    def share_knowledge(self, agent_id: str, knowledge: Dict[str, Any]) -> None:
        """Share knowledge from an agent to the shared memory.

        Args:
            agent_id: ID of the agent sharing knowledge
            knowledge: Knowledge to be shared
        """
        if agent_id not in self.agents:
            raise CollaborationError("Invalid agent ID")

        # Store knowledge in memory
        knowledge_entry = {
            'agent_id': agent_id,
            'content': knowledge,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
        self.knowledge_store.append(knowledge_entry)

        # Add to knowledge graph
        node_id = f"knowledge_{len(self.knowledge_graph)}"
        self.knowledge_graph[node_id] = {
            'agent_id': agent_id,
            'content': knowledge,
            'connections': []
        }

    def query_shared_knowledge(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Query the shared knowledge base.

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant knowledge entries
        """
        # Simple keyword-based search
        results = []
        for entry in self.knowledge_store:
            if any(keyword.lower() in str(entry['content']).lower() for keyword in query.split()):
                results.append(entry)

        # Sort by timestamp (most recent first) and limit to k results
        results.sort(key=lambda x: x['timestamp'], reverse=True)
        return results[:k]