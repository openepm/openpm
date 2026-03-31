from __future__ import annotations

from typing import Dict, List, Literal, Optional

from openenv.core.env_server.interfaces import Action, Observation, State
from pydantic import Field

Priority = Literal["low", "medium", "high", "critical"]
ActionType = Literal[
    "assign_task",
    "reprioritize_task",
    "split_task",
    "request_help",
    "delay_task",
    "mark_complete",
]


class PMAction(Action):
    """Decision issued by the project manager agent."""

    action_type: ActionType
    task_id: Optional[str] = None
    developer_id: Optional[str] = None
    priority: Optional[Priority] = None


class DeveloperSnapshot(State):
    """Developer availability and load information."""

    developer_id: str
    available: bool = True
    assigned_task_id: Optional[str] = None
    skill_profile: Dict[str, float] = Field(default_factory=dict)


class TaskSnapshot(State):
    """Task-level state used in observations and internal state."""

    task_id: str
    title: str
    priority: Priority = "medium"
    domain: str = "backend"
    dependencies: List[str] = Field(default_factory=list)
    blocked: bool = False
    assigned_to: Optional[str] = None
    effort_total: float = 1.0
    effort_remaining: float = 1.0
    due_day: int = 1
    status: Literal["todo", "in_progress", "completed"] = "todo"
    metadata: Dict[str, str | bool | int | float] = Field(default_factory=dict)


class PMState(State):
    """Full deterministic sprint state."""

    scenario_id: str = "easy"
    day: int = 0
    max_days: int = 10
    sprint_progress: float = 0.0
    risk_level: float = 0.0
    time_remaining: int = 10
    project_completed: bool = False
    project_failed: bool = False
    invalid_action_count: int = 0
    score: float = 0.0
    developers: List[DeveloperSnapshot] = Field(default_factory=list)
    tasks: List[TaskSnapshot] = Field(default_factory=list)


class PMObservation(Observation):
    """Structured observation returned after each transition."""

    scenario_id: str = "easy"
    day: int = 0
    max_days: int = 10
    sprint_progress: float = 0.0
    risk_level: float = 0.0
    time_remaining: int = 10
    active_tasks: List[TaskSnapshot] = Field(default_factory=list)
    blocked_tasks: List[str] = Field(default_factory=list)
    developer_availability: Dict[str, bool] = Field(default_factory=dict)
    developer_skill_levels: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    event_log: List[str] = Field(default_factory=list)
    score: float = 0.0
