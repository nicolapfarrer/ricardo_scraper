import time,asyncio,schedule,os
from main import search_all_configs, update_previous_results, send_results
from dotenv import load_dotenv
#load env variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
SCHEDULE_TIME = os.getenv("SCHEDULE_TIME")
#devlare global variables
previous_results = {}
#define the job
async def main():
    update_previous_results(previous_results)
    await send_results(search_all_configs(previous_results))

#schedule the job
schedule.every().day.at(SCHEDULE_TIME).do(asyncio.run,main())

while True:
    schedule.run_pending()
    time.sleep(300) # wait 5 minutes

