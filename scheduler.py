from apscheduler.schedulers.background import BackgroundScheduler
import atexit

scheduler = BackgroundScheduler()
atexit.register(lambda: scheduler.shutdown())


def start():
    scheduler.start()


def add_job(func, time=60 * 60):
    scheduler.add_job(func=func, trigger='interval', seconds=time)
