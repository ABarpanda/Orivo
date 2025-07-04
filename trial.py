import discord
import aiohttp
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required to read message content & attachments

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore bot's own messages

    # Check if there are any attachments (images, files)
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith("image/"):
                print(f"🖼️ Image from {message.author}: {attachment.url}")

                # Optional: download the image
                await save_image(attachment)

async def save_image(attachment):
    # Create a directory to store images
    os.makedirs("imagesFromUsers", exist_ok=True)
    file_path = os.path.join("imagesFromUsers", attachment.filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(attachment.url) as resp:
            if resp.status == 200:
                with open(file_path, "wb") as f:
                    f.write(await resp.read())
                print(f"✅ Saved: {file_path}")
            else:
                print(f"❌ Failed to download image: HTTP {resp.status}")

client.run(os.getenv('discord-token'))
