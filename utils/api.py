import aiohttp
from config_data.config import Config, load_config
import json


config: Config = load_config('.env')


async def fetch_completion(content, message):
    messages = [
            {"role": "system", "content": content},
            {"role": "user", "content": message.text}
        ]
    endpoint = config.tg_bot.http_ai
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': messages,
    }
    data = json.dumps(data)
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, data=data) as response:
            return await response.json()
