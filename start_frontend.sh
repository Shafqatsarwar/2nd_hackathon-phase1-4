#!/bin/bash
cd src/frontend
echo "Installing dependencies..." > frontend_launch.log
npm install >> frontend_launch.log 2>&1
echo "Starting Next.js..." >> frontend_launch.log
nohup npm run dev >> frontend_launch.log 2>&1 &
echo "Frontend started with PID $!" >> frontend_launch.log
