import time,asyncio,schedule,os,logging
from datetime import datetime, timedelta
from scraper import search_all_configs, update_previous_results, send_results, load_previous_results, save_previous_results
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
logger.info(f"Scheduled job for {SCHEDULE_TIME}")

# Load previous results
previous_results = load_previous_results()

#helper function to calculate time until next run
def time_until_next_run(schedule_time):
    now = datetime.now()
    target_time = datetime.strptime(schedule_time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
    if target_time < now:
        target_time += timedelta(days=1)
    return (target_time - now).total_seconds()

#define the job
async def main():
    global previous_results
    previous_results = update_previous_results(previous_results)
    await send_results(search_all_configs(previous_results))
    save_previous_results(previous_results)
    logger.info("Job completed")

def run_main():
    asyncio.run(main())

if __name__ == '__main__':
    #schedule the job
    schedule.every().day.at(SCHEDULE_TIME).do(run_main)
    #run the pending jobs
    while True:
        schedule.run_pending()
        sleep_duration = time_until_next_run(SCHEDULE_TIME)
        sleep_duration_min = int(sleep_duration//60)
        logger.info(f"Hibernating for {sleep_duration_min} Minutes")
        time.sleep(sleep_duration) # wait until the next scheduled time

