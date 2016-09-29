# -*- coding: utf-8 -*-

import Queue
import random
import time

import requests

from ..models import DaoToken


def daocloud_appcheck(token, account, logger):
    api_url = 'https://openapi.daocloud.io/v1/apps'
    sleeping_apps = []

    try:
        resp = requests.get(api_url, headers={"Authorization": "token %s" % token})

        if 'Content-Type' in resp.headers.keys() and resp.headers['Content-Type'] == 'application/json':
            info = resp.json()
            if 'app' in info:
                for app in info['app']:
                    if 'state' in app and app['state'] == 'sleeping' and 'id' in app:
                        sleeping_apps.append(app['id'])

                        if 'name' in app:
                            logger.info('Trigger to restart %s for %s' % (app['name'], account))

    except Exception:
        pass
    finally:
        return {'token': token, 'ids': sleeping_apps}


def daocloud_apprestart(token, app_id):
    api_url = 'https://openapi.daocloud.io/v1/apps/%s/actions/start' % app_id
    try:
        requests.post(api_url, headers={"Authorization": "token %s" % token})
    except Exception:
        pass


def daocloud_job(app, executor):
    x_timeout = int(time.time())

    id_queue = Queue.Queue()
    logger = app.logger

    silence = random.randrange(60, 300)  # Delay for 1min~5min
    logger.info('Generally delay %d seconds ... ' % silence)
    time.sleep(silence)

    # Define callback for jobs
    def daocloud_callback(future):
        if future._state == 'FINISHED':
            id_queue.put(future._result)
        else:
            logger.error('Callback Error ...')

    # ORM objects need to be operated in the same thread under flask context ...
    with app.app_context():
        tokens = DaoToken.query.all()
        random.shuffle(tokens)

        for token_data in tokens:
            future = executor.submit(daocloud_appcheck, token_data.token, token_data.account, app.logger)
            future.add_done_callback(daocloud_callback)

        # Handle results for above requests
        delta = 0
        while delta < 55 * 60:
            try:
                result = id_queue.get(timeout=1)
                if result is not None:
                    token = result['token']
                    ids = result['ids']
                    for app_id in ids:
                        daocloud_apprestart(token, app_id)
            except Queue.Empty:
                pass
            except Exception, e:
                logger.error(e)
            finally:
                delta = int(time.time()) - x_timeout
