import asyncio
from openai import AsyncOpenAI
from creds import openai_api_key

client = AsyncOpenAI(api_key=openai_api_key)

async def generate_story(prompt: str, style: str = "spooky-shorts") -> str:
    system = (
        "You are a suspense writer for spooky, mystery, and cryptid-themed shorts aimed at older audiences. Produce text in an exact format:\n"
        "- Alternate paragraphs: (1) Image Description, then (2) STORY, and repeat.\n"
        "- Separate each paragraph with a single blank line.\n"
        "- Image paragraphs (PROMPTS): 1-2 sentences, purely visual (no speech/emotions). Describe a single cinematic frame with full standalone context: subject, attire/colors, location, time of day, lighting (e.g., moonlit, flashlight beam), mood (tense, eerie), camera framing (close-up/medium/wide).\n"
        "- STORY paragraphs: 1-3 sentences of narrative prose and/or character speech. If all IMAGE paragraphs were removed, the concatenated STORY paragraphs must read as a complete, coherent short story. Keep plot beats here (not in IMAGE paragraphs).\n"
        "- Maintain strict continuity (names, attire, props, locations). Tone: eerie, restrained, suggestive—no gore.\n"
        "- Output validation: after each IMAGE/STORY pair, self-check visual alignment and continuity; if mismatched, correct before continuing.\n\n"
        "# Example (do not label sections; follow exact alternation)\n"
        "Nighttime, abandoned forest trail under a crescent moon: TEEN INVESTIGATOR JUNE (black hoodie, green backpack) aims a flashlight at mist between pines; breath visible, long shadows; medium shot.\n\n"
        "The trail feels wrong tonight. June lowers her voice. \"You heard that too, right?\"\n\n"
        "Old wooden footbridge over a dark creek: footprints wet on the planks, a torn red scarf snagged on a nail; fireflies glimmer; low-angle, moody rim light.\n\n"
        "Eli studies the prints. \"No way those are ours,\" he whispers, but keeps moving.\n\n"
    )

    user = (
        f"# Story Generation Task\n"
        f"- Style: {style} (spooky, mystery, cryptid-friendly; older audience).\n"
        f"- Write a self-contained short with AT LEAST 20 paragraphs total (10 IMAGE + 10 STORY), always alternating. End with a STORY paragraph.\n"
        f"- IMAGE PROMPTS are purely visual and fully self-contained; STORY paragraphs carry the narrative beats (can be narration and/or dialogue).\n"
        f"- Ensure each IMAGE prompt directly depicts the NEXT STORY—no new elements. Maintain continuity for names, outfits, locations, and props.\n"
        f"- Use atmospheric lighting and camera framing. Tone eerie and suggestive.\n\n"
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