# Changelog

All notable changes to this project will be documented in this file.

## 2025-09-01

Branches: `gui-longform`, merged into `gui` with conflict resolution.

### Added
- Script generator: `text.py` migrated to OpenAI v1 async (`AsyncOpenAI`). GUI button “Generate Script”.
- Image generation options: seed support and reference image (image-to-image) with adjustable strength in GUI.
- Auto-music: `music.py` integrates Jamendo search; GUI “Auto Music” button; cached downloads in `out/music/`.
- Runway prototype: `runway.py` with `generate_video_from_prompt` placeholder; GUI button “Runway: Generate Clip”.
- `.gitignore` to exclude caches and temporary media.

### Changed
- `images.py`: unified to support both text-to-image and image-to-image; on `gui` branch tuned to portrait (768x1344) and lower cfg_scale=8; longform landscapes remain handled by video scaling.
- `video.py`: unified text wrapping for portrait (`max_line_length=65`) and portrait scaling/overlays.
- `main.py`: added UI for script generation, seed, reference image, auto music, and Runway prototype.
- `requirements.txt`: added `openai`, `requests`, `tenacity`, `python-dotenv`.
- `setup_ubuntu.md` and `README.md`: updated docs to mention new features and Jamendo key.
- `creds.py`: added `jamendo_client_id`.

### Notes for Next Agent
- OpenAI: set `openai_api_key` in `creds.py`.
- Stability: The API expects `Authorization: Bearer <key>`. We normalize in `images.py` if not prefixed.
- Jamendo: Set `jamendo_client_id` in `creds.py` to enable auto music. Fallback is manual file browse.
- Runway: `runway.py` is a stub. Set `RUNWAY_API_URL` and `RUNWAY_API_KEY` env vars to enable; update payload/response parsing to the actual API.
- GUI differences: `gui` branch uses portrait pipeline (video overlays set for 768x1344). `gui-longform` retains landscape orientation.
- Temporary files: `video.py` writes temp files; cleanup occurs at end. `.gitignore` excludes them.


