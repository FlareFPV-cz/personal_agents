import unittest
from core.agent_collaboration import AgentCollaboration
from core.base_agent import BaseAgent

class MockAgent(BaseAgent):
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.last_run_params = None

    def run(self, **kwargs):
        self.last_run_params = kwargs
        return {"status": "success", "result": f"Processed by {self.agent_id}"}

class TestAgentCollaboration(unittest.TestCase):
    def setUp(self):
        self.collab = AgentCollaboration()
        self.agent1 = MockAgent("agent1")
        self.agent2 = MockAgent("agent2")

    def test_register_agent(self):
        """Test agent registration functionality."""
        self.collab.register_agent("agent1", self.agent1)
        self.assertIn("agent1", self.collab.agents)
        self.assertEqual(self.collab.agents["agent1"], self.agent1)

    def test_register_invalid_agent(self):
        """Test registration with invalid agent type."""
        with self.assertRaises(Exception):
            self.collab.register_agent("invalid", "not_an_agent")

    def test_send_message(self):
        """Test message sending between agents."""
        self.collab.register_agent("agent1", self.agent1)
        self.collab.register_agent("agent2", self.agent2)

        message = {"task": "process_data", "data": "test_data"}
        self.collab.send_message("agent1", "agent2", message)

        self.assertEqual(len(self.collab.message_queue), 1)
        queued_message = self.collab.message_queue[0]
        self.assertEqual(queued_message["from"], "agent1")
        self.assertEqual(queued_message["to"], "agent2")
        self.assertEqual(queued_message["content"], message)
        self.assertEqual(queued_message["status"], "pending")

    def test_process_messages(self):
        """Test message processing functionality."""
        self.collab.register_agent("agent1", self.agent1)
        self.collab.register_agent("agent2", self.agent2)

        message = {"task": "process_data", "data": "test_data"}
        self.collab.send_message("agent1", "agent2", message)

        processed = self.collab.process_messages()
        self.assertEqual(len(processed), 1)
        self.assertEqual(processed[0]["status"], "completed")
        self.assertEqual(processed[0]["result"]["result"], "Processed by agent2")

    def test_share_knowledge(self):
        """Test knowledge sharing functionality."""
        self.collab.register_agent("agent1", self.agent1)
        knowledge = {"topic": "AI", "content": "Test knowledge"}
        
        self.collab.share_knowledge("agent1", knowledge)
        self.assertEqual(len(self.collab.knowledge_store), 1)
        self.assertEqual(self.collab.knowledge_store[0]["agent_id"], "agent1")
        self.assertEqual(self.collab.knowledge_store[0]["content"], knowledge)

    def test_query_shared_knowledge(self):
        """Test querying shared knowledge."""
        self.collab.register_agent("agent1", self.agent1)
        knowledge1 = {"topic": "AI", "content": "Machine learning basics"}
        knowledge2 = {"topic": "NLP", "content": "Natural language understanding"}
        
        self.collab.share_knowledge("agent1", knowledge1)
        self.collab.share_knowledge("agent1", knowledge2)

        results = self.collab.query_shared_knowledge("machine learning", k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], knowledge1)

if __name__ == "__main__":
    unittest.main()