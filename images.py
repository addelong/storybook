import aiohttp
import os
import asyncio

BASE_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0"
TXT2IMG_URL = f"{BASE_URL}/text-to-image"
IMG2IMG_URL = f"{BASE_URL}/image-to-image"

async def generate_images(text_chunks, positive_prompt, negative_prompt, stability_api_key, seed: int | None = None, reference_image_path: str | None = None, image_strength: float = 0.7):
    dir_path = "./out/images/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    session = aiohttp.ClientSession()

    image_coros = []
    for text_chunk in text_chunks:
        image_coros.append(
            generate_image(
                session,
                text_chunk,
                positive_prompt,
                negative_prompt,
                stability_api_key,
                seed,
                reference_image_path,
                image_strength,
            )
        )
    
    responses = await asyncio.gather(*image_coros)

    for idx, response in enumerate(responses):

        if response.status != 200:
            raise Exception("Non-200 response: " + str(response))

        with open(f'./out/images/txt2img_{idx}.png', "wb") as f:
            f.write(await response.content.read())

    await session.close()

async def generate_image(session, text_chunk, positive_prompt, negative_prompt, stability_api_key, seed: int | None, reference_image_path: str | None, image_strength: float):
    # Normalize Authorization header value
    auth_header = stability_api_key if stability_api_key.startswith("Bearer ") else f"Bearer {stability_api_key}"

    if reference_image_path and os.path.exists(reference_image_path):
        # image-to-image flow (multipart) tuned for GUI (portrait)
        form = aiohttp.FormData()
        form.add_field("image_strength", str(image_strength))
        form.add_field("cfg_scale", str(8))
        form.add_field("width", str(768))
        form.add_field("height", str(1344))
        if seed is not None:
            form.add_field("seed", str(seed))
        form.add_field("text_prompts[0][text]", (positive_prompt + text_chunk.replace(',', '')))
        form.add_field("text_prompts[0][weight]", "1")
        form.add_field("text_prompts[1][text]", negative_prompt)
        form.add_field("text_prompts[1][weight]", "-1")
        with open(reference_image_path, "rb") as fp:
            form.add_field("init_image", fp, filename=os.path.basename(reference_image_path), content_type="image/png")

        headers = {
            "Accept": "image/png",
            "Authorization": auth_header,
        }
        return await session.post(IMG2IMG_URL, data=form, headers=headers)
    else:
        # text-to-image flow (JSON) tuned for GUI (portrait)
        body = {
            "width": 768,
            "height": 1344,
            "style-preset": "photographic",
            "cfg_scale": 8,
            "text_prompts": [
                {
                    "text": positive_prompt + text_chunk.replace(',', ''),
                    "weight": 1,
                },
                {
                    "text": negative_prompt,
                    "weight": -1,
                },
            ],
        }

        if seed is not None:
            body["seed"] = seed

        headers = {
            "Accept": "image/png",
            "Content-Type": "application/json",
            "Authorization": auth_header,
        }
        return await session.post(TXT2IMG_URL, json=body, headers=headers)