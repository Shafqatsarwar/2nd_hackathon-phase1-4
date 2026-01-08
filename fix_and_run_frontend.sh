#!/bin/bash
echo "🔧 Fixing Environment..."
# Using tee to ensure we have permission and write correctly
cat <<EOF > src/frontend/.env.local
NEXT_PUBLIC_BACKEND_URL=http://127.0.0.1:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=my_super_secure_hackathon_secret_key_2025
DATABASE_URL=postgresql://neondb_owner:npg_zhJvIP74aTle@ep-long-waterfall-abcwopjg-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
EOF

echo "📦 Installing Frontend Dependencies (this may take a minute)..."
cd src/frontend
npm install

echo "🚀 Starting Frontend at http://localhost:3000"
echo "Press Ctrl+C to stop."
# Run in foreground so user can see errors
npm run dev
