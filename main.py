from text import generate_story
from dialog import get_dialog_tracks
from images import generate_images
from video import create_video_from_images_and_dialogs
import asyncio


prompt = "Write a creative children's story that would take an average narrator about 5 minutes to read through."

async def main ():
    story = """Noah discovered an old, crinkled map inside a book at the library, not a regular book, but one hidden behind others, covered in dust. The map was drawn in bright colors, with a big, candy castle at the end of a winding path through a forest of sweets.

With excitement bubbling inside him, Noah decided to follow the map the very next day. He packed a small backpack with essentials: a flashlight, a water bottle, and, of course, some snacks for the journey.

The path began just outside his town, marked by a signpost shaped like a lollipop. As Noah walked, the trees turned into candy canes and the bushes into clusters of cotton candy.

Noah reached a river that flowed with chocolate milk, where a boat made of a giant wafer waited. A friendly frog, wearing a tiny captain's hat, offered to guide Noah across. "Watch out for the sticky marshmallows," the frog warned as they set sail.

On the other side of the river, Noah encountered a garden of candy flowers. They were guarded by bees buzzing softly, collecting nectar from gumdrop buds. "Please, take one," buzzed a bee, offering Noah a sparkling jelly flower.

As he ventured further, Noah found himself in front of the Candy Castle, its walls glistening under the sun, made entirely of different shades of hard candy. The gate was locked, with a riddle inscribed above it: "Sweet and round, I grow on the ground, in the autumn, I am found."

Pondering the riddle, Noah realized the answer was "pumpkin." He said it out loud, and the gates swung open, revealing the courtyard filled with fountains of lemonade and benches made of licorice.

Inside the castle, Noah met the Candy Queen, a kind figure dressed in robes that shimmered like wrapping foil. She explained that the Candy Castle was in trouble; a spell had been cast on it, turning its once endless supply of sweets sour.

To break the spell, Noah needed to find the Heart of the Castle, a crystal hidden within a maze behind the castle. The Queen handed Noah a small, peppermint compass that would guide him to the heart.

Noah navigated the maze, following the peppermint compass, which ticked like a clock and smelled sweetly of mint. Finally, he found the crystal, glowing softly atop a pedestal.

As soon as Noah touched the crystal, a warm light spread throughout the maze, and the compass pulsed with a stronger glow. He hurried back to the Queen, crystal in hand.

With the Heart of the Castle restored, the spell was broken. The Candy Castle and its surroundings burst back into vibrant colors, sweets turning sweet once more.

The Candy Queen thanked Noah with a gift, a small bag of magical candy that would never run out. "You’ve saved the Candy Castle, Noah. You're always welcome here," she said, smiling.

Noah returned home, his backpack lighter but his heart full. He had saved the Candy Castle, and in his pocket, he carried the magical candy, a reminder of his incredible adventure.

Back in his room, Noah placed the never-ending candy on his desk and the map back inside the book. He knew he'd always remember the day he ventured beyond the ordinary, into a world where magic was real and kindness was the key to adventure. The end."""

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
    output_video="./final_video.mp4"
)

if __name__ == "__main__":
    asyncio.run(main())