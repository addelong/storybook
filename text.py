import openai
from creds import openai_api_key

openai.api_key = openai_api_key

async def generate_story (prompt):
    response = await openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].text