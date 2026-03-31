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

State and observation include

- active tasks with status, effort, dependencies, deadline
- developer availability and skill profile
- blocked tasks
- sprint progress, risk level, time remaining

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

Expected infra envelope

- inference runtime target: under 20 minutes
- machine target: 2 vCPU, 8 GB RAM
