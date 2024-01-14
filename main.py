from text import generate_story
from dialog import get_dialog_tracks
from images import generate_images
from video import create_video_from_images_and_dialogs
import asyncio


prompt = "Write a creative children's story that would take an average narrator about 5 minutes to read through."

async def main ():
    story = """A towering tree in a moonlit forest, its branches glowing softly.

In a moonlit forest stands the Night Tree, ancient and magical, with branches that hold whispered secrets.

An owl, a rabbit, and a deer, illuminated by the tree's glow, gather in anticipation.

A wise owl, a curious rabbit, and a timid deer gather at the Night Tree. They sense the magic of the night unfolding.

The Night Tree's branches light up with radiant orbs, casting a gentle glow on the forest floor.

The Night Tree comes alive with radiant orbs, lighting up the forest. The animals watch, their eyes reflecting the tree's soft light.

A child, Alex, dressed in pajamas, steps into the clearing, eyes filled with wonder at the glowing tree.

Alex, a young child in pajamas, steps into the clearing. The glowing Night Tree captures Alex's imagination.

Alex and the animals sit together, sharing stories under the Night Tree's enchanting light.

Under the Night Tree, Alex and the animal friends share enchanting stories. The night air is filled with tales of adventure and wonder.

The Night Tree at dawn, its light fading, as Alex waves goodbye to the animals.

As dawn breaks, the Night Tree's light fades. Alex, with a heart full of stories, waves goodbye to the forest friends. The end.
"""

    # Split the story into lines, separated by two newlines. Separate them into two sets.
    # The first set contains the 1st, 3rd, 5th, etc. lines, and the second set contains the 2nd, 4th, 6th, etc. lines.
    # The first set is the image descriptions, and the second set is the dialog.
    paragraphs = story.split("\n\n")
    image_descriptions = paragraphs[::2]
    dialog = paragraphs[1::2]

    # # Create the first text chunk with the first paragraph
    # first_chunk = paragraphs[0]

    # # Create subsequent chunks with two paragraphs each
    # remaining_chunks = ["\n\n".join(paragraphs[i:i+2]) for i in range(1, len(paragraphs), 2)]

    # # Combine the first chunk and remaining chunks
    # text_chunks = [first_chunk] + remaining_chunks

    await asyncio.gather(get_dialog_tracks(dialog), generate_images(image_descriptions))
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