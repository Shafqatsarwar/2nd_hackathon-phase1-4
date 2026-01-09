
import { NextRequest, NextResponse } from "next/server";

export const runtime = "edge";

export async function POST(req: NextRequest) {
    try {
        const { messages, userId, token, conversationId } = await req.json();
        const lastMessage = messages[messages.length - 1];

        // 1. Call Python Backend
        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";
        const response = await fetch(`${backendUrl}/api/${userId}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                message: lastMessage.content,
                conversation_id: conversationId
            })
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Backend chat error:", errorText);

            // Return a more informative error message
            if (response.status === 500) {
                return new NextResponse("Chat service unavailable. Please ensure the backend is running and OPENAI_API_KEY is configured.", { status: 500 });
            }

            return new NextResponse(errorText || "Backend error", { status: response.status });
        }

        const data = await response.json();

        // 2. Return as text (Vercel AI SDK can handle raw text response)
        // If we wanted streaming, we'd use OpenAIStream/LangChainAdapter here.
        // Since Python backend is not streaming, we just return the text.
        return new NextResponse(data.response || "I received your message but couldn't process it. Please make sure the backend is running and OPENAI_API_KEY is configured.");

    } catch (error: any) {
        console.error("Chat Adapter Error:", error);
        return new NextResponse("Chat service is not available. Please ensure the backend is running and OPENAI_API_KEY is configured in the backend.", { status: 500 });
    }
}
