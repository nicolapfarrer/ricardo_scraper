import asyncio,telegram,os
from dotenv import load_dotenv
#load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

#send message
async def send_message(message,silent=True):
    if message is None:
        return
    bot = telegram.Bot(BOT_TOKEN)
    async with bot:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML",disable_notification=silent)

#run if called directly for testing purposes
if __name__ == '__main__':
    pass