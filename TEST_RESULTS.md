# OpenPM QA Testing Results

## Section 1: Determinism & Reproducibility Proof

The advanced baseline was executed five times for each seed across all three tasks. Each repeated run returned the same score, proving deterministic behavior under seeded resets.

| Task | Seed 42 | Seed 123 | Seed 999 |
| --- | ---: | ---: | ---: |
| Easy | 1.0000 | 1.0000 | 1.0000 |
| Medium | 0.5900 | 0.5136 | 0.6011 |
| Hard | 0.0000 | 0.0000 | 0.0000 |

| Task | Scores Across 5 Runs | Variance |
| --- | --- | ---: |
| Easy (Seed 42) | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 | 0.0000 |
| Easy (Seed 123) | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 | 0.0000 |
| Easy (Seed 999) | 1.0000, 1.0000, 1.0000, 1.0000, 1.0000 | 0.0000 |
| Medium (Seed 42) | 0.5900, 0.5900, 0.5900, 0.5900, 0.5900 | 0.0000 |
| Medium (Seed 123) | 0.5136, 0.5136, 0.5136, 0.5136, 0.5136 | 0.0000 |
| Medium (Seed 999) | 0.6011, 0.6011, 0.6011, 0.6011, 0.6011 | 0.0000 |
| Hard (Seed 42) | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 | 0.0000 |
| Hard (Seed 123) | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 | 0.0000 |
| Hard (Seed 999) | 0.0000, 0.0000, 0.0000, 0.0000, 0.0000 | 0.0000 |

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
| RandomAgent | 0.0767 | 0.0000 | 0.0000 |
| GreedyAgent | 0.0874 | 0.0000 | 0.0000 |
| AdvancedRuleBasedAgent | 1.0000 | 0.5900 | 0.0000 |

This establishes a globally stable difficulty curve across all tested seeds: Easy > Medium > Hard. The advanced policy still outperforms the simpler baselines while preserving deterministic seed behavior.

## Section 4: Pytest Compliance

`tests/test_openpm.py` passed with 13 tests passing in 5.80s.
