# ⚡ QUICK START - PowerShell Commands

## 📍 YOUR LOCATION
```
PS \\wsl.localhost\Ubuntu\home\shafqatsarwar\Projects\2nd_hackathon-phase1-4>
```
✅ **Stay here for all commands below!**

---

## 🎯 COPY & PASTE THESE COMMANDS (IN ORDER)

### 1️⃣ Build Backend (2-3 minutes)
```powershell
docker build -f Dockerfile.backend -t todo-backend:latest .
```
**Wait for:** `Successfully tagged todo-backend:latest`

---

### 2️⃣ Build Frontend (3-5 minutes)
```powershell
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```
**Wait for:** `Successfully tagged todo-frontend:latest`

---

### 3️⃣ Check Images
```powershell
docker images
```
**Look for:** `todo-backend` and `todo-frontend` in the list

---

### 4️⃣ Check if .env Exists
```powershell
Test-Path .env
```
**If False, run 4a. If True, skip to step 5.**

---

### 4️⃣a Create .env File (only if needed)
```powershell
@"
DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db
BETTER_AUTH_SECRET=change-this-secret-in-production
OPENAI_API_KEY=your-openai-api-key-here
GITHUB_TOKEN=optional
GITHUB_OWNER=your-username
GITHUB_REPO=your-repo
"@ | Out-File -FilePath .env -Encoding utf8
```

---

### 5️⃣ Edit .env with Your API Key
```powershell
notepad .env
```
**Change:** `OPENAI_API_KEY=your-openai-api-key-here`  
**To:** `OPENAI_API_KEY=sk-proj-YOUR-ACTUAL-KEY`  
**Save and close Notepad**

---

### 6️⃣ Verify .env
```powershell
Get-Content .env
```
**Check:** OPENAI_API_KEY should have your real key

---

### 7️⃣ Start All Services
```powershell
docker-compose up -d
```
**Wait for:** All services created

---

### 8️⃣ Check Status
```powershell
docker-compose ps
```
**All should show:** `Up`

---

### 9️⃣ Test Backend
```powershell
curl http://localhost:8000/health
```
**Expected:** `{"status":"healthy","database":"connected"}`

---

### 🔟 Open in Browser
```powershell
start http://localhost:3000
```
**Or manually open:** http://localhost:3000

---

## ✅ SUCCESS!

If all steps worked, you should see:
- ✅ Application running at http://localhost:3000
- ✅ Backend API at http://localhost:8000/docs
- ✅ Chat works without streaming errors

---

## 🛑 USEFUL COMMANDS

```powershell
# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Restart
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build
```

---

## 📖 FULL GUIDE

For detailed explanations, see: **POWERSHELL_DEPLOYMENT_GUIDE.md**

---

**START NOW:** Run command #1 above! ⬆️
