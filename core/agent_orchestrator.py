from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from core.base_agent import BaseAgent
from core.agent_collaboration import AgentCollaboration
from core.knowledge_manager import KnowledgeManager
from utils.error_handler import CollaborationError
import asyncio
import logging

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class Task:
    id: str
    name: str
    priority: TaskPriority
    dependencies: List[str]
    assigned_agent: Optional[str]
    status: TaskStatus
    max_retries: int
    retry_count: int
    created_at: datetime
    updated_at: datetime
    result: Optional[Any]
    error: Optional[str]

class AgentOrchestrator:
    """Advanced orchestration system for managing complex multi-agent workflows."""

    def __init__(self):
        self.collaboration_manager = AgentCollaboration()
        self.knowledge_manager = KnowledgeManager()
        self.tasks: Dict[str, Task] = {}
        self.agent_metrics: Dict[str, Dict[str, Any]] = {}
        self.workflow_hooks: Dict[str, List[Callable]] = {}
        
    def register_agent(self, agent_id: str, agent: BaseAgent, capabilities: List[str]) -> None:
        """Register an agent with its capabilities."""
        self.collaboration_manager.register_agent(agent_id, agent)
        self.agent_metrics[agent_id] = {
            'capabilities': capabilities,
            'current_load': 0,
            'success_rate': 1.0,
            'avg_response_time': 0.0,
            'last_active': datetime.now()
        }

    def create_task(self, name: str, priority: TaskPriority, dependencies: List[str] = None) -> str:
        """Create a new task in the workflow."""
        task_id = f"task_{len(self.tasks)}"
        self.tasks[task_id] = Task(
            id=task_id,
            name=name,
            priority=priority,
            dependencies=dependencies or [],
            assigned_agent=None,
            status=TaskStatus.PENDING,
            max_retries=3,
            retry_count=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            result=None,
            error=None
        )
        return task_id

    async def execute_workflow(self, entry_tasks: List[str]) -> Dict[str, Any]:
        """Execute a workflow of interdependent tasks."""
        results = {}
        pending_tasks = entry_tasks.copy()

        while pending_tasks:
            ready_tasks = [t for t in pending_tasks 
                         if all(dep not in pending_tasks for dep in self.tasks[t].dependencies)]
            
            if not ready_tasks:
                raise CollaborationError("Circular dependency detected in workflow")

            # Execute ready tasks in parallel
            tasks = [self._execute_task(task_id) for task_id in ready_tasks]
            completed = await asyncio.gather(*tasks, return_exceptions=True)

            for task_id, result in zip(ready_tasks, completed):
                if isinstance(result, Exception):
                    logging.error(f"Task {task_id} failed: {str(result)}")
                    self.tasks[task_id].status = TaskStatus.FAILED
                    self.tasks[task_id].error = str(result)
                else:
                    results[task_id] = result
                pending_tasks.remove(task_id)

        return results

    async def _execute_task(self, task_id: str) -> Any:
        """Execute a single task with retry logic and agent selection."""
        task = self.tasks[task_id]
        
        while task.retry_count <= task.max_retries:
            try:
                # Select best agent based on load and performance
                selected_agent = self._select_optimal_agent(task)
                if not selected_agent:
                    raise CollaborationError("No suitable agent available")

                task.assigned_agent = selected_agent
                task.status = TaskStatus.IN_PROGRESS
                task.updated_at = datetime.now()

                # Execute task and update metrics
                start_time = datetime.now()
                result = await self._run_agent_task(selected_agent, task)
                execution_time = (datetime.now() - start_time).total_seconds()

                self._update_agent_metrics(selected_agent, True, execution_time)
                
                task.status = TaskStatus.COMPLETED
                task.result = result
                return result

            except Exception as e:
                task.retry_count += 1
                task.error = str(e)
                task.status = TaskStatus.RETRYING if task.retry_count <= task.max_retries else TaskStatus.FAILED
                self._update_agent_metrics(task.assigned_agent, False, 0)
                
                if task.status == TaskStatus.FAILED:
                    raise

                await asyncio.sleep(2 ** task.retry_count)  # Exponential backoff

    def _select_optimal_agent(self, task: Task) -> Optional[str]:
        """Select the best agent based on load, performance, and capabilities."""
        candidates = []
        for agent_id, metrics in self.agent_metrics.items():
            if metrics['current_load'] < 0.8:  # Load threshold
                score = (
                    metrics['success_rate'] * 0.4 +
                    (1 - metrics['current_load']) * 0.4 +
                    (1 / (metrics['avg_response_time'] + 1)) * 0.2
                )
                candidates.append((agent_id, score))

        if not candidates:
            return None

        return max(candidates, key=lambda x: x[1])[0]

    async def _run_agent_task(self, agent_id: str, task: Task) -> Any:
        """Execute task on selected agent with proper monitoring."""
        agent = self.collaboration_manager.agents[agent_id]
        self.agent_metrics[agent_id]['current_load'] += 1

        try:
            result = await asyncio.to_thread(agent.run, task=task.name)
            
            # Share task result in knowledge store
            self.knowledge_manager.add_documents(
                [str(result)],
                [{'task_id': task.id, 'agent_id': agent_id}]
            )
            
            return result
        finally:
            self.agent_metrics[agent_id]['current_load'] -= 1
            self.agent_metrics[agent_id]['last_active'] = datetime.now()

    def _update_agent_metrics(self, agent_id: str, success: bool, execution_time: float) -> None:
        """Update agent performance metrics."""
        metrics = self.agent_metrics[agent_id]
        metrics['success_rate'] = (
            metrics['success_rate'] * 0.9 +
            (1.0 if success else 0.0) * 0.1
        )
        if success:
            metrics['avg_response_time'] = (
                metrics['avg_response_time'] * 0.9 +
                execution_time * 0.1
            )

    def add_workflow_hook(self, event: str, callback: Callable) -> None:
        """Add a hook to be called during workflow execution."""
        if event not in self.workflow_hooks:
            self.workflow_hooks[event] = []
        self.workflow_hooks[event].append(callback)

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get detailed status of a task."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")

        task = self.tasks[task_id]
        return {
            'id': task.id,
            'name': task.name,
            'status': task.status.value,
            'assigned_agent': task.assigned_agent,
            'retry_count': task.retry_count,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat(),
            'error': task.error
        }