# -*- coding: utf-8 -*-
from .daocloud import daocloud_job


def hourly_jobs(app, executor):
    executor.submit(daocloud_job, app, executor)
