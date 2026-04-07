from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Dict, List, Type

from openpm_env.agents.baselines import AdvancedRuleBasedAgent, GreedyAgent, RandomAgent
from openpm_env.env import OpenPMEnvironment

TASKS = ["easy", "medium", "hard"]
SEEDS = [42, 123, 999]
OUTPUT_PATH = Path("eval_results.json")


def run_agent(agent_cls: Type, task_id: str, seed: int, max_steps: int = 30) -> float:
    env = OpenPMEnvironment()
    agent = agent_cls()
    obs = env.reset(task_id=task_id, seed=seed)

    for _ in range(max_steps):
        if getattr(obs, "done", False):
            break
        obs = env.step(agent.step(obs))

    return float(obs.score)


def main() -> None:
    results: Dict[str, Dict[str, Dict[int, List[float]] | Dict[str, float]]] = {
        "reproducibility": {},
        "comparison": {},
    }

    print("Running reproducibility check")
    for task_id in TASKS:
        task_results: Dict[int, List[float]] = {}
        for seed in SEEDS:
            scores = [round(run_agent(AdvancedRuleBasedAgent, task_id, seed), 4) for _ in range(5)]
            variance = statistics.pvariance(scores)
            assert variance == 0.0, f"Determinism failed for {task_id} seed {seed}"
            task_results[seed] = scores
            print(f"task={task_id} seed={seed} scores={scores} variance={variance:.4f}")
        results["reproducibility"][task_id] = task_results

    print("Running agent comparison check")
    agents = {
        "RandomAgent": RandomAgent,
        "GreedyAgent": GreedyAgent,
        "AdvancedRuleBasedAgent": AdvancedRuleBasedAgent,
    }
    for agent_name, agent_cls in agents.items():
        agent_results: Dict[str, float] = {}
        for task_id in TASKS:
            score = round(run_agent(agent_cls, task_id, seed=42), 4)
            agent_results[task_id] = score
            print(f"agent={agent_name} task={task_id} score={score:.4f}")
        results["comparison"][agent_name] = agent_results

    OUTPUT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"wrote={OUTPUT_PATH}")


if __name__ == "__main__":
    main()
