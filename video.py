import subprocess
import os
import math
import re
from typing import List

def extract_number(filename):
    """
    Extracts the number from the filename that follows an underscore,
    using regular expressions.
    """
    match = re.search(r'_(\d+)', filename)
    return int(match.group(1)) if match else 0

def insert_line_breaks(text, max_line_length):
    words = text.split()
    wrapped_text = ""
    current_line = ""

    for word in words:
        word = word.replace("'", "''")
        if len(current_line) + len(word) <= max_line_length:
            current_line += word + " "
        else:
            wrapped_text += current_line.strip() + "\n"
            current_line = word + " "

    wrapped_text += current_line.strip()
    return wrapped_text

def create_video_from_images_and_dialogs(images_directory, image_extension, background_music, dialog_directory, dialog_extension, dialog_texts, output_video):

    fade_in_duration = 1  # Fade-in duration in seconds

    temp_video_file = "temp_video.mp4"
    temp_video_file_with_audio = "temp_video_with_audio.mp4"  # Temporary file for video with audio
    temp_concat_file = "concat_list.txt"
    temp_music_file = "temp_music.mp3"
    prepend_video_clip = "intro.mp4"

    # Prepare background music reference if provided
    if background_music and os.path.exists(background_music):
        subprocess.call(["cp", background_music, "./bgmusic.mp3"])
        background_music = "./bgmusic.mp3"
    else:
        background_music = None

    image_files = sorted([f for f in os.listdir(images_directory) if f.endswith(image_extension)],
                        key=extract_number)

    dialog_files = sorted([f for f in os.listdir(dialog_directory) if f.endswith(dialog_extension)],
                        key=extract_number)

    # Enforce matching counts before starting any ffmpeg work
    if len(image_files) != len(dialog_files) or len(dialog_texts) != len(dialog_files):
        raise ValueError(f"Counts must match exactly. Images={len(image_files)} Dialogs={len(dialog_files)} DialogLines={len(dialog_texts)}")

    if len(image_files) != len(dialog_files):
        raise ValueError("Mismatch in the number of images and dialog files. Aborting compile.")

    created_segments = []
    with open(temp_concat_file, "w") as concat_file:
        for i, (image, dialog, text) in enumerate(zip(image_files, dialog_files, dialog_texts)):
            segment_file = f"segment_{i}.mp4"

            # Get duration of the dialog file
            try:
                cmd_list = [
                    "ffprobe", "-i", dialog_directory + "/" + dialog,
                    "-show_entries", "format=duration",
                    "-v", "quiet",
                    "-of", "csv=p=0",
                ]
                dialog_duration = subprocess.check_output(cmd_list, stderr=subprocess.STDOUT).decode().strip()
            except subprocess.CalledProcessError as e:
                print("Error:", e)
                print("Command output:", e.output.decode())
                raise e
            
            segment_duration = float(dialog_duration) + fade_in_duration
            segment_fade_out_duration = fade_in_duration

            # Extend the duration of the last image by 2 seconds
            if i == len(image_files) - 1:
                segment_duration += 4  # Extend duration for the last image
                segment_fade_out_duration += 2  # Extend fade-out duration for the last image

            segment_frames = int(segment_duration * 30)

            # Pre-process text to add line breaks if necessary
            wrapped_text = insert_line_breaks(text, max_line_length=48)


            subprocess.call([
            "ffmpeg",
            "-loop", "1",
            "-i", images_directory + "/" + image,
            "-i", dialog_directory + "/" + dialog,
            "-framerate", "30",
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",  # Set audio bitrate
            "-ar", "48000",  # Set audio sample rate
            "-strict", "experimental",
            "-t", str(segment_duration),  # Updated duration
            # add this to the end of the following line to add text to the video
            # , drawbox=y=ih-240:color=black@0.5:t=fill:width=iw:height=120, drawtext=fontfile=/WINDOWS/fonts/ITCKRIST.TTF:text='{wrapped_text}':fontcolor=white:fontsize=24:x=(w-tw)/2:y=h-240+(lh-10)
            "-vf", f"scale=4032:2304, zoompan=z='1+on/{segment_frames}*0.09':d={segment_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps=30:s=1344x768, fade=t=in:st=0:d={fade_in_duration}, fade=t=out:st={float(dialog_duration)+fade_in_duration-1}:d={segment_fade_out_duration}, drawbox=y=ih-200:color=black@0.35:t=fill:width=iw-160:height=160:x=80, drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{wrapped_text}':fontcolor=white:fontsize=30:x=(w-tw)/2:y=h-200+(lh-20)",
            # Make dialog louder relative to bgm later by normalizing per segment
            "-af", f"adelay={fade_in_duration * 1000}|{fade_in_duration * 1000},volume=1.35",
            "-y", segment_file
        ])
            concat_file.write(f"file '{segment_file}'\n")
            created_segments.append(segment_file)

    # Concatenate all segments
    subprocess.call([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", temp_concat_file,
        "-c", "copy",
        "-y", temp_video_file
    ])

    # Prepare background music (optional)
    if background_music:
        cmd_bgm = [
            "ffprobe", "-i", background_music,
            "-show_entries", "format=duration",
            "-v", "quiet",
            "-of", "csv=p=0",
        ]
        bg_music_duration = subprocess.check_output(cmd_bgm).decode().strip()

        cmd_vid = [
            "ffprobe", "-i", temp_video_file,
            "-show_entries", "format=duration",
            "-v", "quiet",
            "-of", "csv=p=0",
        ]
        video_duration = subprocess.check_output(cmd_vid).decode().strip()
        num_loops = math.ceil(float(video_duration) / float(bg_music_duration))

        subprocess.call([
            "ffmpeg",
            "-stream_loop", str(num_loops),
            "-i", background_music,
            "-t", video_duration,
            "-filter_complex", f"[0:a]volume=0.2,afade=t=in:st=0:d=2,afade=t=out:st={float(video_duration)-2}:d=2[a]",
            "-map", "[a]",
            "-y", temp_music_file
        ])

        # Combine video with background music using amix
        subprocess.call([
            "ffmpeg",
            "-i", temp_video_file,
            "-i", temp_music_file,
            "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=3[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-y", temp_video_file_with_audio
        ])
    else:
        # No background music; carry forward the original audio
        subprocess.call([
            "ffmpeg",
            "-i", temp_video_file,
            "-c", "copy",
            "-y", temp_video_file_with_audio
        ])

    overlay_video = "./overlay.mp4"
    overlay_duration = 5.5  # Duration of the overlay video in seconds
    fade_out_start = overlay_duration - 1  # Start fade out 1 second before the overlay ends
    fade_out_duration = 1  # Fade out duration in seconds

    subprocess.call([
        "ffmpeg",
        "-i", temp_video_file_with_audio,
        "-i", overlay_video,
        "-filter_complex",
        "[1:v]chromakey=0x00FF00:0.1:0.2,scale=iw*0.6:-2[overlay_faded];"  # Key out green and scale overlay smaller
        "[0:v][overlay_faded]overlay=(W-w)/2:(H-h)/2-220:eof_action=pass:format=auto;",  # Move overlay up to avoid subtitles
        "-map", "0:a",
        "-c:v", "libx264",  # You might adjust this depending on your needs
        "-c:a", "aac",      # AAC is a widely compatible audio codec
        "-strict", "experimental",
        "-r", "30",         # This sets the frame rate to 24 frames per second
         "-y", output_video
     ])

    # Clean up temporary files
    for f in [temp_video_file, temp_video_file_with_audio, temp_concat_file, temp_music_file]:
        try:
            if os.path.exists(f):
                os.remove(f)
        except Exception:
            pass
    for seg in created_segments:
        try:
            if os.path.exists(seg):
                os.remove(seg)
        except Exception:
            pass

