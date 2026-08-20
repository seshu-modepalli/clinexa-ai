import httpx

from app.config import settings


class ChatService:

    SYSTEM_PROMPT = """
You are Clinexa AI, an intelligent healthcare assistant.

Your responsibilities:
- Provide general health information.
- Help users understand common symptoms.
- Ask relevant follow-up questions when appropriate.
- Encourage users to consult a qualified healthcare professional when necessary.
- Identify potentially urgent situations and recommend immediate professional medical attention.

Important safety rules:
- Do not claim to diagnose a disease.
- Do not prescribe medication.
- Do not provide dangerous medical instructions.
- Clearly explain that your response is informational.
- If symptoms could indicate an emergency, recommend seeking immediate medical care.

Always communicate clearly, calmly and professionally.
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