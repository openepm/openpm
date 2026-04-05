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

<div align="center">
  <h1>OpenPM</h1>

  <p>
    <img src="https://img.shields.io/badge/OpenEnv-Compliant-success?style=for-the-badge&logo=shield" alt="OpenEnv Compliant" />
    <img src="https://img.shields.io/badge/Status-Live-22c55e?style=for-the-badge&logo=huggingface" alt="Status: Live" />
    <img src="https://img.shields.io/badge/License-MIT-0ea5e9?style=for-the-badge&logo=open-source-initiative" alt="License: MIT" />
    <a href="https://huggingface.co/spaces/piyushgoel2808/openpm">
      <img src="https://img.shields.io/badge/Play_on-Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="Play on Hugging Face" />
    </a>
  </p>

  <h3>An enterprise-grade, deterministic Reinforcement Learning environment simulating complex software sprints.</h3>
</div>

<div align="center">

[![Watch the Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://youtu.be/YOUR_VIDEO_ID)

</div>

---

## ⚡ Why OpenPM? (Not a Toy)

Most RL benchmarks focus on games or synthetic, low-stakes puzzles. OpenPM was explicitly built to fulfill the **Real-World Utility** requirement of the Meta/Hugging Face OpenEnv Hackathon by modeling the high-pressure environment of software engineering management.

- 🔗 **Dependency-Aware Planning:** Forces agents to orchestrate complex task graphs efficiently under tight delivery deadlines.
- ⚖️ **Strict Zero-Sum Rewards:** Agents are heavily penalized for invalid actions, resource idling, or ignoring blockers, requiring sophisticated prioritization instead of brute-force guessing.
- 🎲 **Seeded Stochastic Risk:** Production is chaotic. OpenPM injects 100% deterministic, seed-based chaotic task failures and blockers that pressure agents into reactive reassignment and active risk mitigation.

## 🚀 Quick Start & Live Demo

Try the interactive UI or deploy standard OpenEnv agents targeting the endpoint directly.

**Live Hugging Face Space:** [https://huggingface.co/spaces/piyushgoel2808/openpm](https://huggingface.co/spaces/piyushgoel2808/openpm)

### Python Client Integration

**Connect to the deployed Space via SDK:**
```python
from openpm_env import OpenPMEnv, PMAction

with OpenPMEnv.from_env("piyushgoel2808/openpm").sync() as env:
    result = env.reset(task_id="easy")
    
    # Assign Developer D1 to Task T1
    action = PMAction(action_type="assign_task", task_id="T1", developer_id="D1")
    result = env.step(action)
    
    print(f"Reward: {result.reward}, Done: {result.done}")
```

**Connect to a local server:**
```python
from openpm_env import OpenPMEnv, PMAction

with OpenPMEnv(base_url="http://localhost:8000").sync() as env:
    env.reset(task_id="hard")
    env.step(PMAction(action_type="assign_task", task_id="T2", developer_id="D2"))
```

## ⚙️ Core Mechanics (Schemas & Rules)

### Standard Action Space (`PMAction`)

Agents manage the project via rigorous constraints. Notice the newly nerfed `request_help` mechanism designed to drain resources symmetrically.

| Action Type | Required Target | Explanation |
| :--- | :--- | :--- |
| `assign_task` | `task_id`, `developer_id` | Allocate a developer whose skills optimally match the task domain. |
| `reprioritize_task`| `task_id`, `priority` | Shift priority (`low` to `critical`) to accelerate development speed. |
| `split_task` | `task_id` | Decompose high-effort workloads. |
| `request_help` | `task_id`, `helper_developer_id` | **NERFED:** Resolves a blocked task but *requires an available developer* to sacrifice their time. Effectively creates a resource trade-off instead of a "magic unblock button". |
| `delay_task` | `task_id` | Extend deadline (trading time for reduced blocker pressure). |
| `mark_complete` | `task_id` | Commit the finished code to deployment. Fails if effort remains. |

### Dense Observation Space (`PMObservation`)

The observation space strips away irrelevant noise to provide an information-dense snapshot strictly optimized for Large Language Model (LLM) context windows.

| Field | Type | Description |
| :--- | :--- | :--- |
| `day` / `total_days` | `int` | Current progress against the absolute project timeline. |
| `sprint_progress` | `float` | Effort completion ratio (`0.0` to `1.0`). |
| `active_tasks` | `List[TaskSnapshot]` | Aggregated states (id, due date, remaining effort, deps). |
| `blocked_tasks` | `List[str]` | IDs of tasks stuck waiting on dependencies or chaotic risks. |
| `developer_availability`| `Dict[str, bool]` | Real-time map tracking which developers can take immediate work. |
| `risk_level` | `float` | Synthesized system-wide hazard multiplier warning the agent. |

## 💸 The Zero-Sum Reward Engine

OpenPM utilizes an aggressive, zero-sum continuous reward matrix designed to deter brute forcing and reward hallucination. 

- **Progress Rewards:** Given for valid reduction in `task.effort_remaining` based on correct domain-matching.
- **Continuous Idle Penalties:** Agents bleed points for every turn there are unfinished tasks but unassigned developers. Every wasted dev cycle applies a recurring negative weight penalty.
- **Blocker & Invalid Action Penalties:** Massive scalar drains apply the moment the agent ignores blocked task thresholds or hallucinates incorrect `task_id` values.
- **Max Score Ceiling (Cap):** The absolute maximum grade achievable is mathematically bounded at `1.0`, ensuring fair LLM baseline rankings.

## 🛡️ Automated QA & Chaos Testing

OpenPM has undergone rigorous chaos testing (see `TEST_RESULTS.md`) and guarantees mathematical exploit-proof security against reinforcement hacking:

- ✅ **100% Deterministic Framework:** The seemingly random chaotic stochastic risks are fully seed-bound. Executing identical actions across independent local resets generated cryptographically identical execution trajectories. 
- ✅ **Magic Button Blocked:** Tested against the infamous "Magic Helper Exploit." Providing empty requests correctly dumps validation errors, while targeting busy helper devs triggers immediate validation failure without advancing state.
- ✅ **Zero-Sum Drainage Proven:** Long-term idle actions securely collapse to deeply negative trailing rewards (`-0.899`), preventing agents from gaming duration.

## 📊 Baseline Performance & Benchmarks

Baseline metrics represent the deterministic Rule-Based internal solver agent performance across the three core difficulties:

| Task Preset | Rule-Based AI Score |
| :--- | :--- |
| **Easy** | 1.0000 |
| **Medium** | 0.2495 |
| **Hard** | 0.4161 |

> [!NOTE]
> ### 🤖 LLM Benchmarks (Coming Soon)
> Full integration tracking zero-shot GPT-4, Llama 3, and Claude 3 Opus agents attempting the OpenPM Environment will be logged to the official Hugging Face Hub Leaderboard.
