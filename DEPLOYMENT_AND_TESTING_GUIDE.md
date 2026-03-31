# OpenPM Hugging Face Deployment & Testing Guide

## Step 1: Generate a Fresh HF Token (SECURITY CRITICAL)

**Your previous token was rejected.** Follow these steps to create a new one:

1. Go to https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Set name: `openpm-hackathon-deploy`
4. Set permission: **Write** (to create and push repos)
5. Click **"Create token"**
6. **Copy the token immediately** — you won't see it again
7. **IMPORTANT: Do NOT paste it in chat or commit it to git**

---

## Step 2: Authenticate Locally (Keep Token Private)

Run this command **on your local machine** in PowerShell or Terminal:

```bash
cd c:\Users\divya\Desktop\OpenEnv\openpm_project

python -c "from huggingface_hub import login; login(token='YOUR_NEW_TOKEN_HERE', add_to_git_credential=True); print('✓ HF authentication successful')"
```

**Replace `YOUR_NEW_TOKEN_HERE`** with your actual token.

Expected output:

```
✓ HF authentication successful
```

---

## Step 3: Deploy to Hugging Face Spaces

Run this command in your project directory:

```bash
cd c:\Users\divya\Desktop\OpenEnv\openpm_project

openenv push --repo-id your-username/openpm
```

**Replace `your-username`** with your actual HF username.

### What happens:

1. OpenEnv CLI creates a new Space repository on HF
2. Uploads your entire project code
3. Triggers Docker build on HF infrastructure
4. Deploys the environment server
5. Provides you with a public Space URL

### Expected output:

```
✓ Space created: https://huggingface.co/spaces/your-username/openpm
✓ Repository pushed successfully
✓ Docker build started...
```

Keep this URL safe — you'll submit it to the hackathon platform.

---

## Step 4: Monitor the Build (5–15 minutes)

1. Visit your Space URL: `https://huggingface.co/spaces/your-username/openpm`
2. Check the **Logs** tab to watch the Docker build
3. Wait for status to change from **BUILDING** → **RUNNING**

### If build fails:

- Check logs for errors (usually dependency or Docker syntax issues)
- Fix locally: `docker build -f Dockerfile .`
- Push again: `openenv push --repo-id your-username/openpm`

### If build succeeds:

- Status will show **RUNNING** in green
- Your Space is now live and public

---

## Step 5: Test Your Deployment (After Space is RUNNING)

### Test 1: Reset Endpoint (HTTP 200 Check)

```bash
curl -X POST "https://huggingface.co/spaces/your-username/openpm/call/reset" \
  -H "Content-Type: application/json" \
  -d "{}" \
  -w "\nHTTP Status: %{http_code}\n"
```

**Expected output:**

```
HTTP Status: 200
{...observation data...}
```

### Test 2: Verify Inference Works

Once Space is running, test the baseline:

```bash
cd c:\Users\divya\Desktop\OpenEnv\openpm_project

python inference.py
```

**Expected output:**

```
Running inference on 3 tasks...
  Easy task: score = 1.0000
  Medium task: score = 0.2495
  Hard task: score = 0.4161
  Aggregate: 0.5552
  Total time: ~6 seconds
```

### Test 3: Manual Step Interaction (Browser)

1. Visit your Space URL
2. Click the **"API"** tab
3. You should see interactive API endpoints:
   - `/reset`
   - `/step`
   - `/state`
4. Click each endpoint to test live calls

---

## Step 6: Verify Compliance (Before Final Submission)

Run this checklist locally:

```bash
cd c:\Users\divya\Desktop\OpenEnv\openpm_project

# 1. Validate OpenEnv spec
python -m openenv.cli validate

# 2. Test Docker build
docker build -f Dockerfile . --tag openpm-test

# 3. Test reset endpoint
curl -X POST "http://localhost:8000/reset" -H "Content-Type: application/json" -d "{}" -w "\nHTTP: %{http_code}\n"

# 4. Test inference
python inference.py
```

**All must return success.**

---

## Step 7: Final Submission (Team Lead Only)

Once your Space is RUNNING and all tests pass:

1. **Copy your Space URL**: `https://huggingface.co/spaces/your-username/openpm`
2. **Go to hackathon platform**: [Scaler OpenEnv Hackathon](https://scaler.com/topics/hackathon/openenv)
3. **Click "Submit Assessment"**
4. **Paste your Space URL**
5. **Submit before Apr 8, 11:59 PM IST**

---

## Troubleshooting

### Build stuck in BUILDING state (>30 min)

- Likely Docker timeout
- Check logs for errors
- Try: `openenv push --repo-id your-username/openpm --force`

### Reset endpoint returns 500 error

- Check Space logs for Python errors
- Likely missing dependency or import error
- Fix locally, push again

### Inference produces flat scores (all 0.0)

- Space might not be starting correctly
- Check if server process is running: visit Space URL in browser
- If blank page, server didn't start — check logs

### Token still invalid

- Token may have been auto-revoked by HF
- Generate a fresh one at https://huggingface.co/settings/tokens
- Ensure it has **Write** permission

---

## Quick Reference: Key Dates & Constraints

| Item                    | Value                       |
| ----------------------- | --------------------------- |
| **Submission Deadline** | Apr 8, 2026, 11:59 PM IST   |
| **Runtime Limit**       | < 20 minutes                |
| **Memory Limit**        | 8 GB RAM                    |
| **vCPU Limit**          | 2 vCPU                      |
| **Required Endpoints**  | `/reset`, `/step`, `/state` |
| **Baseline Script**     | `inference.py` in root      |

---

## What Judges Will Automatically Check

1. ✅ HF Space deploys (Docker build succeeds)
2. ✅ Reset endpoint responds with HTTP 200
3. ✅ `inference.py` runs without error
4. ✅ Produces 3 task scores in [0.0, 1.0]
5. ✅ Runtime completes in < 20 minutes
6. ✅ `openenv validate` passes

**All must pass or your submission is disqualified.**

---

## Questions?

- **OpenEnv CLI issues**: Check [docs/cli.md](../openenv_source/docs/cli.md)
- **Dockerfile problems**: Check [docs/environment-builder.md](../openenv_source/docs/environment-builder.md)
- **HF Space issues**: Check [huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)
- **Token problems**: Visit [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

Good luck! 🚀
