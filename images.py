import aiohttp
import os
import asyncio
from creds import stability_api_key

url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

async def generate_images(text_chunks):
    dir_path = "./out/images/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    session = aiohttp.ClientSession()

    image_coros = []
    for text_chunk in text_chunks:
        image_coros.append(generate_image(session, text_chunk))
    
    responses = await asyncio.gather(*image_coros)

    for idx, response in enumerate(responses):

        if response.status != 200:
            raise Exception("Non-200 response: " + str(response.text))

        with open(f'./out/images/txt2img_{idx}.png', "wb") as f:
            f.write(await response.content.read())

    await session.close()

async def generate_image(session, text_chunk):
    body = {
        "width": 1344,
        "height": 768,
        "style-preset": "digital-art",
        "cfg_scale": 10,
        "text_prompts": [
            {
            "text": "children's book, high quality, 3d render, digitally animated movie still, digital art, color, " + text_chunk,
            "weight": 1
            },
            {
            "text": "blurry, bad, sloppy, weird, low quality, dogs, dinosaurs",
            "weight": -1
            }
        ],
        }

    headers = {
        "Accept": "image/png",
        "Content-Type": "application/json",
        "Authorization": stability_api_key,
        }

    return await session.post(url, json=body, headers=headers)