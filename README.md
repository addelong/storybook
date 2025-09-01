Storybook turns alternating image descriptions and dialog into narrated videos with music.

Quick start
- Install deps: `pip install -r requirements.txt` (or `sudo apt install python3-pyqt5 python3-aiohttp`)
- Add keys to `creds.py`: OpenAI, ElevenLabs, Stability, optional Jamendo
- Create dirs: `mkdir -p out/images out/dialog`
- Run: `python3 main.py`

Branches
- `gui`: Shorts (9:16 portrait), optimized overlays and text wrapping
- `gui-longform`: Landscape (16:9), longer videos

Workflow in the app
Simple Mode (recommended)
1) Type a quick idea (optional) and click Make Video
   - If only an idea is provided, the app writes the script for you
   - It generates TTS, images, auto-picks music, and compiles the video
   - Toggle “Use AI video” to try Runway-generated clips instead of images

Advanced Mode (optional)
- Prompts, seeds, reference image, Runway overrides/clip settings
- Helper text explains each option; defaults work well for most cases

Script and Runway
- Generate Script: turns an idea into a story (OpenAI)
- Runway: one-click single clip, or multi-clip (seconds per clip + max clips); concatenates and mixes music

Notes
- Set `RUNWAY_API_URL` and `RUNWAY_API_KEY` env vars to enable Runway prototype
- For Jamendo auto-music, set `jamendo_client_id` in `creds.py`
