import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QFileDialog, QProgressBar, QCheckBox
import os
import hashlib
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

# Import necessary functions from your other scripts
from dialog import get_dialog_tracks
from images import generate_images
from text import generate_story
from creds import stability_api_key, elevenlabs_api_key, voice_model_id
from creds import jamendo_client_id
from runway import generate_video_from_prompt, generate_clips_from_paragraphs
from video import create_video_from_images_and_dialogs
from creds import stability_api_key, elevenlabs_api_key, voice_model_id

class Worker(QThread):
    finished = pyqtSignal()  # Signal to indicate the worker has finished

    """ Worker thread to handle long-running tasks without freezing the GUI """
    def __init__(self, func, *args, **kwargs):
        super(Worker, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.finished.connect(self.deleteLater)  # Ensure the worker cleans up after finishing

    def run(self):
        if asyncio.iscoroutinefunction(self.func):
            # Create a new event loop for the coroutine
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.func(*self.args, **self.kwargs))
            loop.close()
        else:
            self.func(*self.args, **self.kwargs)
        self.finished.emit()  # Emit finished signal when done


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.active_workers = []  # Add this line to keep track of active workers

    def initUI(self):
        self.layout = QVBoxLayout()

        # Simple Mode Header
        self.simple_layout = QHBoxLayout()
        self.simple_idea_input = QLineEdit()
        self.simple_idea_input.setPlaceholderText("Describe your video idea (optional)")
        self.use_runway_checkbox = QCheckBox("Use AI video (experimental)")
        self.make_video_button = QPushButton("Make Video")
        self.make_video_button.clicked.connect(self.make_video)
        self.simple_layout.addWidget(self.simple_idea_input)
        self.simple_layout.addWidget(self.use_runway_checkbox)
        self.simple_layout.addWidget(self.make_video_button)
        self.layout.addLayout(self.simple_layout)

        # Story Text Section
        self.story_text = QTextEdit()
        self.story_text.setPlaceholderText("Enter your story here...")
        self.layout.addWidget(self.story_text)

        # Advanced container (collapsible)
        self.advanced_toggle = QPushButton("Show Advanced Options")
        self.advanced_toggle.setCheckable(True)
        self.advanced_toggle.setChecked(False)
        self.advanced_toggle.toggled.connect(self.toggle_advanced)
        self.layout.addWidget(self.advanced_toggle)

        self.advanced_container = QWidget()
        self.advanced_container.setVisible(False)
        self.advanced_layout = QVBoxLayout(self.advanced_container)
        self.advanced_layout.addWidget(QLabel("Advanced options are optional. Defaults are smart and work well. Use these if you need precise control (prompts, seeds, reference images, Runway overrides)."))

        # API Credentials Section (Advanced)
        self.api_keys_layout = QHBoxLayout()
        self.api_keys = {
            'Stability API Key': QLineEdit(),
            'ElevenLabs API Key': QLineEdit(),
            'Voice Model ID': QLineEdit()
        }
        self.api_keys['Stability API Key'].setText(stability_api_key if stability_api_key else 'your_stability_api_key')
        self.api_keys['ElevenLabs API Key'].setText(elevenlabs_api_key if elevenlabs_api_key else 'your_elevenlabs_api_key')
        self.api_keys['Voice Model ID'].setText(voice_model_id if voice_model_id else 'your_voice_model_id')
        for label, line_edit in self.api_keys.items():
            self.api_keys_layout.addWidget(QLabel(label))
            self.api_keys_layout.addWidget(line_edit)
        self.advanced_layout.addLayout(self.api_keys_layout)

        # Script generator controls (Advanced)
        self.script_layout = QHBoxLayout()
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Enter a story idea and click Generate Script")
        self.generate_script_button = QPushButton("Generate Script")
        self.generate_script_button.clicked.connect(self.generate_script)
        self.script_layout.addWidget(self.prompt_input)
        self.script_layout.addWidget(self.generate_script_button)
        self.advanced_layout.addLayout(self.script_layout)

        # Image Generation Text Section (Optional)
        self.image_text = QTextEdit()
        self.image_negative_text = QTextEdit()
        self.image_text.setText("beautiful, kid friendly, perfect quality, 3d animated movie still, pixar, digital art, color, coherent, uhd, detailed face, looks good, expressive, magical, ")
        self.image_negative_text.setText("blurry, bad, sloppy, incoherent, weird faces, messed up, weird hands, too many limbs or digits, anatomically incorrect, unnatural or creepy facial expression, generic or overused design, inconsistent scale or proportions, maniacal smiling")
        self.advanced_layout.addWidget(QLabel("Image Generation Prompt"))
        self.advanced_layout.addWidget(self.image_text)
        self.advanced_layout.addWidget(QLabel("Image Generation Negative Prompt"))
        self.advanced_layout.addWidget(self.image_negative_text)

        # Seed for character consistency
        self.seed_layout = QHBoxLayout()
        self.seed_label = QLabel("Image Seed (optional):")
        self.seed_input = QLineEdit()
        self.seed_input.setPlaceholderText("e.g., 12345")
        self.seed_layout.addWidget(self.seed_label)
        self.seed_layout.addWidget(self.seed_input)
        self.advanced_layout.addLayout(self.seed_layout)

        # Reference image (image-to-image)
        self.ref_layout = QHBoxLayout()
        self.ref_label = QLabel("Reference Image (optional):")
        self.ref_path = QLineEdit()
        self.ref_browse = QPushButton("Browse")
        self.ref_browse.clicked.connect(self.browse_ref_image)
        self.ref_strength_label = QLabel("Strength:")
        self.ref_strength_input = QLineEdit()
        self.ref_strength_input.setPlaceholderText("0.0-1.0, default 0.7")
        self.ref_layout.addWidget(self.ref_label)
        self.ref_layout.addWidget(self.ref_path)
        self.ref_layout.addWidget(self.ref_browse)
        self.ref_layout.addWidget(self.ref_strength_label)
        self.ref_layout.addWidget(self.ref_strength_input)
        self.advanced_layout.addLayout(self.ref_layout)

        # Background Music Selection
        self.bgm_layout = QHBoxLayout()
        self.bgm_label = QLabel("Background Music:")
        self.bgm_file = QLineEdit()
        self.bgm_button = QPushButton("Browse")
        self.bgm_button.clicked.connect(self.browse_music)
        self.auto_music_button = QPushButton("Auto Music")
        self.auto_music_button.clicked.connect(self.auto_music)
        self.bgm_layout.addWidget(self.bgm_label)
        self.bgm_layout.addWidget(self.bgm_file)
        self.bgm_layout.addWidget(self.bgm_button)
        self.bgm_layout.addWidget(self.auto_music_button)
        self.advanced_layout.addLayout(self.bgm_layout)

        # Control Buttons
        self.buttons_layout = QHBoxLayout()
        self.generate_dialog_button = QPushButton("Generate Dialog")
        self.generate_dialog_button.clicked.connect(self.generate_dialog)
        self.generate_images_button = QPushButton("Generate Images")
        self.generate_images_button.clicked.connect(self.generate_images)
        self.compile_video_button = QPushButton("Compile Video")
        self.compile_video_button.clicked.connect(self.compile_video)
        self.runway_toggle = QPushButton("Runway: Generate Clip")
        self.runway_toggle.clicked.connect(self.generate_runway_clip)
        self.runway_multi_layout = QHBoxLayout()
        self.runway_clip_secs = QLineEdit()
        self.runway_clip_secs.setPlaceholderText("Clip seconds (e.g., 5)")
        self.runway_max_clips = QLineEdit()
        self.runway_max_clips.setPlaceholderText("Max clips (optional)")
        self.runway_compile_btn = QPushButton("Runway: Compile From Story")
        self.runway_compile_btn.clicked.connect(self.generate_runway_from_story)
        self.runway_multi_layout.addWidget(self.runway_clip_secs)
        self.runway_multi_layout.addWidget(self.runway_max_clips)
        self.runway_multi_layout.addWidget(self.runway_compile_btn)
        self.buttons_layout.addWidget(self.generate_dialog_button)
        self.buttons_layout.addWidget(self.generate_images_button)
        self.buttons_layout.addWidget(self.compile_video_button)
        self.buttons_layout.addWidget(self.runway_toggle)
        self.advanced_layout.addLayout(self.buttons_layout)
        self.advanced_layout.addLayout(self.runway_multi_layout)

        # Runway overrides and progress (Advanced)
        self.advanced_layout.addWidget(QLabel("Runway Prompt Overrides (optional, blank-line separated):"))
        self.runway_overrides = QTextEdit()
        self.runway_overrides.setPlaceholderText("Provide custom prompts per paragraph. If left empty, paragraphs are used.")
        self.advanced_layout.addWidget(self.runway_overrides)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.advanced_layout.addWidget(self.progress_bar)

        self.layout.addWidget(self.advanced_container)

        # Progress bar visibility off by default
        self.progress_bar.setVisible(False)

        # Set main layout
        self.setLayout(self.layout)
        self.setWindowTitle('Story to Video Converter')

    def browse_music(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Background Music", "", "Audio Files (*.mp3 *.wav)")
        if filename:
            self.bgm_file.setText(filename)

    def browse_ref_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Reference Image", "", "Images (*.png *.jpg *.jpeg)")
        if filename:
            self.ref_path.setText(filename)

    def generate_dialog(self):
        # Split the story into lines, separated by two newlines. Separate them into two sets.
        # The first set contains the 1st, 3rd, 5th, etc. lines, and the second set contains the 2nd, 4th, 6th, etc. lines.
        # The first set is the image descriptions, and the second set is the dialog.
        story = self.story_text.toPlainText()
        paragraphs = story.split("\n\n")
        self.start_worker(get_dialog_tracks, paragraphs, self.api_keys['ElevenLabs API Key'].text(), self.api_keys['Voice Model ID'].text())

    def generate_images(self):
        # Split the story into lines, separated by two newlines. Separate them into two sets.
        # The first set contains the 1st, 3rd, 5th, etc. lines, and the second set contains the 2nd, 4th, 6th, etc. lines.
        # The first set is the image descriptions, and the second set is the dialog.
        story_text = self.story_text.toPlainText()
        paragraphs = story_text.split("\n\n")
        seed_text = self.seed_input.text().strip()
        seed_val = int(seed_text) if seed_text.isdigit() else None
        ref_path = self.ref_path.text().strip() or None
        try:
            strength_val = float(self.ref_strength_input.text().strip()) if self.ref_strength_input.text().strip() else 0.7
        except ValueError:
            strength_val = 0.7
        self.start_worker(
            generate_images,
            paragraphs,
            self.image_text.toPlainText(),
            self.image_negative_text.toPlainText(),
            self.api_keys['Stability API Key'].text(),
            seed_val,
            ref_path,
            strength_val,
        )

    def compile_video(self):
        story = self.story_text.toPlainText()
        paragraphs = story.split("\n\n")
        self.start_worker(create_video_from_images_and_dialogs, "./out/images", "png", self.bgm_file.text(), "./out/dialog", "mp3", paragraphs, "./final_video.mp4")

    def generate_script(self):
        idea = self.prompt_input.text().strip()
        if not idea:
            return
        async def run():
            script = await generate_story(idea)
            self.story_text.setText(script)
        self.start_worker(run)

    def make_video(self):
        idea = self.simple_idea_input.text().strip()
        use_runway = self.use_runway_checkbox.isChecked()

        async def run():
            story_text = self.story_text.toPlainText().strip()
            if not story_text and idea:
                # Auto-generate script from idea
                gen = await generate_story(idea)
                story_text = gen or idea
                self.story_text.setText(story_text)

            paragraphs = story_text.split("\n\n") if story_text else []
            # Derive seed from story for stable character consistency
            seed_val = int(hashlib.sha256((story_text or idea).encode("utf-8")).hexdigest()[:8], 16) if (story_text or idea) else None

            # Auto music attempt
            music = self.bgm_file.text().strip()
            if not music:
                try:
                    from music import find_thematic_track
                    track_path = await find_thematic_track(story_text or idea, jamendo_client_id)
                    if track_path:
                        music = track_path
                        self.bgm_file.setText(music)
                except Exception:
                    pass

            if use_runway and paragraphs:
                # Minimal runway path: 5s per clip, up to 12 clips (1 min)
                secs = 5
                maxc = 12
                self.progress_bar.setVisible(True)
                self.progress_bar.setMaximum(min(len(paragraphs), maxc))
                self.progress_bar.setValue(0)
                from runway import generate_video_from_prompt
                clips = []
                for idx, para in enumerate(paragraphs):
                    if idx >= maxc:
                        break
                    clip = await generate_video_from_prompt(para[:600], secs)
                    if clip:
                        clips.append(clip)
                    self.progress_bar.setValue(idx + 1)
                if clips:
                    from video import concat_runway_clips
                    concat_runway_clips(clips, music if music else clips[0], "./final_video.mp4")
                self.progress_bar.setVisible(False)
                return

            if paragraphs:
                # Generate dialog (TTS)
                await get_dialog_tracks(paragraphs[1::2], self.api_keys['ElevenLabs API Key'].text(), self.api_keys['Voice Model ID'].text())
                # Generate images for description paragraphs
                await generate_images(paragraphs[0::2], self.image_text.toPlainText(), self.image_negative_text.toPlainText(), self.api_keys['Stability API Key'].text(), seed_val)
                # Compile
                create_video_from_images_and_dialogs("./out/images", "png", music if music else self.bgm_file.text(), "./out/dialog", "mp3", paragraphs, "./final_video.mp4")
        self.start_worker(run)

    def auto_music(self):
        # Placeholder: choose an existing local file if jamendo_client_id not set
        if not jamendo_client_id:
            filename, _ = QFileDialog.getOpenFileName(self, "Select Background Music", "", "Audio Files (*.mp3 *.wav)")
            if filename:
                self.bgm_file.setText(filename)
            return
        # Defer import to avoid hard dependency
        try:
            from music import find_thematic_track
        except Exception:
            return
        story = self.story_text.toPlainText()
        async def run():
            track_path = await find_thematic_track(story, jamendo_client_id)
            if track_path:
                self.bgm_file.setText(track_path)
        self.start_worker(run)

    def generate_runway_clip(self):
        prompt = self.story_text.toPlainText()[:500]
        async def run():
            clip = await generate_video_from_prompt(prompt, 5)
            # No UI for preview; just place file if generated
            if clip:
                self.bgm_label.setText("Background Music:")
        self.start_worker(run)

    def generate_runway_from_story(self):
        story = self.story_text.toPlainText()
        paragraphs = story.split("\n\n")
        overrides_text = self.runway_overrides.toPlainText().strip()
        overrides = overrides_text.split("\n\n") if overrides_text else []
        try:
            secs = int(self.runway_clip_secs.text().strip()) if self.runway_clip_secs.text().strip() else 5
        except ValueError:
            secs = 5
        try:
            maxc = int(self.runway_max_clips.text().strip()) if self.runway_max_clips.text().strip() else None
        except ValueError:
            maxc = None

        async def run():
            self.progress_bar.setVisible(True)
            # Generate sequentially to track progress
            total = len(paragraphs) if maxc is None else min(len(paragraphs), maxc)
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(0)
            os.makedirs("./out/runway", exist_ok=True)
            clips = []
            for idx, para in enumerate(paragraphs):
                if maxc is not None and idx >= maxc:
                    break
                prompt = (overrides[idx].strip() if idx < len(overrides) and overrides[idx].strip() else para.strip())[:600]
                clip = await generate_video_from_prompt(prompt, secs)
                if clip:
                    target = f"./out/runway/clip_{idx}.mp4"
                    try:
                        if os.path.abspath(clip) != os.path.abspath(target):
                            try:
                                os.replace(clip, target)
                            except Exception:
                                import shutil
                                shutil.copyfile(clip, target)
                        clips.append(target)
                    except Exception:
                        pass
                # Update progress
                try:
                    self.progress_bar.setValue(min(idx + 1, total))
                except Exception:
                    pass
            if not clips:
                return
            # auto-music if not set
            music = self.bgm_file.text().strip()
            if not music:
                try:
                    from music import find_thematic_track
                    track_path = await find_thematic_track(story, jamendo_client_id)
                    if track_path:
                        music = track_path
                except Exception:
                    pass
            from video import concat_runway_clips
            concat_runway_clips(clips, music if music else clips[0], "./final_video.mp4")
            self.progress_bar.setVisible(False)
        self.start_worker(run)

    def toggle_advanced(self, checked):
        self.advanced_container.setVisible(checked)

    def start_worker(self, func, *args):
        """ Starts a worker thread to run a function """
        worker = Worker(func, *args)
        worker.finished.connect(lambda: self.active_workers.remove(worker))  # Remove worker from the list when done
        self.active_workers.append(worker)  # Keep track of the worker
        worker.start()
        # Optionally, connect signals from the worker here (e.g., for progress updates)


    # Additional methods and logic for your scripts

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = MainApp()
    mainApp.show()
    sys.exit(app.exec_())