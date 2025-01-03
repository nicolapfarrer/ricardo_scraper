import time,asyncio,schedule,os,logging
from main import search_all_configs, update_previous_results, send_results
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
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME")
logger.info("Loaded environment variables")

#devlare global variables
previous_results = {}
#define the job
async def main():
    update_previous_results(previous_results)
    await send_results(search_all_configs(previous_results))
    logger.info("Job completed")

#schedule the job
schedule.every().day.at(SCHEDULE_TIME).do(asyncio.run,main())

while True:
    schedule.run_pending()
    time.sleep(300) # wait 5 minutes

