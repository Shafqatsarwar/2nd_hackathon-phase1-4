# 🔍 Troubleshooting: "Failed to parse stream string" Error

## What This Error Means

This error occurs when the chat tries to stream a response but the format is incompatible with the Vercel AI SDK.

## Most Common Causes

### 1. ❌ Backend is NOT Running
**Check**: Is the backend server running?
```bash
# Test if backend is accessible
curl http://localhost:8000/health

# Expected: {"status":"healthy","database":"connected"}
```

**If you get "Connection refused"**: Backend is not running!

**Solution**: Start the backend
```bash
uv run uvicorn src.backend.main:app --reload --port 8000
```

### 2. ❌ OPENAI_API_KEY Not Set
**Check**: Does backend have the OpenAI API key?
```bash
# Test OpenAI configuration
curl http://localhost:8000/health/openai
```

**If you see "OPENAI_API_KEY environment variable is not set"**:

**Solution**: Check `src/backend/.env.local` has:
```env
OPENAI_API_KEY=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
```

### 3. ❌ Backend Error in Processing
**Check**: Look at backend terminal for errors

**Common errors**:
- `ModuleNotFoundError: No module named 'openai'` → Run `uv sync`
- `Database connection failed` → Check `DATABASE_URL`
- `OpenAI API error` → Check API key is valid

## Quick Diagnostic Steps

### Step 1: Check Backend Status
```bash
# Is backend running?
curl http://localhost:8000/health

# Is OpenAI configured?
curl http://localhost:8000/health/openai
```

### Step 2: Check Frontend Environment
```bash
# Check if .env.local exists
ls -la src/frontend/.env.local

# Should contain:
# NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
```

### Step 3: Test Chat Endpoint Directly
```bash
# Test the chat endpoint
curl -X POST http://localhost:8000/api/admin/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer admin_token" \
  -d '{"message": "Hello", "conversation_id": null}'
```

**Expected**: Streaming response with AI text

**If you get error**: Check the error message for clues

## Solutions

### Solution 1: Backend Not Running
```bash
# Terminal 1 - Start Backend
cd ~/Projects/2nd_hackathon-phase1-4
uv run uvicorn src.backend.main:app --reload --port 8000
```

### Solution 2: Missing Environment Variables
```bash
# Create backend .env.local if missing
cd ~/Projects/2nd_hackathon-phase1-4
./setup-env.sh
```

### Solution 3: Reinstall Dependencies
```bash
# Backend dependencies
uv sync --reinstall

# Frontend dependencies
cd src/frontend
rm -rf node_modules package-lock.json
npm install
cd ../..
```

### Solution 4: Restart Both Servers
```bash
# Stop both servers (Ctrl+C in each terminal)

# Terminal 1 - Backend
uv run uvicorn src.backend.main:app --reload --port 8000

# Terminal 2 - Frontend
npm run dev --workspace=src/frontend
```

## Expected Working State

### Backend Terminal Should Show:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
✅ Admin user seeded: khansarwar1@hotmail.com
✅ Chat router successfully included
INFO:     Application startup complete.
```

### Frontend Terminal Should Show:
```
▲ Next.js 15.5.9
- Local:        http://localhost:3000

✓ Ready in 2.5s
```

### Browser Console Should Show:
- No errors when loading /chat
- When sending message: Streaming response appears
- No "Failed to parse stream string" error

## Still Not Working?

### Check These:

1. **Port Conflicts**
   ```bash
   # Check if port 8000 is in use
   lsof -i :8000  # Linux/macOS
   netstat -ano | findstr :8000  # Windows
   ```

2. **Firewall/Antivirus**
   - Temporarily disable to test
   - Add exception for ports 3000 and 8000

3. **WSL Network Issues** (if using WSL)
   ```bash
   # Access from Windows using WSL IP
   wsl hostname -I
   # Use that IP instead of localhost
   ```

4. **Check Browser Console**
   - Open DevTools (F12)
   - Go to Network tab
   - Send a chat message
   - Look at the `/api/chat` request
   - Check the response

## Quick Test Script

Save this as `test-chat.sh`:
```bash
#!/bin/bash

echo "🔍 Testing Chat System..."
echo ""

echo "1. Testing Backend Health..."
curl -s http://localhost:8000/health || echo "❌ Backend not responding!"
echo ""

echo "2. Testing OpenAI Configuration..."
curl -s http://localhost:8000/health/openai || echo "❌ OpenAI check failed!"
echo ""

echo "3. Testing Chat Endpoint..."
curl -s -X POST http://localhost:8000/api/admin/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer admin_token" \
  -d '{"message": "test", "conversation_id": null}' \
  || echo "❌ Chat endpoint failed!"
echo ""

echo "✅ Tests complete!"
```

Run it:
```bash
chmod +x test-chat.sh
./test-chat.sh
```

---

**Most Likely Issue**: Backend is not running or OPENAI_API_KEY is not set.

**Quick Fix**:
1. Start backend: `uv run uvicorn src.backend.main:app --reload --port 8000`
2. Check it's running: `curl http://localhost:8000/health`
3. Refresh frontend and try chat again

🎯 **The error should disappear once backend is properly running with OpenAI API key configured!**
