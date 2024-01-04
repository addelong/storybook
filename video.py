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

def create_video_from_images_and_dialogs(images_directory, image_extension, background_music, dialog_directory, dialog_extension, output_video):

    temp_video_file = "temp_video.mp4"
    temp_concat_file = "concat_list.txt"
    temp_music_file = "temp_music.mp3"

    image_files = sorted([f for f in os.listdir(images_directory) if f.endswith(image_extension)],
                        key=extract_number)

    dialog_files = sorted([f for f in os.listdir(dialog_directory) if f.endswith(dialog_extension)],
                        key=extract_number)

    if len(image_files) != len(dialog_files):
        raise ValueError("Mismatch in the number of images and dialog files")

    with open(temp_concat_file, "w") as concat_file:
        for i, (image, dialog) in enumerate(zip(image_files, dialog_files)):
            segment_file = f"segment_{i}.mp4"

            # Get duration of the dialog file
            try:
                cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(dialog_directory + "/" + dialog)

                dialog_duration = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode().strip()
            except subprocess.CalledProcessError as e:
                print("Error:", e)
                print("Command output:", e.output.decode())
                raise e

            subprocess.call([
                "ffmpeg",
                "-loop", "1",
                "-i", images_directory + "/" + image,
                "-i", dialog_directory + "/" + dialog,
                "-c:v", "libx264",
                "-tune", "stillimage",
                "-c:a", "aac",
                "-strict", "experimental",
                "-t", dialog_duration,  # Set the duration to match the dialog
                "-vf", f"fade=t=in:st=0:d=1, fade=t=out:st={float(dialog_duration)-1}:d=1",
                "-y", segment_file
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
        "-filter_complex", f"[0:a]volume=0.2,afade=t=in:st=0:d=2,afade=t=out:st={float(video_duration)-2}:d=2[a]",
        "-map", "[a]",
        "-y", temp_music_file
    ])

    # Combine video with background music
    subprocess.call([
        "ffmpeg",
        "-i", temp_video_file,
        "-i", temp_music_file,
        "-filter_complex", "[0:a][1:a]amerge=inputs=2[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        "-y", output_video
    ])

    # Clean up temporary files
    os.remove(temp_video_file)
    os.remove(temp_concat_file)
    os.remove(temp_music_file)
    for i in range(len(image_files)):
        os.remove(f"segment_{i}.mp4")

# Example usage:
# create_video_from_images_and_dialogs("images", "jpg", "background.mp3", "dialogs", "mp3", "output.mp4")
