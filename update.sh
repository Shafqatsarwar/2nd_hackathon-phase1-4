#!/bin/bash
SRC="/home/shafqatsarwar/Projects/2nd_hackathon-phase1-4/public/2nd_hackathon-phase1-3-main"
DEST="/home/shafqatsarwar/Projects/2nd_hackathon-phase1-4"

echo "Updating TaskInterface..."
cp -f "$SRC/src/frontend/components/TaskInterface.tsx" "$DEST/src/frontend/components/TaskInterface.tsx"

echo "Updating tailwind.config.js..."
cp -f "$SRC/src/frontend/tailwind.config.js" "$DEST/src/frontend/tailwind.config.js"

echo "Updating globals.css..."
cp -f "$SRC/src/frontend/app/globals.css" "$DEST/src/frontend/app/globals.css"

echo "Updating chat folder..."
cp -rf "$SRC/src/frontend/app/chat" "$DEST/src/frontend/app/"

echo "Update complete."
