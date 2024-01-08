from text import generate_story
from dialog import get_dialog_tracks
from images import generate_images
from video import create_video_from_images_and_dialogs
import asyncio


prompt = "Write a creative children's story that would take an average narrator about 5 minutes to read through."

async def main ():
    story = """It's night, and everything is so dark!

What if there are monsters? Or spooky shadows?

But wait! I have my trusty flashlight.

Oh no, a giant monster!

It's just my toys! Silly me.

The night isn't scary. It's just... different.

Goodnight, night. See you in the morning!"""

    # Split story into paragraphs
    text_chunks = story.split("\n\n")

    # # Create the first text chunk with the first paragraph
    # first_chunk = paragraphs[0]

    # # Create subsequent chunks with two paragraphs each
    # remaining_chunks = ["\n\n".join(paragraphs[i:i+2]) for i in range(1, len(paragraphs), 2)]

    # # Combine the first chunk and remaining chunks
    # text_chunks = [first_chunk] + remaining_chunks

    # await asyncio.gather(get_dialog_tracks(text_chunks), generate_images(text_chunks))
    # await asyncio.gather(get_dialog_tracks(text_chunks))
    # await generate_images(text_chunks)


    create_video_from_images_and_dialogs(
        images_directory="./out/images",
        image_extension="png",
        background_music="./bgmusic.mp3",
        dialog_directory="./out/dialog",
        dialog_extension="mp3",
        output_video="./final_video.mp4"
    )

if __name__ == "__main__":
    asyncio.run(main())