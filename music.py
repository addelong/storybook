import os
import asyncio
import hashlib
import json
from typing import Optional

import aiohttp
from tenacity import retry, wait_exponential, stop_after_attempt

JAMENDO_API = "https://api.jamendo.com/v3.0/tracks/"


def _cache_path(url: str) -> str:
    os.makedirs("./out", exist_ok=True)
    os.makedirs("./out/music", exist_ok=True)
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    return f"./out/music/{digest}.mp3"


async def find_thematic_track(theme_text: str, jamendo_client_id: str) -> Optional[str]:
    if not jamendo_client_id:
        return None

    # Derive tags from theme text via simple heuristics
    theme = (theme_text or "").lower()
    tag = "happy"
    if any(k in theme for k in ["sad", "melancholy", "lonely"]):
        tag = "calm"
    elif any(k in theme for k in ["adventure", "journey", "hero"]):
        tag = "uplifting"
    elif any(k in theme for k in ["calm", "peaceful", "gentle"]):
        tag = "acoustic"

    # Prefer kid-friendly, light genres/moods
    preferred_moods = "happy,bright,cheerful,playful,acoustic,ukulele,whistle,light"

    params = {
        "client_id": jamendo_client_id,
        "format": "json",
        "audioformat": "mp31",
        "include": "musicinfo+licenses",
        "fuzzytags": f"{tag},{preferred_moods}",
        "limit": 1,
        "order": "relevance_desc",
        "licenses": "cc_by-sa,cc_by,cc_by-nc,cc_by-nc-sa,cc0",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(JAMENDO_API, params=params) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            results = data.get("results", [])
            if not results:
                return None
            track = results[0]
            audio_url = track.get("audio")
            if not audio_url:
                return None
            target = _cache_path(audio_url)
            if os.path.exists(target):
                return target
            async with session.get(audio_url) as audio_resp:
                if audio_resp.status != 200:
                    return None
                with open(target, "wb") as f:
                    f.write(await audio_resp.read())
            return target


