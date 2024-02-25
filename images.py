import aiohttp
import os
import asyncio

url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

async def generate_images(text_chunks, positive_prompt, negative_prompt, stability_api_key):
    dir_path = "./out/images/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    session = aiohttp.ClientSession()

    image_coros = []
    for text_chunk in text_chunks:
        image_coros.append(generate_image(session, text_chunk, positive_prompt, negative_prompt, stability_api_key))
    
    responses = await asyncio.gather(*image_coros)

    for idx, response in enumerate(responses):

        if response.status != 200:
            raise Exception("Non-200 response: " + str(response.text))

        with open(f'./out/images/txt2img_{idx}.png', "wb") as f:
            f.write(await response.content.read())

    await session.close()

async def generate_image(session, text_chunk, positive_prompt, negative_prompt, stability_api_key):
    body = {
        "width": 1344,
        "height": 768,
        "style-preset": "photographic",
        "cfg_scale": 15,
        "text_prompts": [
            {
            "text": positive_prompt + text_chunk.replace(',', ''),
            "weight": 1
            },
            {
            "text": negative_prompt,
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