import requests
import aiohttp
import asyncio
import pandas as pd
import os
import numpy as np
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.environ.get("API_KEY")
endpoint = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"
results = []
df = pd.read_excel("what_is_love.xlsx")
comments = np.array(df["original_comment"])
batch_size = 30
roundup_size = (len(comments) // batch_size) * batch_size
batch_comments = [
    batch.tolist() for batch in np.split(comments[:roundup_size], batch_size)
] + comments[roundup_size:].tolist()


async def fetch(session, url, comments):
    payload = {"q": comments, "target": "en"}
    async with session.post(url, json=payload) as response:
        return await response.json()


async def main():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *(fetch(session, endpoint, comments) for comments in batch_comments)
        )
        with open("data.json", "w", encoding="utf-8") as jsonfile:
            json.dump({"results": results}, jsonfile, ensure_ascii=False)


asyncio.run(main())