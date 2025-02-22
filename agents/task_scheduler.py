# task_scheduler.py
import datetime
from typing import Dict, Any, List
from core.base_agent import BaseAgent

class TaskSchedulerAgent(BaseAgent):
    def __init__(self, temperature: float = 0.3):
        super().__init__(temperature=temperature)
        self.tasks = []
        
        # Initialize with task management prompt
        self._initialize_chain("""
        You are a task scheduling assistant. Help organize and prioritize tasks.
        Current tasks: {tasks}
        User request: {query}
        Provide a structured response with task organization and scheduling recommendations.
        """)
    
    def add_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new task to the scheduler"""
        try:
            if not all(k in task for k in ['title', 'priority', 'due_date']):
                raise ValueError("Task must include title, priority, and due_date")
            
            task['created_at'] = datetime.datetime.now().isoformat()
            self.tasks.append(task)
            return self._format_response(task)
        except Exception as e:
            return self._handle_error(e, "add_task")
    
    def list_tasks(self, filter_params: Dict = None) -> Dict[str, Any]:
        """List all tasks with optional filtering"""
        try:
            filtered_tasks = self.tasks
            if filter_params:
                for key, value in filter_params.items():
                    filtered_tasks = [t for t in filtered_tasks if t.get(key) == value]
            return self._format_response(filtered_tasks)
        except Exception as e:
            return self._handle_error(e, "list_tasks")
    
    def run(self, query: str) -> Dict[str, Any]:
        """Process task-related queries and provide recommendations"""
        try:
            response = self.chain.invoke({
                "tasks": self.tasks,
                "query": query
            })
            return self._format_response(str(response.content))
        except Exception as e:
            return self._handle_error(e, "task analysis")