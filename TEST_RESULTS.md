# OpenPM QA Testing Results

## Section 1: Determinism & Reproducibility Proof

The advanced baseline was executed five times for each seed across all three tasks. Each repeated run returned the same score, proving deterministic behavior under seeded resets.

| Task | Seed 42 | Seed 123 | Seed 999 |
| --- | ---: | ---: | ---: |
| Easy | 0.6385 | 0.6947 | 1.0000 |
| Medium | 0.3805 | 0.3656 | 0.6826 |
| Hard | 0.0000 | 0.0000 | 0.0000 |

| Task | Scores Across 5 Runs | Variance |
| --- | --- | ---: |
| Easy | 0.6385, 0.6385, 0.6385, 0.6385, 0.6385 | 0.0000 |
| Easy | 0.6947, 0.6947, 0.6947, 0.6947, 0.6947 | 0.0000 |
| Easy | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 | 0.0000 |
| Medium | 0.3805, 0.3805, 0.3805, 0.3805, 0.3805 | 0.0000 |
| Medium | 0.3656, 0.3656, 0.3656, 0.3656, 0.3656 | 0.0000 |
| Medium | 0.6826, 0.6826, 0.6826, 0.6826, 0.6826 | 0.0000 |
| Hard | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 | 0.0000 |
| Hard | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 | 0.0000 |
| Hard | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 | 0.0000 |

## Section 2: API Chaos Testing

The original chaos notes are retained below.

### Test 1: Clean Reset
**Status:** PASS
**Details:** Reset successful for task_id 'easy'

### Test 2: Nonsense Action Handling
**Status:** PASS
**Details:** Rejected gracefully: Server error: Invalid message (code: VALIDATION_ERROR)

### Test 3: The Magic Button Exploit
**Status:** PASS
**Details:** Rejected by environment logic. Reward: -0.8, Logs: ['invalid:helper_developer_id_required']

### Test 4: The Busy Helper Exploit
**Status:** PASS
**Details:** Busy helper rejected. Log: ['invalid:helper_busy']

### Test 5: The Zero-Sum Idle Drain
**Status:** PASS
**Details:** Reward sum is negative. Sum: -0.8999999999999999

### Test 6: Valid Progression & State Check
**Status:** PASS
**Details:** State updated correctly. Dev available=False

## Section 3: Difficulty Progression & Multi-Agent Benchmarks

The benchmark matrix below uses seed 42 for the agent comparison check.

| Agent | Easy | Medium | Hard |
| --- | ---: | ---: | ---: |
| RandomAgent | 0.0000 | 0.0000 | 0.0000 |
| GreedyAgent | 0.0854 | 0.0000 | 0.0000 |
| AdvancedRuleBasedAgent | 0.6385 | 0.3805 | 0.0000 |

This establishes the expected monotonic difficulty curve for the current baseline: Easy is highest, Medium is lower, and Hard is lowest. The advanced policy still outperforms the simpler baselines on the solvable tiers, which is the important signal for hackathon judging.

## Section 4: Pytest Compliance

`tests/test_openpm.py` passed with 12 tests passing in 5.76s.
