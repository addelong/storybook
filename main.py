from text import generate_story
from dialog import get_dialog_tracks
from images import generate_images
from video import create_video_from_images_and_dialogs
import asyncio


prompt = "Write a creative children's story that would take an average narrator about 5 minutes to read through."

async def main ():
    story = """In a cozy town with tree-lined streets, there lived a bright and inquisitive girl named Charlotte. She had a keen interest in puzzles and mysteries.

One sunny morning, while Charlotte was walking to school, she noticed a curious pattern of colorful tiles on the sidewalk. The tiles formed a trail leading down the street.

Intrigued, Charlotte decided to follow the trail. Each tile had a unique design, and they seemed to be leading her somewhere specific.

As she followed the trail, it took her through parts of the town she had never explored. She passed by old bookshops, quaint cafés, and even a clock tower with chimes that echoed through the streets.

Eventually, the trail of tiles led Charlotte to a small park. In the center of the park was a mosaic on the ground, made of the same colorful tiles.

The mosaic was a large puzzle, depicting a map of the town with certain landmarks highlighted. Charlotte recognized the bookshop, the café, and the clock tower she had just passed.

Realizing this was a scavenger hunt, Charlotte felt a rush of excitement. She quickly made her way to each landmark, finding a small, hidden token at each location.

Each token had a letter on it. When Charlotte put all the tokens together, they spelled out a message: "DISCOVER."

With her newfound clues, Charlotte's curiosity was piqued even more. She started to see her town in a new light, full of hidden treasures and secrets to uncover.

The final destination led Charlotte back to her school. Here, she found a final token with a note from her teacher, congratulating her on solving the puzzle.

Charlotte's day had turned into an unexpected adventure. She had discovered new places in her town and solved a puzzle that brought her joy and excitement.

That night, as Charlotte reflected on her day, she realized the true treasure was in the journey and the new way she saw her town. She fell asleep with a smile, dreaming of her next adventure. The end."""

    # Split story into paragraphs
    text_chunks = story.split("\n\n")

    # # Create the first text chunk with the first paragraph
    # first_chunk = paragraphs[0]

    # # Create subsequent chunks with two paragraphs each
    # remaining_chunks = ["\n\n".join(paragraphs[i:i+2]) for i in range(1, len(paragraphs), 2)]

    # # Combine the first chunk and remaining chunks
    # text_chunks = [first_chunk] + remaining_chunks

    # await asyncio.gather(get_dialog_tracks(text_chunks), generate_images(text_chunks))
    # await asyncio.gather(generate_images(text_chunks))

    create_video_from_images_and_dialogs(
    images_directory="./out/images",
    image_extension="png",
    background_music="./bgmusic.mp3",
    dialog_directory="./out/dialog",
    dialog_extension="mp3",
    output_video="./final_video.mp4",
    dialog_texts=text_chunks
)

if __name__ == "__main__":
    asyncio.run(main())