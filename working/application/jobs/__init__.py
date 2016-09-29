# -*- coding: utf-8 -*-

import time
from threading import Thread

from concurrent.futures import ThreadPoolExecutor
import schedule

from hourlyjobs import hourly_jobs


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


def daemonlized_jobs(app):
    executor = ThreadPoolExecutor(max_workers=8)

    # X:45 start checkin job
    schedule.every().hour.at('00:45').do(hourly_jobs, app, executor)

    t = Thread(target=run_schedule)
    t.setDaemon(True)
    t.start()

    return executor
