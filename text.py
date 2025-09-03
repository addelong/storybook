import asyncio
from openai import AsyncOpenAI
from creds import openai_api_key

client = AsyncOpenAI(api_key=openai_api_key)

async def generate_story(prompt: str, style: str = "storybook") -> str:
    system = (
        "You are a children’s screenwriter. Produce text in an exact, simple format:\n"
        "- Alternate paragraphs: (1) Image Description, then (2) Dialog, and repeat.\n"
        "- Separate each paragraph with a single blank line.\n"
        "- Image paragraphs: 1–3 vivid sentences describing a single illustration (no dialogue).\n"
        "- Dialog paragraphs: 1–2 short lines a character speaks (use quotes, optional speaker name).\n"
        "- Keep it gentle, imaginative, and age-appropriate.\n\n"
        "Example output format (do not label sections):\n"
        "A small fox stands on a riverbank at dusk, fireflies drifting above the water. The forest glows with warm, mossy light.\n\n"
        "\"Do you think the moon follows us?\" whispers Pip.\n\n"
        "A wooden bridge curves over the river; lanterns sway softly in the breeze and reflect on the current.\n\n"
        "\"Come on,\" says Mira, \"adventure is just across the bridge.\"\n"
    )

    user = (
        f"Style: {style}.\n\n"
        f"Write a short, self-contained story with 8–14 paragraphs total, alternating image and dialog as specified.\n"
        f"Topic/Prompt:\n{prompt}\n"
    )

    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.7,
        max_tokens=1200,
    )
    return resp.choices[0].message.content