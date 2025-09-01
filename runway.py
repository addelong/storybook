import os
import asyncio
from typing import Optional, List
import aiohttp

# Prototype integration stub. Runway API access requires credentials and
# possibly usage of hosted endpoints. This function is a placeholder to
# demonstrate flow in the GUI.

RUNWAY_API_URL = os.environ.get("RUNWAY_API_URL", "")
RUNWAY_API_KEY = os.environ.get("RUNWAY_API_KEY", "")


async def generate_video_from_prompt(prompt: str, duration_seconds: int = 5) -> Optional[str]:
    if not RUNWAY_API_URL or not RUNWAY_API_KEY:
        return None
    # Example payload — adjust per actual API once available
    payload = {
        "prompt": prompt,
        "duration": duration_seconds,
        "resolution": "1280x720",
    }
    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(RUNWAY_API_URL, json=payload, headers=headers) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            # Expect a downloadable URL
            url = data.get("result_url")
            if not url:
                return None
            # Download to out/
            os.makedirs("./out", exist_ok=True)
            target = "./out/runway_clip.mp4"
            async with session.get(url) as dl:
                if dl.status != 200:
                    return None
                with open(target, "wb") as f:
                    f.write(await dl.read())
            return target


async def generate_clips_from_paragraphs(paragraphs: List[str], seconds_per_clip: int = 5, max_clips: Optional[int] = None) -> List[str]:
    if not RUNWAY_API_URL or not RUNWAY_API_KEY:
        return []
    os.makedirs("./out/runway", exist_ok=True)
    clips: List[str] = []
    count = 0
    for idx, para in enumerate(paragraphs):
        if max_clips is not None and count >= max_clips:
            break
        prompt = (para or "").strip()[:600]
        clip = await generate_video_from_prompt(prompt, seconds_per_clip)
        if clip:
            target = f"./out/runway/clip_{idx}.mp4"
            try:
                # Move/rename to predictable path
                if os.path.abspath(clip) != os.path.abspath(target):
                    try:
                        os.replace(clip, target)
                    except Exception:
                        # Fallback to copy
                        import shutil
                        shutil.copyfile(clip, target)
                else:
                    pass
                clips.append(target)
                count += 1
            except Exception:
                # Skip on filesystem errors
                continue
    return clips


