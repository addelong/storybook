import asyncio
from openai import AsyncOpenAI
from creds import openai_api_key

client = AsyncOpenAI(api_key=openai_api_key)

async def generate_story(prompt: str, style: str = "storybook") -> str:
    system = "You are a screenwriter that outputs alternating image descriptions and dialog, separated by blank lines."
    user = f"Style: {style}.\n\nConstraints:\n- Alternate image description and dialog paragraphs.\n- Keep each paragraph 1-3 sentences.\n- Suitable for children.\n\nPrompt:\n{prompt}"
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.8,
        max_tokens=1200,
    )
    # Prefer message.content per new API
    return resp.choices[0].message.content