from __future__ import annotations

import statistics

import pytest
from pydantic import ValidationError

from openpm_env import PMAction
from openpm_env.agents.baselines import AdvancedRuleBasedAgent
from openpm_env.env import OpenPMEnvironment
from openpm_env.graders import grade_for_task


def test_reset_returns_valid_observation() -> None:
    env = OpenPMEnvironment()
    obs = env.reset(task_id="easy", seed=42)

    assert obs is not None
    assert obs.active_tasks
    assert obs.developer_availability
    assert 0.0 <= obs.score <= 1.0


def test_invalid_action_validation_and_penalty() -> None:
    with pytest.raises(ValidationError):
        PMAction(action_type="not_a_real_action", task_id="T1")

    env = OpenPMEnvironment()
    obs = env.reset(task_id="easy", seed=42)
    task_id = obs.active_tasks[0].task_id

    invalid_obs = env.step(PMAction(action_type="assign_task", task_id=task_id, developer_id="missing-dev"))

    assert env._state.invalid_action_count > 0
    assert invalid_obs.score < obs.score or any("invalid:" in e for e in invalid_obs.event_log)


def test_request_help_exploit_prevention() -> None:
    env = OpenPMEnvironment()
    obs = env.reset(task_id="easy", seed=42)

    unblocked_task = next(task for task in obs.active_tasks if not task.blocked and task.status != "completed")
    helper_id = next(dev_id for dev_id, available in obs.developer_availability.items() if available)

    step_obs = env.step(
        PMAction(
            action_type="request_help",
            task_id=unblocked_task.task_id,
            helper_developer_id=helper_id,
        )
    )

    assert any("invalid:" in entry for entry in step_obs.event_log)

    helper = next(dev for dev in env._state.developers if dev.developer_id == helper_id)
    assert helper.available is True


def test_reward_and_grader_bounds() -> None:
    env = OpenPMEnvironment()
    obs = env.reset(task_id="hard", seed=42)

    assert 0.0 <= grade_for_task("hard", env.state) <= 1.0

    for _ in range(12):
        obs = env.step(PMAction(action_type="delay_task", task_id=obs.active_tasks[0].task_id))
        if getattr(obs, "done", False):
            break

    assert 0.0 <= obs.score <= 1.0
    assert 0.0 <= grade_for_task(obs.scenario_id, env.state) <= 1.0


def _run_advanced_episode(task_id: str, seed: int, max_steps: int = 30) -> float:
    env = OpenPMEnvironment()
    agent = AdvancedRuleBasedAgent()
    obs = env.reset(task_id=task_id, seed=seed)

    for _ in range(max_steps):
        if getattr(obs, "done", False):
            break
        obs = env.step(agent.step(obs))

    return obs.score


@pytest.mark.parametrize("task_id", ["easy", "medium", "hard"])
@pytest.mark.parametrize("seed", [42, 123, 999])
def test_advanced_agent_is_deterministic(task_id: str, seed: int) -> None:
    scores = [_run_advanced_episode(task_id, seed) for _ in range(5)]

    assert len(set(scores)) == 1
    assert statistics.pvariance(scores) == 0.0
