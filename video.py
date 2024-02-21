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

def create_video_from_images_and_dialogs(images_directory, image_extension, background_music, dialog_directory, dialog_extension, dialog_texts, output_video):

    fade_in_duration = 1  # Fade-in duration in seconds

    temp_video_file = "temp_video.mp4"
    temp_concat_file = "concat_list.txt"
    temp_music_file = "temp_music.mp3"

    # Copy background_music to ./bgmusic.mp3 to not have to worry about path separators
    subprocess.call(["cp", background_music, "./bgmusic.mp3"])
    background_music = "./bgmusic.mp3"

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
            segment_fade_out_duration = fade_in_duration

            # Extend the duration of the last image by 2 seconds
            if i == len(image_files) - 1:
                segment_duration += 4  # Extend duration for the last image
                segment_fade_out_duration += 2  # Extend fade-out duration for the last image

            segment_frames = int(segment_duration * 30)

            # Pre-process text to add line breaks if necessary
            wrapped_text = insert_line_breaks(text, max_line_length=65)  # Adjust max_line_length as needed


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
            "-vf", f"scale=2304:4032, zoompan=z='1+on/{segment_frames}*0.09':d={segment_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':fps=30:s=768x1344, fade=t=in:st=0:d={fade_in_duration}, fade=t=out:st={float(dialog_duration)+fade_in_duration-1}:d={segment_fade_out_duration}, drawbox=y=ih-360:color=black@0.5:t=fill:width=iw:height=240, drawtext=fontfile=./CaslonAntique.ttf:text='{wrapped_text}':fontcolor=white:fontsize=34:x=(w-tw)/2:y=h-360+(lh-20)",
            "-af", f"adelay={fade_in_duration * 1000}|{fade_in_duration * 1000}",  # Delay the audio
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
        "-filter_complex", f"[0:a]volume=0.5,afade=t=in:st=0:d=2,afade=t=out:st={float(video_duration)-2}:d=2[a]",
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
        "-b:a", "192k",  # Ensure a higher audio bitrate for the output
        "-shortest",
        "-y", output_video
    ])

    # Clean up temporary files
    os.remove(temp_video_file)
    os.remove(temp_concat_file)
    # os.remove(temp_concat_file_2)
    os.remove(temp_music_file)
    for i in range(len(image_files)):
        os.remove(f"segment_{i}.mp4")

# Example usage:
# create_video_from_images_and_dialogs("images", "jpg", "background.mp3", "dialogs", "mp3", "output.mp4")
