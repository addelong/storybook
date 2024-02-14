from text import generate_story
from dialog import get_dialog_tracks
from images import generate_images
from video import create_video_from_images_and_dialogs
import asyncio


prompt = "Write a creative children's story that would take an average narrator about 5 minutes to read through."

async def main ():
    story = """In the cozy village of Flufferton, nestled among cotton-candy clouds, lived Milo, a young bear with a head full of inventive ideas. Unlike other bears who were content with honey and fish, Milo dreamed of playing among the clouds.

One sunny day, inspired by the fluffy clouds above, Milo decided to build a machine that could create marshmallow clouds. He envisioned clouds so soft and sweet, everyone in Flufferton could enjoy a piece of the sky.

Milo set to work, gathering gears, levers, and, most importantly, marshmallows. He tinkered and toiled in his workshop, his paws covered in sticky sweetness as he assembled his marshmallow cloud machine.

After days of hard work, Milo unveiled his creation at the village square. The machine was a wonder to behold, with pipes whistling and gears turning, ready to transform marshmallows into clouds.

With a push of a button, the machine roared to life, puffing out clouds of marshmallows that floated gently over Flufferton. The villagers gathered, their mouths open in awe, as Milo's marshmallow clouds drifted down from the sky.

Children laughed and danced, catching marshmallows on their tongues. Adults, too, couldn't help but join in the fun, reminded of the joy of simple pleasures.

Milo watched, his heart swelling with pride. His dream of bringing the clouds down to earth had come true, and with it, he brought a day of joy and sweetness to Flufferton.

The marshmallow cloud machine became a village treasure, brought out for special occasions to fill the sky with sweetness. And Milo, the young bear with big dreams, became known as the inventor who turned the sky into a treat for all.

From that day on, the villagers of Flufferton looked up at the clouds not just with wonder, but with a taste of sweetness on their lips, all thanks to Milo's marvelous invention. The end."""

    # Split story into paragraphs
    text_chunks = story.split("\n\n")

    # # Create the first text chunk with the first paragraph
    # first_chunk = paragraphs[0]

    # # Create subsequent chunks with two paragraphs each
    # remaining_chunks = ["\n\n".join(paragraphs[i:i+2]) for i in range(1, len(paragraphs), 2)]

    # # Combine the first chunk and remaining chunks
    # text_chunks = [first_chunk] + remaining_chunks

    await asyncio.gather(get_dialog_tracks(text_chunks), generate_images(text_chunks))
    # await asyncio.gather(generate_images(text_chunks))

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