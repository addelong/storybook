import asyncio
from openai import AsyncOpenAI
from creds import openai_api_key

client = AsyncOpenAI(api_key=openai_api_key)

async def generate_story(prompt: str, style: str = "storybook") -> str:
    system = (
        "You are a children's screenwriter. Produce text in an exact, simple format:\n"
        "- Alternate paragraphs: (1) Image Description, then (2) Dialog, and repeat.\n"
        "- Separate each paragraph with a single blank line.\n"
        "- Image paragraphs (PROMPTS): 1-2 sentences used verbatim as prompts to an AI image generator for the NEXT dialog paragraph. They MUST be purely visual.\n"
        "  - No speech/quotes, feelings, intentions, backstory, or plot progression.\n"
        "  - Describe a single frozen moment that a camera could see (no motion verbs like 'presses', 'jumps', 'goes', 'begins to', 'returns').\n"
        "  - Every image prompt must fully restate standalone context: character NAMES, SPECIES (e.g., squirrel, rabbit), age, clothing and colors, environment/location, time of day, lighting, mood, and camera framing (close-up, medium shot, wide).\n"
        "  - If characters are animals, keep them clearly anthropomorphic animals (not humans).\n"
        "  - Repetition is EXPECTED and REQUIRED across prompts to ensure independent generation and consistency.\n"
        "  - Maintain strict visual continuity across ALL image paragraphs: same characters, outfits, palette, art style, and environment unless explicitly changed by the story.\n"
        "  - Match the NEXT dialog paragraph precisely in subject and setting; do not invent new objects/places/characters.\n"
        "  - Never use generic labels in image prompts (e.g., 'siblings', 'friends', 'kids'); always specify each character by species, name, outfit, and age.\n"
        "- Dialog paragraphs (STORY): 1-2 short lines of narrative or character speech. Keep all plot details and actions here (not in image paragraphs).\n"
        "- Keep it gentle, imaginative, and age-appropriate.\n\n"
        "Longer example (do not label sections; follow the exact pattern):\n"
        "Medium shot, daytime, in a sunny backyard: LEO THE SQUIRREL (age 8, red cap, blue shorts) and MIA THE RABBIT (age 7, pink dress, yellow bow) stand on a wooden ladder leading to a blue-and-orange treehouse; soft warm sunlight through leaves; cheerful color palette; camera at eye level.\n\n"
        "\"Wow, Mia, our secret treehouse!\" says Leo.\n\n"
        "Interior of the treehouse, cozy wood walls: the round silver ELEVATOR DOOR with colorful buttons glows beside a small table holding a MAP; LEO THE SQUIRREL (red cap, blue shorts) and MIA THE RABBIT (pink dress, yellow bow) look toward the elevator; late-afternoon light through a window; medium-wide framing.\n\n"
        "\"Do you think it really goes to the jungle?\" asks Mia.\n\n"
        "Jungle doorway POV from inside elevator: lush green leaves and orange flowers outside; colorful parrots perched; LEO THE SQUIRREL (red cap, blue shorts) and MIA THE RABBIT (pink dress, yellow bow) visible from behind; bright dappled sunlight; wide shot.\n\n"
        "\"Let’s explore the jungle first!\" says Leo.\n\n"
        "Desert vista at sunset: golden dunes, cacti silhouettes; LEO THE SQUIRREL (red cap, blue shorts) and MIA THE RABBIT (pink dress, yellow bow) start a sandy mound decorated with seashells; warm rim light; medium-wide shot.\n\n"
        "\"This sandcastle is huge!\" says Mia.\n\n"
        "Candy mountain land: bright sugar hills, lollipop trees, chocolate river; LEO THE SQUIRREL (red cap, blue shorts) and MIA THE RABBIT (pink dress, yellow bow) at the base of a rainbow candy tower; soft pastel lighting; wide establishing shot.\n\n"
    )

    user = (
        f"Style: {style}.\n\n"
        f"Write a short, self-contained story with AT LEAST 20 paragraphs total (10 image paragraphs and 10 dialog paragraphs), strictly alternating image and dialog as specified. End on a dialog paragraph.\n"
        f"Image paragraphs are AI image prompts: purely visual, no story actions, no speech, no feelings. Dialog paragraphs carry all narrative.\n"
        f"Keep visual identity and style consistent across the entire piece (characters' names, ages, outfits, colors, environment, palette, and art style).\n"
        f"EVERY image paragraph must include full standalone context for independent generation, even if repetitive: species/identity, outfits and colors, exact location, time of day, lighting, mood, and camera framing.\n"
        f"If animals are the characters, they must remain anthropomorphic animals in every image (never humans).\n"
        f"Ensure each image paragraph concretely depicts what the NEXT dialog references (no new elements).\n"
        f"Avoid generic backgrounds; include salient props the character mentions.\n\n"
        f"Topic/Prompt:\n{prompt}\n"
    )

    # Use Responses API with a single combined input string for maximum compatibility
    combined_input = system + "\n\n" + user
    resp = await client.responses.create(
        model="gpt-5",
        input=combined_input,
        temperature=0.7,
        max_output_tokens=1200,
    )
    # Prefer the convenience field when available
    if hasattr(resp, "output_text") and resp.output_text:
        return resp.output_text
    # Fallback: concatenate structured output parts
    # Structured fallbacks across SDK versions
    try:
        data = resp.model_dump() if hasattr(resp, "model_dump") else None
    except Exception:
        data = None
    if data:
        # 1) output_text
        if isinstance(data.get("output_text"), str) and data["output_text"]:
            return data["output_text"]
        # 2) output -> content -> text
        out = data.get("output") or []
        parts: list[str] = []
        for item in out:
            for c in (item.get("content") or []):
                t = c.get("text")
                if t:
                    parts.append(t)
        if parts:
            return "".join(parts)
        # 3) choices-style (if backend returned chat-like schema)
        ch = data.get("choices") or []
        if ch and isinstance(ch, list):
            msg = (ch[0] or {}).get("message") or {}
            if isinstance(msg.get("content"), str):
                return msg["content"]
    return ""