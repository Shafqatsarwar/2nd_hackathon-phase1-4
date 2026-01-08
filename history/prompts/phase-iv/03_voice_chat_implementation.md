# Phase IV Prompt History Log - Session 002

## Date: 2026-01-08
**Focus**: Voice-Enabled Chatbot & Vercel AI SDK Integration

## Summary of Actions

### 1. Specification Reorganization
-   **User Request**: "Add proper plan, spec and task in md file".
-   **Action**: Moved Phase IV specs to standard directory structure: `specs/phase-iv-local-kubernetes-deployment/`.
    -   `spec.md`: Detailed system requirements and compliance.
    -   `plan.md`: Technical implementation strategy.
    -   `tasks.md`: Task checklist for judging.

### 2. Voice-Enabled Chatbot (ChatKit/AI SDK)
-   **User Request**: "Add chatkit for better chatbot integrations and improve ui... try voiceenable chatbot".
-   **Action**:
    -   **Dependencies**: Installed `ai`, `framer-motion`, `react-markdown` via `install_chat_deps.sh`.
    -   **Frontend (`page.tsx`)**: Replaced manual fetch with **Vercel AI SDK** (`useChat`).
    -   **Voice Input**: Added `SpeechRecognition` (Web Speech API) for real-time transcription.
    -   **Voice Output**: Added `speechSynthesis` (TTS) for reading AI responses.
    -   **Backend Adapter (`api/chat/route.ts`)**: Created a Next.js Route Handler to proxy requests from the AI SDK to the Python FastAPI backend.

### 3. Documentation Updates
-   **User Request**: "Update in guide.md".
-   **Action**: Added "🎙️ Voice-Enabled AI Chatbot" section to `guide.md`, explaining how to use the microphone and speaker features and the new architecture.

### 4. Bug Fixes
-   **Issue**: TypeScript errors ("Cannot find module", "Implicit any") and syntax errors in `page.tsx`.
-   **Fix**:
    -   Created `install_chat_deps.sh` to fix missing modules.
    -   Rewrote `page.tsx` to handle types correctly and removed syntax errors.

## Next Steps
-   Run `wsl --cd src/frontend bash install_chat_deps.sh` to ensure environment is clean.
-   Restart `npm run dev` to load the new API route.
-   Test Voice Chat in Chrome/Edge.
