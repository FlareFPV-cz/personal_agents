# task_scheduler_example.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.task_scheduler import TaskSchedulerAgent
from utils.logger import AgentLogger

# Initialize logger
logger = AgentLogger("task_scheduler")

# Create task scheduler agent
agent = TaskSchedulerAgent()

# Add some example tasks
tasks = [
    {
        "title": "Complete project documentation",
        "priority": "high",
        "due_date": "2024-03-20"
    },
    {
        "title": "Review pull requests",
        "priority": "medium",
        "due_date": "2024-03-15"
    }
]

# Add tasks to scheduler
for task in tasks:
    result = agent.add_task(task)
    logger.info(f"Added task: {result['data']['title']}")

# List all tasks
all_tasks = agent.list_tasks()
logger.info(f"All tasks: {all_tasks['data']}")

# Get task recommendations
query = "What tasks should I focus on today?"
recommendations = agent.run(query)
logger.info(f"Recommendations: {recommendations['data']}")

# Filter tasks by priority
high_priority = agent.list_tasks({"priority": "high"})
logger.info(f"High priority tasks: {high_priority['data']}")