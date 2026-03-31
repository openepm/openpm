---
title: OpenPM Environment
emoji: 📈
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
app_port: 8000
base_path: /web
tags:
  - openenv
---

# OpenPM: Project Management RL Environment

OpenPM is a deterministic, real-world OpenEnv environment that simulates a software sprint. An agent plays the role of a project manager and must deliver work under constraints: dependencies, blockers, deadlines, developer availability, and skill fit.

This environment is designed for evaluation first: reproducible transitions, typed interfaces, automated graders, and clear reward shaping.

## What This Project Is

OpenPM models a sprint as a decision process where each step is one management action.

Goal:

- Maximize sprint completion quality while minimizing delays, invalid actions, and avoidable risk.

Why it is realistic:

- Task dependencies can block execution.
- Developers have domain-specific skill levels.
- Prioritization and assignment decisions directly affect throughput.
- Hard mode introduces dynamic blockers and deadline pressure.

## OpenEnv Compliance

The environment follows OpenEnv requirements:

- `reset(task_id=...)`
- `step(action)`
- `state()`
- Typed Pydantic models for Action, Observation, and State
- `openenv.yaml` manifest for validation/deployment

## Environment Lifecycle

1. Call `reset(task_id="easy" | "medium" | "hard")` to start a deterministic scenario.
2. Call `step(action)` repeatedly.
3. Read reward and done flag after each step.
4. Call `state()` to inspect full episode state and metadata.
5. Episode ends on completion or horizon exhaustion.

## Action Space

- `assign_task(task_id, developer_id)`
- `reprioritize_task(task_id, priority)`
- `split_task(task_id)`
- `request_help(task_id)`
- `delay_task(task_id)`
- `mark_complete(task_id)`

### Action Schema (`PMAction`)

| Field          | Type  | Required    | Notes                                                                                                  |
| -------------- | ----- | ----------- | ------------------------------------------------------------------------------------------------------ |
| `action_type`  | `str` | yes         | One of `assign_task`, `reprioritize_task`, `split_task`, `request_help`, `delay_task`, `mark_complete` |
| `task_id`      | `str` | conditional | Required for task-specific actions                                                                     |
| `developer_id` | `str` | conditional | Required for `assign_task`                                                                             |
| `priority`     | `str` | conditional | Required for `reprioritize_task`; one of `low`, `medium`, `high`, `critical`                           |

## Observation and State

Each step returns a rich observation with sprint progress, risks, and task/developer status.

### Observation Schema (`PMObservation`)

| Field                    | Type                          | Notes                                                             |
| ------------------------ | ----------------------------- | ----------------------------------------------------------------- |
| `day`                    | `int`                         | Current sprint day                                                |
| `total_days`             | `int`                         | Sprint horizon for active scenario                                |
| `active_tasks`           | `list[TaskSnapshot]`          | Per-task status, assignment, effort, deps, due day, blocker flags |
| `task_priorities`        | `dict[str, str]`              | Priority map by task id                                           |
| `deadlines`              | `dict[str, int]`              | Due-day map by task id                                            |
| `developer_availability` | `dict[str, bool]`             | Availability by developer                                         |
| `developer_skill_levels` | `dict[str, dict[str, float]]` | Skill matrix by developer/domain                                  |
| `blocked_tasks`          | `list[str]`                   | Currently blocked task ids                                        |
| `sprint_progress`        | `float`                       | Fraction of total effort completed                                |
| `risk_level`             | `float`                       | Normalized sprint risk estimate                                   |
| `time_remaining`         | `int`                         | Remaining days in sprint                                          |

## Reward Design

Reward includes partial progress signals across the whole trajectory:

- Positive signals for progress and high-quality decisions.
- Penalties for invalid actions, idle capacity, and overdue work.
- Terminal bonus for successful delivery.

## Tasks and Graders

OpenPM provides three deterministic tasks with graders returning scores in `[0.0, 1.0]`:

- `easy`: small sprint, clear priorities
- `medium`: dependency-heavy sprint with constrained developers
- `hard`: dynamic blocker injections with tight deadlines

## Quick Start (Local)

```bash
uv sync
uv run server
```

In another terminal:

```bash
python inference.py
```

## Use from Python

### Connect to deployed Space

```python
from openpm_env import OpenPMEnv, PMAction

with OpenPMEnv.from_env("divyanshjha/openpm").sync() as env:
    result = env.reset(task_id="easy")
    result = env.step(PMAction(action_type="assign_task", task_id="T1", developer_id="D1"))
    print(result.reward, result.done)
```

### Connect to local server directly

```python
from openpm_env import OpenPMEnv, PMAction

with OpenPMEnv(base_url="http://localhost:8000").sync() as env:
    env.reset(task_id="easy")
    env.step(PMAction(action_type="assign_task", task_id="T1", developer_id="D1"))
```

## Test on Hugging Face Frontend

Open the Space app and use the Playground form:

1. Click `Reset`.
2. Select `Action Type` = `assign_task`.
3. Enter `Task Id` = `T1`.
4. Enter `Developer Id` = `D1`.
5. Click `Step`.
6. Click `Get state` to verify state transition.

Tip:

- If you see a validation error, verify required fields for the selected action are provided.

## Test via API (curl)

Use the Space subdomain endpoint:

```bash
curl -X POST "https://divyanshjha-openpm.hf.space/reset" -H "Content-Type: application/json" -d "{}"
curl -X GET "https://divyanshjha-openpm.hf.space/state"
curl -X POST "https://divyanshjha-openpm.hf.space/step" -H "Content-Type: application/json" -d '{"action":{"action_type":"assign_task","task_id":"T1","developer_id":"D1"}}'
```

Important:

- `/step` expects payload shape `{"action": { ... }}`. Sending raw action fields at top level returns HTTP 422.

## Inference Modes

Default mode is deterministic rule-based baseline.

Optional OpenAI mode:

- `OPENPM_USE_OPENAI=1`
- `API_BASE_URL=<llm-endpoint>`
- `MODEL_NAME=<model-id>`
- `HF_TOKEN` or `OPENAI_API_KEY`

Robustness behavior:

- `inference.py` first tries `OPENPM_BASE_URL` (default `http://localhost:8000`).
- If endpoint is local and unavailable, it auto-starts local uvicorn and retries.
- For unreachable remote endpoints, it fails fast with a clear error.

## Validation and Deployment

```bash
openenv validate
docker build -t openpm-env:latest .
openenv push --repo-id divyanshjha/openpm
```

## Baseline Results (Reference)

| Task      | Score  |
| --------- | ------ |
| easy      | 1.0000 |
| medium    | 0.2495 |
| hard      | 0.4161 |
| aggregate | 0.5552 |

Typical runtime:

- ~6-15 seconds in standard runs, far below the 20-minute constraint.

Target infra envelope:

- 2 vCPU
- 8 GB RAM

## Troubleshooting

### HTTP 422 on `/step`

Cause:

- Wrong JSON body shape.

Fix:

- Send `{"action": {...}}` wrapper, not flat fields.

### Space is up but command fails

Cause:

- Using Hugging Face repository URL instead of Space subdomain API URL.

Fix:

- Use `https://<owner>-<space>.hf.space` for API calls.

### OpenEnv push complains about missing `__init__.py`

Cause:

- Running push from wrong directory layout.

Fix:

- Run from project root and keep package/init files present.
