# Story to Video Converter - Ubuntu Setup Guide

This application creates storybook-style videos from text using AI-generated images and speech.

## Prerequisites

1. **System Dependencies**
   ```bash
   sudo apt update
   sudo apt install -y ffmpeg python3-pyqt5 python3-aiohttp
   ```

2. **API Keys Required**
   - OpenAI API key (for text generation)
   - ElevenLabs API key (for text-to-speech)
   - Stability AI API key (for image generation)

## Setup Instructions

1. **Clone/Download the project** to your local machine

2. **Configure API keys** by editing `creds.py`:
   ```python
   openai_api_key = "your_openai_api_key_here"
   stability_api_key = "your_stability_api_key_here"
   elevenlabs_api_key = "your_elevenlabs_api_key_here"
   voice_model_id = "your_elevenlabs_voice_model_id_here"
   ```

3. **Create required directories**:
   ```bash
   mkdir -p out/images out/dialog
   ```

4. **Add required files** (if you want overlay functionality):
   - `overlay.mp4` - Green screen overlay video
   - Background music file of your choice

## Running the Application

```bash
python3 main.py
```

## Usage

1. Enter your API keys in the application GUI
2. Enter your story text (alternating image descriptions and dialog)
3. Click "Generate Dialog" to create audio tracks
4. Click "Generate Images" to create images
5. Select background music file
6. Click "Compile Video" to create the final video

## File Structure

- `main.py` - GUI application
- `creds.py` - API credentials
- `dialog.py` - Text-to-speech functionality
- `images.py` - Image generation functionality  
- `video.py` - Video compilation functionality
- `out/images/` - Generated images
- `out/dialog/` - Generated audio files
- `final_video.mp4` - Final output video

## Troubleshooting

- Ensure all API keys are valid and have sufficient credits
- Check that ffmpeg is properly installed: `ffmpeg -version`
- Make sure you have sufficient disk space for video processing
- If you get Qt/GUI errors, try: `export QT_QPA_PLATFORM=xcb` 