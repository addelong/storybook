# Changelog

## 2025-09-01

- Script generator: `text.py` migrated to OpenAI v1 async (`AsyncOpenAI`). GUI button “Generate Script”.
- Image generation options: seed support and reference image (image-to-image) with adjustable strength in GUI.
- Auto-music: `music.py` integrates Jamendo search; GUI “Auto Music” button; cached downloads in `out/music/`.
- Runway: single-clip (`generate_video_from_prompt`) and multi-clip (`generate_clips_from_paragraphs`) support, with concatenation in `video.py` via `concat_runway_clips`; GUI inputs for seconds per clip and max clips.
- `.gitignore` restored to exclude caches and temp artifacts.
- Docs updated: README and setup guide mention new features and Jamendo key.

Notes for next agent:
- OpenAI: set `openai_api_key` in `creds.py`.
- Stability: `Authorization` should be `Bearer <key>`; code normalizes if missing.
- Jamendo: set `jamendo_client_id` for auto music (fallback is manual file browse).
- Runway: `runway.py` uses env vars `RUNWAY_API_URL` and `RUNWAY_API_KEY`; update payloads/parsing to actual API.
- Branches: `gui` is portrait (shorts), `gui-longform` is landscape.

