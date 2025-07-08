import os
import joblib
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message
from functions.keep_alive import keep_alive
# from functions.nsfw_check import is_nsfw
from functions.hindi_profanity import containsHindiSlang
import functions.mongo_connect  as mongo_connect
from better_profanity import profanity
import datetime
keep_alive()

load_dotenv()
TOKEN: Final[str] = os.getenv('discord-token')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

clf = joblib.load('spam_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')
def is_spam(text):
    text_vec = vectorizer.transform([text])
    prediction:bool = clf.predict(text_vec)[0]
    return prediction

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    author: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    content:str = message.content.lower()
    document_format = {"timestamp": datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"), 
                        "username": author,
                        "message":user_message,
                        "channel":channel
                        }

    if profanity.contains_profanity(content):
        try:
            mongo_connect.create("Profanity",document_format)
        except Exception as e:
            print("Bot failed:", e)
        await message.delete()
        await message.author.send(f"The message sent by you - \n\"{message.content}\" \nis not acceptable in our server.")
        await message.author.send("Please refrain from using profanity.\nRepeat offenders may be banned from the server")

    if containsHindiSlang(content):
        try:
            mongo_connect.create("Profanity",document_format)
        except Exception as e:
            print("Bot failed:", e)
        await message.delete()
        await message.author.send(f"The message sent by you - \n\"{message.content}\" \nis not acceptable in our server.")
        await message.author.send("Please refrain from using profanity.\nRepeat offenders may be banned from the server")

    if is_spam(content):
        try:
            mongo_connect.create("Spam",document_format)
        except Exception as e:
            print("Bot failed:", e)
        await message.delete()
        await message.author.send(f"The message sent by you - \n\"{message.content}\" \nis not acceptable in our server")
        await message.author.send("Please refrain from sending spam to the server.\nRepeat offenders may be banned from the server")

def main() -> None:
    try:
        client.run(TOKEN)
    except Exception as e:
        print("Bot failed:", e)


if __name__ == '__main__':
    main()