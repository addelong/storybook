import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QFileDialog, QProgressBar
# Import necessary functions from your other scripts
from dialog import get_dialog_tracks
from images import generate_images
from video import create_video_from_images_and_dialogs
from creds import stability_api_key, elevenlabs_api_key, voice_model_id

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # API Credentials Section
        self.api_keys_layout = QHBoxLayout()
        self.api_keys = {
            'Stability API Key': QLineEdit(),
            'ElevenLabs API Key': QLineEdit(),
            'Voice Model ID': QLineEdit()
        }
        # Set default values for API keys here
        self.api_keys['Stability API Key'].setText(stability_api_key if stability_api_key else 'your_stability_api_key')
        self.api_keys['ElevenLabs API Key'].setText(elevenlabs_api_key if elevenlabs_api_key else 'your_elevenlabs_api_key')
        self.api_keys['Voice Model ID'].setText(voice_model_id if voice_model_id else 'your_voice_model_id')  
        for label, line_edit in self.api_keys.items():
            self.api_keys_layout.addWidget(QLabel(label))
            self.api_keys_layout.addWidget(line_edit)
        self.layout.addLayout(self.api_keys_layout)

        # Story Text Section
        self.story_text = QTextEdit()
        self.story_text.setPlaceholderText("Enter your story here...")
        self.layout.addWidget(self.story_text)

        # Image Generation Text Section (Optional)
        self.image_text = QTextEdit()
        self.image_negative_text = QTextEdit()
        self.image_text.setText("beautiful, perfect quality, 3d animated movie still, pixar, digital art, color, coherent, uhd, detailed face, looks good, expressive, magical, ")
        self.image_negative_text.setText("blurry, bad, sloppy, incoherent, weird faces, messed up, weird hands, too many limbs or digits, anatomically incorrect, unnatural or creepy facial expression, generic or overused design, inconsistent scale or proportions, maniacal smiling")
        self.layout.addWidget(QLabel("Image Generation Prompt"))
        self.layout.addWidget(self.image_text)
        self.layout.addWidget(QLabel("Image Generation Negative Prompt"))
        self.layout.addWidget(self.image_negative_text)

        # Background Music Selection
        self.bgm_layout = QHBoxLayout()
        self.bgm_label = QLabel("Background Music:")
        self.bgm_file = QLineEdit()
        self.bgm_button = QPushButton("Browse")
        self.bgm_button.clicked.connect(self.browse_music)
        self.bgm_layout.addWidget(self.bgm_label)
        self.bgm_layout.addWidget(self.bgm_file)
        self.bgm_layout.addWidget(self.bgm_button)
        self.layout.addLayout(self.bgm_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        # Control Buttons
        self.buttons_layout = QHBoxLayout()
        self.generate_dialog_button = QPushButton("Generate Dialog")
        self.generate_dialog_button.clicked.connect(self.generate_dialog)
        self.generate_images_button = QPushButton("Generate Images")
        self.generate_images_button.clicked.connect(self.generate_images)
        self.compile_video_button = QPushButton("Compile Video")
        self.compile_video_button.clicked.connect(self.compile_video)
        self.buttons_layout.addWidget(self.generate_dialog_button)
        self.buttons_layout.addWidget(self.generate_images_button)
        self.buttons_layout.addWidget(self.compile_video_button)
        self.layout.addLayout(self.buttons_layout)

        # Set main layout
        self.setLayout(self.layout)
        self.setWindowTitle('Story to Video Converter')

    def browse_music(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Background Music", "", "Audio Files (*.mp3 *.wav)")
        if filename:
            self.bgm_file.setText(filename)

    def generate_dialog(self):
        # Split the story into lines, separated by two newlines. Separate them into two sets.
        # The first set contains the 1st, 3rd, 5th, etc. lines, and the second set contains the 2nd, 4th, 6th, etc. lines.
        # The first set is the image descriptions, and the second set is the dialog.
        story = self.story_text.toPlainText()
        paragraphs = story.split("\n\n")
        dialog = paragraphs[1::2]
        self.start_worker(get_dialog_tracks, dialog)

    def generate_images(self):
        # Split the story into lines, separated by two newlines. Separate them into two sets.
        # The first set contains the 1st, 3rd, 5th, etc. lines, and the second set contains the 2nd, 4th, 6th, etc. lines.
        # The first set is the image descriptions, and the second set is the dialog.
        story_text = self.story_text.toPlainText()
        paragraphs = story_text.split("\n\n")
        image_descriptions = paragraphs[::2]
        self.start_worker(generate_images, image_descriptions, self.image_text.toPlainText(), self.image_negative_text.toPlainText())

    def compile_video(self):
        self.start_worker(create_video_from_images_and_dialogs, "./out/images", "png", self.bgm_file.text(), "./out/dialog", "mp3", "./final_video.mp4")


    # Additional methods and logic for your scripts

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = MainApp()
    mainApp.show()
    sys.exit(app.exec_())