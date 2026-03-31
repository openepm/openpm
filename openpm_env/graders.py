from __future__ import annotations

from typing import List

from openpm_env.models import PMState, TaskSnapshot


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _count_completed(tasks: List[TaskSnapshot]) -> int:
    return sum(1 for task in tasks if task.status == "completed")


def _deadline_penalty(state: PMState) -> float:
    overdue = sum(1 for task in state.tasks if task.status != "completed" and state.day > task.due_day)
    return min(0.6, overdue * 0.1)


def grade_state(state: PMState) -> float:
    total_tasks = max(1, len(state.tasks))
    completed_ratio = _count_completed(state.tasks) / total_tasks
    invalid_penalty = min(0.4, state.invalid_action_count * 0.05)
    risk_penalty = min(0.3, state.risk_level * 0.3)
    score = completed_ratio - _deadline_penalty(state) - invalid_penalty - risk_penalty
    if state.project_completed and not state.project_failed:
        score += 0.2
    return _clamp01(score)


def grade_easy(state: PMState) -> float:
    return grade_state(state)


def grade_medium(state: PMState) -> float:
    return grade_state(state)


def grade_hard(state: PMState) -> float:
    return grade_state(state)


def grade_for_task(task_id: str, state: PMState) -> float:
    task_id = task_id.lower()
    if task_id == "easy":
        return grade_easy(state)
    if task_id == "medium":
        return grade_medium(state)
    if task_id == "hard":
        return grade_hard(state)
    raise ValueError(f"Unknown task_id: {task_id}")
