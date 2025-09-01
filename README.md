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
1) Paste story text: alternate image descriptions and dialog in separate paragraphs
2) Generate Dialog: creates TTS files in `out/dialog/`
3) Generate Images: Stability image gen; optional seed and reference image
4) Music: choose a file or click Auto Music (Jamendo)
5) Compile Video: builds final `final_video.mp4`

Script and Runway
- Generate Script: turns an idea into a story (OpenAI)
- Runway: one-click single clip, or multi-clip (seconds per clip + max clips); concatenates and mixes music

Notes
- Set `RUNWAY_API_URL` and `RUNWAY_API_KEY` env vars to enable Runway prototype
- For Jamendo auto-music, set `jamendo_client_id` in `creds.py`
