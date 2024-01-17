import subprocess
import os
import math
import re

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

def create_video_from_images_and_dialogs(images_directory, image_extension, background_music, dialog_directory, dialog_extension, output_video, dialog_texts):

    fade_in_duration = 1  # Fade-in duration in seconds

    temp_video_file = "temp_video.mp4"
    temp_video_file_with_audio = "temp_video_with_audio.mp4"  # Temporary file for video with audio
    temp_concat_file = "concat_list.txt"
    temp_music_file = "temp_music.mp3"
    prepend_video_clip = "intro.mp4"

    image_files = sorted([f for f in os.listdir(images_directory) if f.endswith(image_extension)],
                        key=extract_number)

    dialog_files = sorted([f for f in os.listdir(dialog_directory) if f.endswith(dialog_extension)],
                        key=extract_number)

    if len(image_files) != len(dialog_files):
        raise ValueError("Mismatch in the number of images and dialog files")

    with open(temp_concat_file, "w") as concat_file:
        for i, (image, dialog, text) in enumerate(zip(image_files, dialog_files, dialog_texts)):
            segment_file = f"segment_{i}.mp4"

            # Get duration of the dialog file
            try:
                cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(dialog_directory + "/" + dialog)

                dialog_duration = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
            except subprocess.CalledProcessError as e:
                print("Error:", e)
                print("Command output:", e.output.decode())
                raise e
            
            segment_duration = float(dialog_duration) + fade_in_duration

            # Extend the duration of the last image by 2 seconds
            if i == len(image_files) - 1:
                segment_duration += 2  # Extend duration for the last image

            segment_frames = int(segment_duration * 30)

            # Pre-process text to add line breaks if necessary
            wrapped_text = insert_line_breaks(text, max_line_length=50)  # Adjust max_line_length as needed

            subprocess.call([
                "ffmpeg",
                "-loop", "1",
                "-framerate", "30",
                "-i", os.path.join(images_directory, image),  # The main image for the video
                "-i", os.path.join(dialog_directory, dialog),  # The dialog audio file
                "-t", str(segment_duration),  # Duration of the video segment
                "-filter_complex",
                f"[0:v]scale=4032:2304, "
                f"zoompan=z='1+on/{segment_frames}*0.05':d={segment_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps=30:s=1344x768,"
                f"fade=t=in:st=0:d={fade_in_duration}, "
                f"fade=t=out:st={float(dialog_duration)+fade_in_duration-1}:d={fade_in_duration}[base];"  # Base video
                f"movie=subtitlebg.png, scale=778:282[bg];"  # Load and scale subtitle background
                f"[base][bg]overlay=x=(W-w)/2:y=H-h-50:shortest=1[video];"  # Overlay subtitle background
                f"[video]drawtext=fontfile=/WINDOWS/fonts/segoepr.ttf:text='{wrapped_text}':fontcolor=black:fontsize=24:x=(w-tw)/2:y=H-th-282/2[final]",  # Apply subtitles
                "-map", "[final]",  # Map the final video stream with subtitles
                "-map", "1:a",  # Map the audio stream
                "-c:v", "libx264",
                "-tune", "stillimage",
                "-c:a", "aac",
                "-strict", "experimental",
                "-af", f"adelay={fade_in_duration * 1000}|{fade_in_duration * 1000}",  # Delay the audio to sync with video
                "-y", segment_file  # Output file
            ])


            concat_file.write(f"file '{segment_file}'\n")

    # Concatenate all segments
    subprocess.call([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", temp_concat_file,
        "-c", "copy",
        "-y", temp_video_file
    ])

    # Prepare background music
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(background_music)
    bg_music_duration = subprocess.check_output(cmd).decode().strip()

    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(temp_video_file)
    video_duration = subprocess.check_output(cmd).decode().strip()
    num_loops = math.ceil(float(video_duration) / float(bg_music_duration))

    subprocess.call([
        "ffmpeg",
        "-stream_loop", str(num_loops),
        "-i", background_music,
        "-t", video_duration,
        "-filter_complex", f"[0:a]volume=0.4,afade=t=in:st=0:d=2,afade=t=out:st={float(video_duration)-2}:d=2[a]",
        "-map", "[a]",
        "-y", temp_music_file
    ])

    # Combine video with background music using amix
    subprocess.call([
        "ffmpeg",
        "-i", temp_video_file,
        "-i", temp_music_file,
        "-filter_complex", "[1:a]volume=0.5[a1]; [0:a][a1]amix=inputs=2:duration=first:dropout_transition=3[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        "-y", temp_video_file_with_audio
    ])

    # Concatenate prepend video clip and the generated video
    # with open(temp_concat_file_2, "w") as concat_file:
    #     concat_file.write(f"file '{prepend_video_clip}'\n")
    #     concat_file.write(f"file '{temp_video_file_with_audio}'\n")

    subprocess.call([
        "ffmpeg",
        "-i", prepend_video_clip,
        "-i", temp_video_file_with_audio,
        "-filter_complex", "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",  # You might adjust this depending on your needs
        "-c:a", "aac",      # AAC is a widely compatible audio codec
        "-strict", "experimental",
        "-r", "30",         # This sets the frame rate to 24 frames per second
        "-y", output_video
    ])

    # Clean up temporary files
    os.remove(temp_video_file)
    os.remove(temp_video_file_with_audio)
    os.remove(temp_concat_file)
    # os.remove(temp_concat_file_2)
    os.remove(temp_music_file)
    for i in range(len(image_files)):
        os.remove(f"segment_{i}.mp4")

# Example usage:
# create_video_from_images_and_dialogs("images", "jpg", "background.mp3", "dialogs", "mp3", "output.mp4")
