import asyncio
from openai import AsyncOpenAI
from creds import openai_api_key

client = AsyncOpenAI(api_key=openai_api_key)

async def generate_story(prompt: str, style: str = "storybook") -> str:
    system = (
        "You are a children's screenwriter. Produce text in an exact, simple format:\n"
        "- Alternate paragraphs: (1) Image Description, then (2) Dialog, and repeat.\n"
        "- Separate each paragraph with a single blank line.\n"
        "- Image paragraphs (PROMPTS): 1-3 sentences used verbatim as prompts to an AI image generator for the NEXT dialog paragraph. They MUST be purely visual descriptions, not narrative.\n"
        "  - No speech, quotations, onomatopoeia, feelings, internal thoughts, intentions, or plot beats.\n"
        "  - Describe only what a camera could see in a single still frame (show, don't tell).\n"
        "  - Include all standalone context every time: consistent character names and ages, clothing, colors, setting, time of day, lighting, mood, camera framing (e.g., close-up, medium shot), and key props referenced by the next dialog.\n"
        "  - Always restate the characters' species or identity (e.g., rabbit, raccoon, hedgehog) and anthropomorphic style if applicable. Never assume humans unless explicitly stated.\n"
        "  - Repetition is EXPECTED and REQUIRED: each image prompt must fully restate identity, outfits, species, setting, lighting, framing, and style, even if already stated before.\n"
        "  - Maintain visual continuity across ALL image paragraphs: same characters, outfits, palette, art style, and environment unless explicitly changed.\n"
        "- Dialog paragraphs (STORY): 1-2 short lines of narrative or character speech. Keep all plot details and actions here (not in image paragraphs).\n"
        "- Keep it gentle, imaginative, and age-appropriate.\n\n"
        "Example output format (do not label sections):\n"
        "A small fox stands on a riverbank at dusk, fireflies drifting above the water. The forest glows with warm, mossy light.\n\n"
        "\"Do you think the moon follows us?\" whispers Pip.\n\n"
        "A wooden bridge curves over the river; lanterns sway softly in the breeze and reflect on the current.\n\n"
        "\"Come on,\" says Mira, \"adventure is just across the bridge.\" Together, they walk across the bridge and into the forest.\n\n"
    )

    user = (
        f"Style: {style}.\n\n"
        f"Write a short, self-contained story with AT LEAST 20 paragraphs total (10 image paragraphs and 10 dialog paragraphs), strictly alternating image and dialog as specified. End on a dialog paragraph.\n"
        f"Image paragraphs are AI image prompts: purely visual, no story actions, no speech, no feelings. Dialog paragraphs carry all narrative.\n"
        f"Keep visual identity and style consistent across the entire piece (characters' names, ages, outfits, colors, environment, palette, and art style).\n"
        f"Every image paragraph must include sufficient standalone context (who/where/when/lighting/framing/props) for independent generation.\n"
        f"Explicitly restate species/identity for characters in EVERY image paragraph (e.g., rabbit wearing a blue scarf), and clarify anthropomorphic style if used. If the characters are animals, do NOT produce human characters.\n"
        f"Repetition is expected and required: it's okay if prompts repeat details to ensure consistency.\n"
        f"Ensure each image paragraph concretely depicts the exact setting/object/character that the following dialog references.\n"
        f"Avoid generic backgrounds; include salient props the character mentions.\n\n"
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