# Example usage:
# create_video_from_images_and_dialogs("images", "jpg", "background.mp3", "dialogs", "mp3", "output.mp4")


def concat_runway_clips(clips: List[str], background_music: str, output_video: str):
    temp_concat_file = "concat_list.txt"
    temp_video_file = "temp_video.mp4"
    temp_video_file_with_audio = "temp_video_with_audio.mp4"
    temp_music_file = "temp_music.mp3"

    with open(temp_concat_file, "w") as f:
        for clip in clips:
            f.write(f"file '{os.path.abspath(clip)}'\n")

    subprocess.call([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", temp_concat_file,
        "-c", "copy",
        "-y", temp_video_file
    ])

    cmd_bgm = ["ffprobe","-i",background_music,"-show_entries","format=duration","-v","quiet","-of","csv=p=0"]
    bg_music_duration = subprocess.check_output(cmd_bgm).decode().strip()
    cmd_vid = ["ffprobe","-i",temp_video_file,"-show_entries","format=duration","-v","quiet","-of","csv=p=0"]
    video_duration = subprocess.check_output(cmd_vid).decode().strip()
    num_loops = math.ceil(float(video_duration) / float(bg_music_duration))

    subprocess.call([
        "ffmpeg",
        "-stream_loop", str(num_loops),
        "-i", background_music,
        "-t", video_duration,
        "-filter_complex", f"[0:a]volume=0.2,afade=t=in:st=0:d=2,afade=t=out:st={float(video_duration)-2}:d=2[a]",
        "-map", "[a]",
        "-y", temp_music_file
    ])

    subprocess.call([
        "ffmpeg",
        "-i", temp_video_file,
        "-i", temp_music_file,
        "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=3[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-y", temp_video_file_with_audio
    ])

    os.replace(temp_video_file_with_audio, output_video)
    os.remove(temp_video_file)
    os.remove(temp_music_file)
    os.remove(temp_concat_file)
