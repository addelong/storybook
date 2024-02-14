from text import generate_story
from dialog import get_dialog_tracks
from images import generate_images
from video import create_video_from_images_and_dialogs
import asyncio


prompt = "Write a creative children's story that would take an average narrator about 5 minutes to read through."

async def main ():
    story = """In a sun-drenched valley surrounded by towering mountains, there lived a llama named Liam. Liam was not your average llama; his dreams were as high as the peaks around him, filled with roller coasters and ferris wheels.

Liam had spent his whole life in the valley, tending to the fields, but he had always longed for adventure. He'd heard stories of a place where the fun never stopped, a land of thrills and laughs known as Wonder Whirl Theme Park.

One morning, Liam decided it was time to take a vacation. He put on his favorite striped hat, packed a bag of his best snacks, and set off on a journey to the theme park he had always dreamed of visiting.

The journey was long, with winding roads that curled around the mountains like ribbons. But Liam's spirits were high, and he hummed a merry tune with every step, thinking of the exciting rides that awaited him.

As he reached the gates of Wonder Whirl, his eyes grew wide with amazement. The park was even more magnificent than he had imagined, with bright colors everywhere and the sound of laughter filling the air.

Liam wasted no time. He dashed to the nearest roller coaster, a twisting, turning beast named the Dragon's Tail. With his heart in his throat, Liam rode the coaster, feeling the wind rush against his woolly face, and for the first time, he felt like he was flying.

Next was the Giant Wheel, a towering ferris wheel that offered views across the entire park. From the top, Liam could see far across the land, and he felt as if he was part of a larger world, a world full of possibility.

The day turned into evening, and the park lit up with twinkling lights. Liam tried every game and rode every ride, his laughter joining the chorus of happy voices around him.

As the fireworks began to paint the night sky, Liam found a quiet spot to watch. He thought about his home in the valley and his adventure in Wonder Whirl. He felt a warmth in his heart, knowing that he'd have incredible stories to share.

When Liam returned home, he was greeted with hugs and eager questions. As he recounted his tales, he realized that while the theme park was an amazing place, it was the journey and the return that made his adventure complete.

Liam the Llama's vacation became a legend in the valley, inspiring others to dream big. And Liam himself? He kept the striped hat on a special hook, a reminder of the theme park vacation and the thrill of the Dragon's Tail, ready for whenever he felt the pull of adventure again. The end."""

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