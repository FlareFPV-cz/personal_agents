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
- Git (for cloning the repository)
- pip (Python package installer)

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

### Configuration Options
- `GROQ_API_KEY`: Your Groq API key for LLM access
- `AGENT_CONFIG_PATH`: Path to custom agent configuration file (optional)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `KNOWLEDGE_BASE_PATH`: Path to persistent knowledge storage

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

### Code Analysis
```python
from agents.code_analyst import CodeHelper

# Initialize analyzer
analyzer = CodeHelper(
    quality_threshold=8.5,
    model_name="llama3-70b-8192"
)

# Analyze code
results = analyzer.analyze("path/to/your/code.py")
print(f"Quality Score: {results['quality_score']}/10")
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

## Troubleshooting

### Common Issues
1. **API Key Issues**
   - Ensure GROQ_API_KEY is properly set in .env file
   - Verify API key permissions and quota

2. **Import Errors**
   - Confirm all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Agent Initialization Failures**
   - Verify configuration file paths
   - Check log files for detailed error messages

### Debug Mode
Enable debug logging by setting:
```env
LOG_LEVEL=DEBUG
```

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation as needed
- Maintain backwards compatibility

## Testing
Run the test suite:
```bash
python -m unittest discover tests
```

For coverage report:
```bash
coverage run -m unittest discover
coverage report
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
