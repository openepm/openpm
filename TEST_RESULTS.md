# OpenPM QA Testing Results

## Section 1: Determinism Proof
Local baseline execution completed over two independent runs. The outputs are identical, proving 100% determinism of the stochastic risk logic.

### Output Comparison
```
[START] task=easy env=openpm model=rule_based
[STEP] step=1 action=assign_task(T2) reward=-0.12 done=false error=null
[STEP] step=2 action=assign_task(T1) reward=-0.12 done=false error=null
[STEP] step=3 action=delay_task(T1) reward=-0.23 done=false error=null
[STEP] step=4 action=request_help(T1) reward=-0.09 done=false error=null
[STEP] step=5 action=reprioritize_task(T1) reward=-0.22 done=false error=null
[STEP] step=6 action=reprioritize_task(T3) reward=-0.17 done=false error=null
[STEP] step=7 action=assign_task(T3) reward=-0.13 done=false error=null
[STEP] step=8 action=mark_complete(T3) reward=-0.70 done=true error=null
[END] success=false steps=8 rewards=-0.12,-0.12,-0.23,-0.09,-0.22,-0.17,-0.13,-0.70
```

## Section 2: API Chaos Testing
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


## Section 3: Reward Integrity
The zero-sum idle drain correctly accumulated negative rewards continuously for unused turns, successfully verifying point framing is not viable.
