import asyncio,telegram,os,logging
from dotenv import load_dotenv

#logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

#load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
logger.info("Loaded environment variables")

#send message
async def send_message(message,silent=True):
    if message is None:
        logger.warning("Attempted to send a None message")
        return
    try:
        bot = telegram.Bot(BOT_TOKEN)
        async with bot:
            await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML",disable_notification=silent)
    except Exception as e:
        logger.error(f"Failed to send message: {str(e)}")
        return

#run if called directly for testing purposes
if __name__ == '__main__':
    pass