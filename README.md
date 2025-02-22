# Personal AI Agents

## Overview
A comprehensive framework for building and managing intelligent AI agents powered by LangChain. This project provides a modular and extensible architecture for creating specialized AI agents that can assist with various tasks including data analysis, research, content analysis, and task scheduling.

## Key Features
- **Modular Agent Architecture**: Built on a robust BaseAgent class for consistent behavior
- **Specialized Agents**:
  - Data Analyst: Statistical analysis and data visualization
  - Content Analyst: Text and content processing
  - Task Scheduler: Intelligent task management
  - Researcher: Information gathering and analysis
  - Mail Agent: Email processing and management
  - Code Analyst: Code analysis and quality assessment
- **Built-in Utilities**:
  - Advanced error handling and logging
  - Configuration management
  - Knowledge management system

## Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key for LLM access

### Quick Start
1. Clone the repository:
```bash
git clone https://github.com/FlareFPV-cz/personal_agents.git
cd personal_agents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_api_key_here
AGENT_CONFIG_PATH=path/to/config.json  # Optional
```

## Usage Examples

### Data Analysis
```python
from agents.data_analyst import DataAnalystAgent
from utils.logger import AgentLogger

# Initialize
logger = AgentLogger("data_analyst")
agent = DataAnalystAgent()

# Load and analyze data
df = pd.read_csv("your_data.csv")
result = agent.load_data(df)
summary = agent.generate_summary()

# Create visualizations
agent.create_visualization('histogram', 'age')
agent.create_visualization('scatter', 'income', 'education')
```

### Task Scheduling
```python
from agents.task_scheduler import TaskSchedulerAgent

agent = TaskSchedulerAgent()

# Add tasks
task = {
    "title": "Project Review",
    "priority": "high",
    "due_date": "2024-03-20"
}
agent.add_task(task)

# Get recommendations
recommendations = agent.run("What should I focus on today?")
```

## Architecture

### Core Components
- **BaseAgent**: Foundation class implementing common agent functionality
- **Knowledge Manager**: Handles persistent knowledge storage and retrieval
- **Config Manager**: Manages agent configurations and settings
- **Logger**: Advanced logging with configurable outputs
- **Error Handler**: Standardized error management system

### Agent Capabilities
- Data analysis and visualization
- Natural language task management
- Content analysis and processing
- Code quality assessment
- Research and information gathering
- Email processing and management

## Project Structure
```
personal_agents/
├── agents/             # Specialized agent implementations
├── core/              # Core framework components
├── examples/          # Usage examples and demos
├── tests/             # Comprehensive test suite
├── utils/             # Utility modules
└── requirements.txt   # Project dependencies
```

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing
Run the test suite:
```bash
python -m unittest discover tests
```

## Future Roadmap
- Enhanced agent collaboration capabilities
- Additional specialized agents
- Advanced memory management system
- Web interface for agent management
- Multi-modal agent interactions
- Performance optimizations

## License
This project is licensed under the MIT License - see the LICENSE file for details.
