# Personal AI Agents

## Overview
A framework for building and managing personal AI agents using LangChain. This project provides a flexible and extensible architecture for creating specialized AI agents that can assist with various tasks.

## Features
- Modular agent architecture with BaseAgent class
- Built-in error handling and logging
- Configuration management system
- Multiple specialized agents (Content Analyst, Mail Agent, Researcher)
- Comprehensive testing framework

## Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key for LLM access

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/personal_agents.git
cd personal_agents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root and add:
```
GROQ_API_KEY=your_api_key_here
AGENT_CONFIG_PATH=path/to/config.json  # Optional
```

## Architecture

### Core Components
- **BaseAgent**: Foundation class for all agents
- **Knowledge Manager**: Handles agent knowledge and memory
- **Config Manager**: Manages configuration and settings
- **Error Handler**: Provides standardized error handling
- **Logger**: Configurable logging utility

### Available Agents
- **Content Analyst**: Analyzes and processes content
- **Mail Agent**: Handles email-related tasks
- **Researcher**: Performs research and information gathering

## Usage

### Basic Example
```python
from agents.researcher import ResearchAgent
from utils.logger import AgentLogger

# Initialize logger
logger = AgentLogger("research_agent")

# Create and run agent
agent = ResearchAgent()
result = agent.run(query="your research query")
```

### Configuration
```python
from utils.config_manager import ConfigManager

config = ConfigManager()
config.set("api_timeout", 30)
config.save()
```

## Testing
Run the test suite:
```bash
python -m unittest discover tests
```

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Project Structure
```
personal_agents/
├── agents/             # Specialized agent implementations
├── core/              # Core framework components
├── tests/             # Test suite
├── utils/             # Utility modules
└── requirements.txt   # Project dependencies
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements
- Additional specialized agents
- Enhanced memory management
- Integration with more LLM providers
- Web interface for agent management
- Performance optimizations