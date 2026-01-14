#!/bin/bash

# Docker Deployment Script for Phase 1-4
# This script sets up and deploys the application using Docker

echo "🐳 Docker Deployment for Phase 1-4"
echo "=================================="
echo ""

# Step 1: Create .env file for Docker Compose
echo "📝 Step 1: Creating .env file for Docker Compose..."
cat > .env <<'EOF'
# Docker Compose Environment Variables
DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
OPENAI_API_KEY=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
GITHUB_TOKEN=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
GITHUB_OWNER=Shafqatsarwar
GITHUB_REPO=2nd_hackathon-phase1-4
EOF

echo "✅ Created .env file"
echo ""

# Step 2: Stop any running containers
echo "🛑 Step 2: Stopping any existing containers..."
docker-compose down 2>/dev/null || true
echo "✅ Containers stopped"
echo ""

# Step 3: Build Docker images
echo "🔨 Step 3: Building Docker images..."
echo "This may take 5-10 minutes on first build..."
echo ""

echo "Building backend image..."
docker build -f Dockerfile.backend -t todo-backend:latest . || {
    echo "❌ Backend build failed!"
    exit 1
}
echo "✅ Backend image built"
echo ""

echo "Building frontend image..."
docker build -f Dockerfile.frontend -t todo-frontend:latest . || {
    echo "❌ Frontend build failed!"
    exit 1
}
echo "✅ Frontend image built"
echo ""

# Step 4: Start containers
echo "🚀 Step 4: Starting containers with docker-compose..."
docker-compose up -d || {
    echo "❌ Failed to start containers!"
    exit 1
}
echo ""

# Step 5: Wait for services to be ready
echo "⏳ Step 5: Waiting for services to start..."
sleep 10
echo ""

# Step 6: Check container status
echo "📊 Step 6: Container Status"
echo "=========================="
docker-compose ps
echo ""

# Step 7: Show logs
echo "📜 Step 7: Recent Logs"
echo "===================="
docker-compose logs --tail=20
echo ""

# Step 8: Health checks
echo "🏥 Step 8: Health Checks"
echo "======================="
echo ""

echo "Testing backend health..."
curl -s http://localhost:8000/health | jq '.' 2>/dev/null || curl -s http://localhost:8000/health || echo "Backend not ready yet"
echo ""

echo "Testing frontend..."
curl -s -o /dev/null -w "Frontend HTTP Status: %{http_code}\n" http://localhost:3000 || echo "Frontend not ready yet"
echo ""

# Final instructions
echo "🎉 Deployment Complete!"
echo "======================"
echo ""
echo "Your application is now running in Docker:"
echo ""
echo "  🌐 Frontend:  http://localhost:3000"
echo "  🔧 Backend:   http://localhost:8000"
echo "  📚 API Docs:  http://localhost:8000/docs"
echo "  🗄️  Database: localhost:5432 (PostgreSQL)"
echo ""
echo "Useful commands:"
echo "  View logs:        docker-compose logs -f"
echo "  Stop containers:  docker-compose down"
echo "  Restart:          docker-compose restart"
echo "  Rebuild:          docker-compose up -d --build"
echo ""
echo "✨ Happy coding!"
