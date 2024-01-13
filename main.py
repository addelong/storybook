from text import generate_story
from dialog import get_dialog_tracks
from images import generate_images
from video import create_video_from_images_and_dialogs
import asyncio


prompt = "Write a creative children's story that would take an average narrator about 5 minutes to read through."

async def main ():
    story = """Riley lived in a quiet neighborhood, where each house had its own charm. Her favorite spot was the big oak tree in her front yard, perfect for daydreaming and adventures.

One windy afternoon, while playing near the tree, Riley spotted something glistening in the grass. It was a small, golden key with intricate symbols etched onto its surface. Intrigued, Riley picked it up.

To her surprise, the key began to speak! "Hello, Riley," it said in a warm, friendly voice. "I'm Kay, the talking key. I've been waiting for a brave soul to find me." Riley's eyes widened in wonder. A talking key!

Kay explained that it unlocked a secret box hidden somewhere in Riley's house. Riley's heart raced with excitement at the thought of a hidden treasure. She eagerly asked, "Where can I find this box?" Kay responded, "It's closer than you think."

Riley dashed into her house, Kay in hand, searching high and low. She looked in cupboards, behind books, and even in the forgotten corners of the attic. The box remained elusive, but Kay kept her spirits up.

Then, Riley remembered an old chest in the basement, a relic from her great-grandfather's times. It was always locked, and no one in her family had found the key. Could this be the destination for Kay?

She hurried to the basement, dust swirling around the old chest. With a trembling hand, Riley inserted Kay into the lock. The key turned with a satisfying click, and the chest creaked open, revealing its secrets.

Inside the chest, Riley found old maps, strange gadgets, and a diary belonging to her great-grandfather. He had been an explorer! The diary was filled with tales of his adventures and discoveries.

Riley spent the evening reading the diary, captivated by the stories. Kay, now quiet, had found its purpose. Riley realized she had uncovered more than just a hidden box; she had discovered her family's adventurous past.

That night, as Riley went to bed, her mind buzzed with ideas for her own adventures. She knew that with Kay by her side, many more mysteries awaited. And the big oak tree outside seemed more magical than ever. The end."""

    # Split story into paragraphs
    text_chunks = story.split("\n\n")

    # # Create the first text chunk with the first paragraph
    # first_chunk = paragraphs[0]

    # # Create subsequent chunks with two paragraphs each
    # remaining_chunks = ["\n\n".join(paragraphs[i:i+2]) for i in range(1, len(paragraphs), 2)]

    # # Combine the first chunk and remaining chunks
    # text_chunks = [first_chunk] + remaining_chunks

    # await asyncio.gather(get_dialog_tracks(text_chunks), generate_images(text_chunks))
    await asyncio.gather(generate_images(text_chunks))

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