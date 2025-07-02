import os
import joblib
from typing import Final
from dotenv import load_dotenv
from discord import Intents, Client, Message
# from functions.responses import get_response
from functions.keep_alive import keep_alive
from better_profanity import profanity
keep_alive()

load_dotenv()
TOKEN: Final[str] = os.getenv('discord-token')
# print(TOKEN)

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

# async def send_message(message: Message, user_message: str) -> None:
#     if not user_message:
#         print('(Message was empty because intents were not enabled probably)')
#         return

#     if user_message[0] == '?':
#         is_private = True
#     else: is_private = False

#     if is_private:
#         user_message = user_message[1:]

#     try:
#         response: str = get_response(user_message)
#         await message.author.send(response) if is_private else await message.channel.send(response)
#     except Exception as e:
#         print(e)

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

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    # print(f'[{channel}] {username}: "{user_message}"')
    # await send_message(message, user_message)

    content = message.content.lower()

    if profanity.contains_profanity(content):
        await message.delete()
        await message.author.send("Please refrain from using profanity.")
    if is_spam(content):
        await message.delete()
        await message.author.send("Please refrain from sending spam to the server.")

def main() -> None:
    try:
        client.run(TOKEN)
    except Exception as e:
        print("❌ Bot failed:", e)


if __name__ == '__main__':
    main()