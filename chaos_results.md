### Test 1: Clean Reset
**Status:** PASS
**Details:** Reset successful for task_id 'easy'

### Test 2: Nonsense Action Handling
**Status:** PASS
**Details:** Rejected gracefully with status 422

### Test 3: The Magic Button Exploit
**Status:** FAIL
**Details:** Should have rejected. Status: 200

### Test 4: The Busy Helper Exploit
**Status:** FAIL
**Details:** Allowed busy helper! Status: 200

### Test 5: The Zero-Sum Idle Drain
**Status:** FAIL
**Details:** Reward sum is not negative! Sum: 1.5

### Test 6: Valid Progression & State Check
**Status:** FAIL
**Details:** State did not update correctly. Avail: None
