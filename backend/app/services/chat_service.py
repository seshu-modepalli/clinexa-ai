import httpx
import json

from app.config import settings


class ChatService:

    SYSTEM_PROMPT = """
    You are Clinexa AI, an intelligent healthcare assistant.

    Your role:
    - Provide general health information.
    - Help users understand common symptoms.
    - Ask relevant follow-up questions when necessary.
    - Identify potentially urgent situations.
    - Encourage users to consult qualified healthcare professionals when appropriate.

    Safety rules:
    - Do not diagnose diseases.
    - Do not prescribe medications.
    - Do not provide dangerous medical instructions.
    - Do not claim certainty about a medical condition.
    - For emergency warning signs, recommend immediate professional medical attention.

    Response style:
    - Be concise and easy to understand.
    - Answer the user's exact question first.
    - If the user asks for a short answer or specifies a number of lines, follow that instruction.
    - For simple questions, normally respond in 2-4 sentences.
    - Use bullet points only when they improve readability.
    - Do not repeat the user's question.
    - Do not add unnecessary explanations.
    - Do not use excessive medical terminology.
    - Clearly state when professional medical advice is needed.

    Always communicate calmly, clearly and professionally.
    """

    async def chat(self, message: str) -> str:

        url = f"{settings.OLLAMA_URL}/api/generate"

        prompt = f"""
{self.SYSTEM_PROMPT}

User message:
{message}

Clinexa AI response:
"""

        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }

        async with httpx.AsyncClient(timeout=120.0) as client:

            response = await client.post(
                url,
                json=payload
            )

            response.raise_for_status()

            data = response.json()

            return data.get("response", "").strip()

    async def chat_stream(self, message: str):

        url = f"{settings.OLLAMA_URL}/api/generate"

        prompt = f"""
    {self.SYSTEM_PROMPT}

    User message:

    {message}

    Clinexa AI response:
    """

        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": True
        }

        async with httpx.AsyncClient(timeout=None) as client:

            async with client.stream(
                "POST",
                url,
                json=payload
            ) as response:

                response.raise_for_status()

                async for line in response.aiter_lines():

                    if not line:
                        continue

                    try:

                        data = json.loads(line)

                        yield data.get("response", "")

                        if data.get("done", False):
                            break

                    except json.JSONDecodeError:
                        continue