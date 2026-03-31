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

OpenPM: Project Management RL Environment

OpenPM simulates a realistic software sprint where an agent acts as a project manager and makes scheduling and delivery decisions. The environment is deterministic and designed for robust evaluation.

Real-world objective

- Deliver a sprint by managing tasks, dependencies, blockers, and developer capacity under deadlines.

OpenEnv compliance

- step(action)
- reset(task_id=easy|medium|hard)
- state()
- Typed models for action, observation, state
- openenv.yaml included

Action space

- assign_task(task_id, developer_id)
- reprioritize_task(task_id, priority)
- split_task(task_id)
- request_help(task_id)
- delay_task(task_id)
- mark_complete(task_id)

Action schema (PMAction)

| Field        | Type | Required    | Notes                                                                                       |
| ------------ | ---- | ----------- | ------------------------------------------------------------------------------------------- |
| action_type  | str  | yes         | One of: assign_task, reprioritize_task, split_task, request_help, delay_task, mark_complete |
| task_id      | str  | conditional | Required for all task-specific actions                                                      |
| developer_id | str  | conditional | Required for assign_task                                                                    |
| priority     | str  | conditional | Required for reprioritize_task; one of low, medium, high, critical                          |

State and observation include

- active tasks with status, effort, dependencies, deadline
- developer availability and skill profile
- blocked tasks
- sprint progress, risk level, time remaining

Observation schema (PMObservation)

| Field                  | Type                        | Notes                                                                       |
| ---------------------- | --------------------------- | --------------------------------------------------------------------------- |
| day                    | int                         | Current sprint day                                                          |
| total_days             | int                         | Sprint horizon for active task                                              |
| active_tasks           | list[TaskSnapshot]          | Per-task status, assignment, priority, dependencies, due day, blocker flags |
| task_priorities        | dict[str, str]              | Current priority by task_id                                                 |
| deadlines              | dict[str, int]              | Due day by task_id                                                          |
| developer_availability | dict[str, bool]             | Availability state per developer                                            |
| developer_skill_levels | dict[str, dict[str, float]] | Skill matrix by developer and domain                                        |
| blocked_tasks          | list[str]                   | Task IDs currently blocked                                                  |
| sprint_progress        | float                       | Fraction of total effort completed                                          |
| risk_level             | float                       | Normalized project risk estimate                                            |
| time_remaining         | int                         | Remaining days in sprint                                                    |

Tasks and graders

- easy: small sprint with clear priorities
- medium: dependency-heavy sprint with limited developers
- hard: dynamic blocker injections and deadline pressure
- deterministic grader scores in [0.0, 1.0]

Reward logic

- positive for progress, good prioritization, and blocker resolution
- penalties for invalid actions, idle developers, and overdue work
- terminal bonus for successful sprint completion

Quick start

1. Install dependencies
   uv sync
2. Run server
   uv run server
3. Run baseline inference
   python inference.py

Inference robustness

- `inference.py` first tries to connect to `OPENPM_BASE_URL` (default `http://localhost:8000`).
- If unreachable and base URL is local (`localhost`/`127.0.0.1`), it auto-starts `uvicorn` and retries.
- For remote endpoints, it fails fast with a clear error message.

Optional OpenAI baseline path

- Set OPENPM_USE_OPENAI=1
- Set API_BASE_URL
- Set MODEL_NAME
- Set HF_TOKEN or OPENAI_API_KEY

Validation and deployment

1. Validate
   openenv validate
2. Build Docker
   docker build -t openpm-env:latest .
3. Push
   openenv push --repo-id <username>/openpm-env

Baseline results (reference run)

The deterministic rule-based baseline produces reproducible non-flat scores across all required tasks.

| Task      | Score  |
| --------- | ------ |
| easy      | 1.0000 |
| medium    | 0.2495 |
| hard      | 0.4161 |
| aggregate | 0.5552 |

Reference runtime: approximately 6-10 seconds on a local dev machine, well within the 20-minute submission constraint.

Expected infra envelope

- inference runtime target: under 20 minutes
- machine target: 2 vCPU, 8 GB RAM
