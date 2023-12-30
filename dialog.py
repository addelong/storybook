import aiohttp
import os
from creds import elevenlabs_api_key, voice_model_id


async def get_dialog_tracks(text_chunks):
    dir_path = "./out/dialog/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for idx, text_chunk in enumerate(text_chunks):
        await generate_dialog_track(text_chunk, idx)


async def generate_dialog_track(text_chunk, idx):
    # Set the API endpoint URL
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_model_id}"

    session = aiohttp.ClientSession()

    # Set the request headers
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_api_key
    }

    # Set the request payload
    payload = {
        "text": text_chunk
    }

    # Send the POST request
    response = await session.post(url, json=payload, headers=headers)

    # Check if the ClientResponse was successful
    if response.status == 200:
        # Write the audio file to disk and return the file path
        with open(f"./out/dialog/dialog_{idx}.mp3", "wb") as f:
            f.write(await response.read())

        await session.close()
        
    else:
        # Raise an exception if the request failed
        raise Exception("Failed to generate dialog track: {}".format(response.text))
        
    
