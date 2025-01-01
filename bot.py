import asyncio,telegram,os
from dotenv import load_dotenv
#load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'config', '.env'))
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def send_message(message):
    bot = telegram.Bot(BOT_TOKEN)
    async with bot:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")

if __name__ == '__main__':
    asyncio.run(send_message("<a href='https://www.ricardo.ch/de/a/apple-ipad-tastatur-magic-keyboard-defekt-1277392920/'>Google</a>"))