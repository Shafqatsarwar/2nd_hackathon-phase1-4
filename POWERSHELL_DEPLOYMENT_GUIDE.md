# 🚀 PowerShell Deployment Guide - Step by Step

## ✅ Prerequisites Checklist

Before starting, verify:
- [x] Docker installed and in PATH
- [x] PowerShell open in project directory
- [x] Current directory: `\\wsl.localhost\Ubuntu\home\shafqatsarwar\Projects\2nd_hackathon-phase1-4`

---

## 📍 WHERE TO RUN COMMANDS

All commands in this guide should be run in **PowerShell** (the terminal you're currently in).

**Your current location:**
```
PS \\wsl.localhost\Ubuntu\home\shafqatsarwar\Projects\2nd_hackathon-phase1-4>
```

✅ **This is correct!** Stay in this directory for all commands below.

---

## 🎯 STEP-BY-STEP DEPLOYMENT

### **STEP 1: Verify Docker is Working**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
docker --version
```

**EXPECTED OUTPUT:**
```
Docker version 27.3.1, build ce12230
```

✅ **STATUS:** You already confirmed this works!

---

### **STEP 2: Build Backend Docker Image**

**WHERE:** PowerShell  
**TIME:** ~2-3 minutes  
**COMMAND:**
```powershell
docker build -f Dockerfile.backend -t todo-backend:latest .
```

**WHAT THIS DOES:**
- Reads `Dockerfile.backend`
- Installs Python 3.12
- Installs dependencies from `requirements.txt`
- Copies backend code
- Creates Docker image named `todo-backend:latest`

**EXPECTED OUTPUT (at the end):**
```
Successfully built <some-hash>
Successfully tagged todo-backend:latest
```

**IF YOU SEE ERRORS:**
- Check that `Dockerfile.backend` exists
- Check that `requirements.txt` has content
- Make sure you have internet connection

**RUN THIS NOW ⬇️**

---

### **STEP 3: Build Frontend Docker Image**

**WHERE:** PowerShell  
**TIME:** ~3-5 minutes  
**COMMAND:**
```powershell
docker build -f Dockerfile.frontend -t todo-frontend:latest .
```

**WHAT THIS DOES:**
- Reads `Dockerfile.frontend`
- Installs Node.js 18
- Installs npm dependencies
- Builds Next.js application
- Creates Docker image named `todo-frontend:latest`

**EXPECTED OUTPUT (at the end):**
```
Successfully built <some-hash>
Successfully tagged todo-frontend:latest
```

**RUN THIS AFTER STEP 2 COMPLETES ⬇️**

---

### **STEP 4: Verify Images Were Created**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
docker images
```

**EXPECTED OUTPUT:**
```
REPOSITORY        TAG       IMAGE ID       CREATED          SIZE
todo-frontend     latest    <id>           <time>           <size>
todo-backend      latest    <id>           <time>           <size>
```

You should see both `todo-backend` and `todo-frontend` in the list.

**RUN THIS TO CONFIRM ⬇️**

---

### **STEP 5: Check if .env File Exists**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
Test-Path .env
```

**EXPECTED OUTPUT:**
- `True` = File exists (go to Step 6)
- `False` = File doesn't exist (create it in Step 5a)

**RUN THIS NOW ⬇️**

---

### **STEP 5a: Create .env File (if it doesn't exist)**

**WHERE:** PowerShell  
**COMMAND:**
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

**WHAT THIS DOES:**
- Creates a new `.env` file
- Adds default configuration

**RUN THIS IF STEP 5 RETURNED FALSE ⬇️**

---

### **STEP 6: Edit .env File with Your API Key**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
notepad .env
```

**OR if you have VS Code:**
```powershell
code .env
```

**WHAT TO DO:**
1. File will open in Notepad/VS Code
2. Find the line: `OPENAI_API_KEY=your-openai-api-key-here`
3. Replace `your-openai-api-key-here` with your actual OpenAI API key
4. It should look like: `OPENAI_API_KEY=sk-proj-...`
5. Save the file (Ctrl+S)
6. Close Notepad/VS Code

**⚠️ CRITICAL:** Without a valid OPENAI_API_KEY, the chat feature won't work!

**RUN THIS NOW AND EDIT THE FILE ⬇️**

---

### **STEP 7: Verify .env File Contents**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
Get-Content .env
```

**EXPECTED OUTPUT:**
```
DATABASE_URL=postgresql://postgres:postgres@db:5432/todo_db
BETTER_AUTH_SECRET=change-this-secret-in-production
OPENAI_API_KEY=sk-proj-<your-actual-key>
GITHUB_TOKEN=optional
GITHUB_OWNER=your-username
GITHUB_REPO=your-repo
```

**VERIFY:** Your OPENAI_API_KEY should start with `sk-proj-` or `sk-`

**RUN THIS TO CONFIRM ⬇️**

---

### **STEP 8: Start All Services with Docker Compose**

**WHERE:** PowerShell  
**TIME:** ~30 seconds  
**COMMAND:**
```powershell
docker-compose up -d
```

**WHAT THIS DOES:**
- Creates a Docker network
- Starts PostgreSQL database container
- Starts backend container (port 8000)
- Starts frontend container (port 3000)
- All run in background (`-d` = detached mode)

**EXPECTED OUTPUT:**
```
Creating network "2nd_hackathon-phase1-4_app-network" ... done
Creating 2nd_hackathon-phase1-4_db_1 ... done
Creating 2nd_hackathon-phase1-4_backend_1 ... done
Creating 2nd_hackathon-phase1-4_frontend_1 ... done
```

**RUN THIS NOW ⬇️**

---

### **STEP 9: Check Services Status**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
docker-compose ps
```

**EXPECTED OUTPUT:**
```
NAME                                    STATE    PORTS
2nd_hackathon-phase1-4_backend_1        Up       0.0.0.0:8000->8000/tcp
2nd_hackathon-phase1-4_frontend_1       Up       0.0.0.0:3000->3000/tcp
2nd_hackathon-phase1-4_db_1             Up       0.0.0.0:5432->5432/tcp
```

**WHAT TO CHECK:**
- All services should show **"Up"** in STATE column
- Ports should be mapped correctly

**IF ANY SERVICE IS NOT "Up":**
```powershell
docker-compose logs <service-name>
```
Replace `<service-name>` with: `backend`, `frontend`, or `db`

**RUN THIS TO VERIFY ⬇️**

---

### **STEP 10: Test Backend Health**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
curl http://localhost:8000/health
```

**EXPECTED OUTPUT:**
```json
{"status":"healthy","database":"connected"}
```

**IF YOU GET AN ERROR:**
- Wait 10 seconds and try again (backend might still be starting)
- Check backend logs: `docker-compose logs backend`

**RUN THIS TO TEST ⬇️**

---

### **STEP 11: Test Frontend**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
curl http://localhost:3000
```

**EXPECTED OUTPUT:**
You should see HTML content (a long response starting with `<!DOCTYPE html>`)

**RUN THIS TO TEST ⬇️**

---

### **STEP 12: Open Application in Browser**

**WHERE:** Your Web Browser  
**ACTIONS:**

1. Open your browser (Chrome, Edge, Firefox, etc.)
2. Go to: **http://localhost:3000**
3. You should see the Todo application login page

**WHAT TO TEST:**
- ✅ Page loads without errors
- ✅ Can login (use admin credentials if available)
- ✅ Can access chat page
- ✅ Chat works without "streaming error"
- ✅ Voice features work

**DO THIS NOW ⬇️**

---

## 📊 MONITORING & LOGS

### **View All Logs**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
docker-compose logs
```

### **View Logs for Specific Service**

**WHERE:** PowerShell  
**COMMANDS:**
```powershell
# Backend logs
docker-compose logs backend

# Frontend logs
docker-compose logs frontend

# Database logs
docker-compose logs db
```

### **Follow Logs in Real-Time**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
docker-compose logs -f
```

Press **Ctrl+C** to stop following logs.

### **View Last 50 Lines**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
docker-compose logs --tail=50
```

---

## 🛑 STOPPING & RESTARTING

### **Stop All Services**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
docker-compose down
```

**WHAT THIS DOES:**
- Stops all containers
- Removes containers
- Removes network
- **KEEPS:** Database data (in Docker volume)

### **Stop and Remove Everything (Including Data)**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
docker-compose down -v
```

**⚠️ WARNING:** This deletes all database data!

### **Restart Services**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
docker-compose restart
```

### **Restart Specific Service**

**WHERE:** PowerShell  
**COMMANDS:**
```powershell
docker-compose restart backend
docker-compose restart frontend
docker-compose restart db
```

### **Rebuild and Restart**

**WHERE:** PowerShell  
**COMMAND:**
```powershell
docker-compose up -d --build
```

**WHEN TO USE:** After changing code or Dockerfiles

---

## 🔍 TROUBLESHOOTING

### **Problem: Build fails with "requirements.txt not found"**

**WHERE:** PowerShell  
**CHECK:**
```powershell
Get-Content requirements.txt
```

**FIX:** File should have content. If empty, it was already fixed in your project.

---

### **Problem: Port already in use**

**WHERE:** PowerShell  
**CHECK:**
```powershell
netstat -ano | findstr :3000
netstat -ano | findstr :8000
```

**FIX:**
```powershell
# Stop the conflicting process or use docker-compose down
docker-compose down
docker-compose up -d
```

---

### **Problem: Backend won't start**

**WHERE:** PowerShell  
**CHECK LOGS:**
```powershell
docker-compose logs backend
```

**COMMON ISSUES:**
- Missing OPENAI_API_KEY in .env
- Database not ready (wait 10 seconds and check again)
- Port 8000 already in use

---

### **Problem: Frontend can't connect to backend**

**WHERE:** PowerShell  
**CHECK:**
```powershell
# Verify backend is running
docker-compose ps

# Test backend health
curl http://localhost:8000/health

# Check frontend logs
docker-compose logs frontend
```

---

### **Problem: Chat shows "streaming error"**

**SOLUTION:** This was already fixed in `src/frontend/app/api/chat/route.ts`

**VERIFY FIX:**
```powershell
# Rebuild frontend
docker-compose up -d --build frontend
```

---

## ✅ VERIFICATION CHECKLIST

After completing all steps, verify:

- [ ] **Step 2:** Backend image built successfully
- [ ] **Step 3:** Frontend image built successfully
- [ ] **Step 4:** Both images appear in `docker images`
- [ ] **Step 6:** .env file has your actual OPENAI_API_KEY
- [ ] **Step 8:** All services started
- [ ] **Step 9:** All services show "Up" status
- [ ] **Step 10:** Backend health check returns `{"status":"healthy"}`
- [ ] **Step 11:** Frontend returns HTML
- [ ] **Step 12:** Application opens in browser
- [ ] **Step 12:** Can login to application
- [ ] **Step 12:** Chat works without errors

---

## 🎯 QUICK REFERENCE

### **Essential Commands (All in PowerShell)**

```powershell
# Build images
docker build -f Dockerfile.backend -t todo-backend:latest .
docker build -f Dockerfile.frontend -t todo-frontend:latest .

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Test backend
curl http://localhost:8000/health

# Open in browser
start http://localhost:3000
```

---

## 🚀 NEXT STEPS AFTER DOCKER WORKS

Once Docker deployment is working, you can try:

1. **Kubernetes Deployment** (see `DOCKER_KUBERNETES_DEPLOYMENT.md`)
2. **Scale Services** (increase replicas)
3. **Deploy to Cloud** (AWS, Azure, GCP)

---

## 📚 RELATED DOCUMENTATION

- **Full Guide:** `DOCKER_KUBERNETES_DEPLOYMENT.md`
- **Quick Reference:** `QUICK_REFERENCE.md`
- **Streaming Fix:** `STREAMING_FIX_APPLIED.md`
- **Visual Guide:** `VISUAL_DEPLOYMENT_GUIDE.md`

---

## 🎉 YOU'RE READY!

**Start with STEP 2** and work through each step in order.

All commands are clearly marked with **WHERE:** to show they run in **PowerShell**.

**Current command to run:**
```powershell
docker build -f Dockerfile.backend -t todo-backend:latest .
```

Good luck! 🚀
