#!/bin/bash
echo "📦 Installing Chat Dependencies..."
echo "This fixes missing modules (ai, react-markdown, framer-motion, clsx)"

cd src/frontend

# Use --no-audit to be faster
npm install ai framer-motion react-markdown clsx tailwind-merge lucide-react --no-audit --save

echo "✅ Dependencies Installed!"
echo "🔄 Please restart your valid Next.js server if it's running."
