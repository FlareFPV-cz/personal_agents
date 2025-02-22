from core.agent_collaboration import AgentCollaboration
from core.base_agent import BaseAgent
from typing import Dict, Any

class DataProcessingAgent(BaseAgent):
    def run(self, **kwargs) -> Dict[str, Any]:
        data = kwargs.get('data', [])
        return {"processed_data": [x * 2 for x in data]}

class AnalysisAgent(BaseAgent):
    def run(self, **kwargs) -> Dict[str, Any]:
        data = kwargs.get('processed_data', [])
        return {"analysis": f"Average value: {sum(data)/len(data) if data else 0}"}

def demonstrate_agent_collaboration():
    # Initialize collaboration system
    collab = AgentCollaboration()
    
    # Create and register agents
    processor = DataProcessingAgent()
    analyzer = AnalysisAgent()
    
    collab.register_agent("processor", processor)
    collab.register_agent("analyzer", analyzer)
    
    # Send data for processing
    initial_data = {"data": [1, 2, 3, 4, 5]}
    collab.send_message("processor", "analyzer", initial_data)
    
    # Process messages
    results = collab.process_messages()
    print("\nMessage Processing Results:")
    for result in results:
        print(f"From: {result['from']}")
        print(f"To: {result['to']}")
        print(f"Status: {result['status']}")
        if 'result' in result:
            print(f"Result: {result['result']}")
    
    # Share knowledge
    knowledge = {
        "topic": "data_processing",
        "description": "Processed numerical data and calculated averages"
    }
    collab.share_knowledge("processor", knowledge)
    
    # Query shared knowledge
    query_results = collab.query_shared_knowledge("data processing", k=1)
    print("\nKnowledge Query Results:")
    for entry in query_results:
        print(f"Agent: {entry['agent_id']}")
        print(f"Content: {entry['content']}")

if __name__ == "__main__":
    print("=== Agent Collaboration Demo ===")
    demonstrate_agent_collaboration()