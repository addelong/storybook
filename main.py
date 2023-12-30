from text import generate_story
from dialog import get_dialog_tracks
from images import generate_images
from video import create_video_from_images_and_dialogs
import asyncio


prompt = "Write a creative children's story that would take an average narrator about 5 minutes to read through."

async def main ():
    story = """In the mystical Willowby Wood, where the trees whispered secrets and the stars shone brighter than anywhere else, there lived a remarkably insightful fox named Felix. Felix, with his fiery red fur and emerald eyes, was not just any fox; he had the unique ability to understand the language of the wind, a gift passed down through generations of his family.

One crisp, autumn evening, as Felix was listening to the whispers of the wind, he heard a faint, urgent message unlike any he had encountered before. The wind spoke of a hidden treasure, an ancient artifact known as the Heart of the Forest, capable of preserving the beauty and magic of Willowby Wood forever. However, it was in danger of being lost to the greed of outsiders. Felix, with his keen fox instincts, knew he had to find it first.

Setting out under the moonlit sky, Felix embarked on his quest. He traveled through the thick underbrush, his fox senses guiding him through the dark. Along the way, he met an old badger named Bernard, wise and seasoned, who shared legends of the Heart of the Forest. Bernard, with his vast knowledge, offered to accompany Felix, and together they ventured deeper into the mysterious wood.

The journey was perilous, filled with challenges that tested Felix's cunning and Bernard's wisdom. They navigated through dense fog, where Felix's sharp fox eyes spotted hidden paths. They encountered a riddle-speaking owl, whose cryptic clues Felix deciphered with his understanding of the wind's language. The deeper they went, the more the wood seemed alive, guiding and testing them.

After days of travel, Felix and Bernard arrived at a secluded glade, where a stream of moonlight illuminated a pedestal in the center. There, resting quietly, was the Heart of the Forest, a stunning gem that pulsed with a gentle, green light. Felix, with his heart pounding, carefully approached it, but as he did, a shadow loomed over the glade.

A group of outsiders, led by a cunning raven, had followed them, intent on taking the Heart for themselves. Felix, with his quick fox reflexes, sprang into action, darting between the trees and leading them on a wild chase through the wood. Bernard, using his badger strength, created obstacles to slow the intruders down. The wood itself seemed to aid them, with branches and roots hindering the raven's group at every turn.

Finally, with the intruders outwitted and the Heart of the Forest safe, Felix and Bernard returned it to its rightful place. As soon as the gem touched the pedestal, a wave of energy swept through the wood. Trees grew taller, flowers bloomed brighter, and a sense of peace settled over Willowby Wood. The wind whispered a thank you, its voice full of gratitude and wonder.

As Felix and Bernard made their way back, they knew that their adventure had changed them. Felix, with his extraordinary fox abilities, had grown more connected to the wood than ever. Bernard, with his years of wisdom, had found a renewed sense of purpose. Together, they had saved Willowby Wood, and in return, it had given them a bond of friendship that would last a lifetime. The wind continued to whisper their story for years to come, a tale of courage, friendship, and the magic that lies in the heart of the forest. The end."""

    # Split story into paragraphs
    text_chunks = story.split("\n\n")

    # # Create the first text chunk with the first paragraph
    # first_chunk = paragraphs[0]

    # # Create subsequent chunks with two paragraphs each
    # remaining_chunks = ["\n\n".join(paragraphs[i:i+2]) for i in range(1, len(paragraphs), 2)]

    # # Combine the first chunk and remaining chunks
    # text_chunks = [first_chunk] + remaining_chunks

    await asyncio.gather(get_dialog_tracks(text_chunks), generate_images(text_chunks))

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