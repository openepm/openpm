# OpenPM Hackathon Round 1 Submission Checklist

**Project**: OpenPM — Deterministic Project Management RL Environment  
**Repository**: https://github.com/openepm/openpm.git  
**Status**: Ready for Hugging Face Spaces Deployment  
**Date**: March 31, 2026

---

## ✅ Pre-Deployment Verification (Local)

### Required Artifacts
- ✅ **openenv.yaml** — Environment manifest with `spec_version: 1`, `runtime: fastapi`, `app: server.app:app`
- ✅ **Dockerfile** — Multi-stage build from openenv-base with proper PYTHONPATH and entry point
- ✅ **inference.py** — Root-level baseline inference script with auto-bootstrap and deterministic scoring
- ✅ **README.md** — Complete documentation with environment description, action/observation schemas, task details, baseline scores, and setup instructions
- ✅ **pyproject.toml** — Project metadata with dependencies (openenv-core>=0.2.2, fastapi, uvicorn, pydantic) and server entry point
- ✅ **uv.lock** — Deterministic dependency lockfile for reproducible builds

### Environment Package Structure
- ✅ **openpm_env/env.py** — Core environment logic with reset(), step(), state() lifecycle
- ✅ **openpm_env/models.py** — Typed Pydantic models: PMAction, PMObservation, PMState
- ✅ **openpm_env/reward.py** — Reward calculation with partial progress and penalties
- ✅ **openpm_env/graders.py** — Three task graders (easy, medium, hard) with [0.0, 1.0] bounded scoring
- ✅ **openpm_env/tasks/scenarios.py** — Three deterministic scenarios with fixed seeds
- ✅ **server/app.py** — FastAPI server entry point with create_app() factory and main() function

### Local Validation Gates
- ✅ **openenv validate** — CLI compliance check passes
- ✅ **Docker build** — Image builds successfully without errors
- ✅ **Reset endpoint** — Returns HTTP 200 with valid PMObservation
- ✅ **Inference execution** — Completes all three tasks with non-flat reproducible scores:
  - Easy: 1.0000
  - Medium: 0.2495
  - Hard: 0.4161
  - Aggregate: 0.5552
  - Runtime: ~6.2 seconds
- ✅ **Reproducibility** — Multiple runs produce identical scores with same seed
- ✅ **Infra constraints** — Completes well under 20-minute target, suitable for 2 vCPU/8 GB environment

### Git Sync Status
- ✅ **Remote sync** — All commits pushed to https://github.com/openepm/openpm.git
- ✅ **Branch**: `main`
- ✅ **Latest commit**: fe03c2a (Final README alignment verification)
- ✅ **Working directory**: Clean (all changes committed)

---

## 🚀 Deployment Steps (Execute These)

### Step 1: Authenticate with Hugging Face
```bash
pip install huggingface-hub
huggingface-cli login
# Paste your HF token when prompted
```

### Step 2: Deploy to Hugging Face Spaces
```bash
cd /path/to/openpm_project
openenv push --repo-id your-username/openpm
```

**Note**: If the command fails, try:
```bash
huggingface-cli repo create openpm --type space --space-sdk docker
openenv push --repo-id your-username/openpm
```

This will:
1. Create a new HF Space repository
2. Upload the entire project files
3. Build the Docker container on HF infrastructure
4. Start the environment server
5. Provide a public Space URL

### Step 3: Verify Space Health
Once deployment completes (~5–10 minutes), visit:
```
https://huggingface.co/spaces/your-username/openpm
```

Confirm:
- Space status shows **RUNNING** (not BUILDING or ERROR)
- Space API is accessible at the public URL

### Step 4: Manual Endpoint Test (Optional)
```bash
# Test the reset endpoint
curl -X POST https://huggingface.co/spaces/your-username/openpm/reset \
  -H "Content-Type: application/json"

# Should return HTTP 200 with a JSON observation object
```

---

## 📋 Final Submission

### What to Submit
1. **HF Space URL**: `https://huggingface.co/spaces/your-username/openpm`
2. **GitHub Repository URL**: `https://github.com/openepm/openpm.git`

### Submission Window
- **Opens**: March 28, 2026
- **Closes**: April 8, 2026 at 11:59 PM IST (strict deadline)
- **Team Lead Responsibility**: Only the team lead (Piyush Goel) can submit the final entry

### Submission Method
1. Log into the hackathon platform
2. Navigate to Round 1 submission form
3. Paste your HF Space URL in the designated field
4. Paste your GitHub repository URL
5. Click Submit

**⚠️ Important**: Submit at least 4 hours before the deadline to allow rollback time if needed.

---

## 🔍 Automated Judge Validation Flow

Judges will automatically check the following gates:

1. **HF Space Health**
   - Ping endpoint: GET `/` → should return 200
   - Reset endpoint: POST `/reset` → should return 200 + valid observation

2. **OpenEnv Compliance**
   - Command: `openenv validate http://your-space-url`
   - Expected: `Ready for multi-mode deployment`

3. **Docker Build**
   - Rebuild from submitted repo
   - Expected: Success (no errors)

4. **Baseline Reproducibility**
   - Run: `python inference.py`
   - Expected: Complete all three tasks, produce scores in [0.0, 1.0]

5. **Task Graders**
   - Verify three distinct graders (easy, medium, hard)
   - Expected: Non-constant, non-flat scores

---

## 🛠️ Rollback Plan (If Deployment Fails)

If there is a deployment issue once live, you can:

1. **Identify the issue** via Space logs (click "Show Logs" in HF Space UI)
2. **Fix locally** in the repo
3. **Commit and push** to GitHub
4. **Redeploy** via `openenv push --repo-id your-username/openpm`

HF Spaces will automatically rebuild and update.

---

## 📞 Debugging Reference

### Common Space Build Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: cannot import name` | Missing PYTHONPATH in Dockerfile | Check `ENV PYTHONPATH="/app/env:$PYTHONPATH"` in Dockerfile |
| `Docker build timeout` | Large dependencies or slow connection | Ensure requirements are minimal; use uv.lock for speed |
| `Connection refused on /reset` | Server not starting | Check Dockerfile CMD and app.py entry point |
| `WebSocket timeout during inference` | Long LLM inference | Already handled; WebSocket ping interval is tuned |

### Local Debugging Before Push

```bash
# Start server locally
cd /path/to/openpm_project
python -m uvicorn server.app:app --host 0.0.0.0 --port 8000

# In another terminal, test reset
curl -X POST http://localhost:8000/reset

# Run inference
python inference.py
```

---

## ✨ Success Criteria

Your submission is accepted if:

- ✅ HF Space deploys and responds to reset() with HTTP 200
- ✅ openenv validate passes
- ✅ Docker builds without errors
- ✅ inference.py runs and produces three non-flat, non-constant task scores in [0.0, 1.0]
- ✅ All files are present and accessible on GitHub
- ✅ README includes environment description, action/observation schemas, and baseline scores

---

## 📝 Notes

- **Team Composition**: Piyush Goel (Lead), Divyansh Jha (You)
- **Project Risk Level**: Low (all pre-checks pass locally)
- **Contingency**: HF Space deployment is automated; if it fails, fix is a simple git push + rebuild
- **Estimated Deployment Time**: 5–15 minutes from push to Space live

---

**Ready to submit? Execute the deployment steps above, then notify your team lead to finalize the hackathon platform submission.**
