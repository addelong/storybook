from text import generate_story
from dialog import get_dialog_tracks
from images import generate_images
from video import create_video_from_images_and_dialogs
import asyncio


prompt = "Write a creative children's story that would take an average narrator about 5 minutes to read through."

async def main ():
    story = """Frances, a young girl in cozy pajamas, holding a stuffed bear, stands reluctantly beside her bed.

It's bedtime for Frances, but she's not quite ready to sleep. She holds her stuffed bear, wishing for just a few more minutes of play.

Frances's room, filled with soft toys and moonlight streaming through the window.

Her room is a cozy haven, bathed in gentle moonlight. Soft toys are scattered around, each with its own bedtime story.

Frances looking out the window at the starry night sky, her expression thoughtful.

Frances peers out her window. The stars twinkle like tiny guides, leading her towards dreamland.

Her parents say goodnight and sweet dreams, a bedside lamp casting a warm glow.

Mom and Dad come in to tuck Frances in. They kiss her goodnight, leaving a soft glow from the bedside lamp.

Frances lying in bed, a faint smile on her face as she clutches her stuffed bear.

In her bed, Frances snuggles with her bear. She starts to feel sleepy, her eyes drifting shut.

The room in soft darkness with Frances sleeping peacefully, a nightlight casting a comforting glow.

Frances is now sound asleep, the nightlight casting a warm, comforting glow. Her room is quiet, and dreams await her in the peaceful night. The end."""

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
    # await generate_images(image_descriptions)


    create_video_from_images_and_dialogs(
        images_directory="./out/images",
        image_extension="png",
        background_music="./bgmusic.mp3",
        dialog_directory="./out/dialog",
        dialog_extension="mp3",
        dialog_texts=dialog,
        output_video="./final_video.mp4"
    )

if __name__ == "__main__":
    asyncio.run(main())