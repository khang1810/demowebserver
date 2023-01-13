from mobio.libs.schedule import SchedulerFactory
from dotenv import load_dotenv
load_dotenv()
from src.schedulers.clear_files_reacts import TestScheduler

if __name__ == '__main__':
    fac = SchedulerFactory()
    fac.add(TestScheduler(name="MyScheduler", redis_uri="redis://127.0.0.1:6379/0"))
    fac.run()