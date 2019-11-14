import time
import random

from .celery import app
from .notify import notify

@app.task
def calculate(group_name, job_id):
    print("Starting Calculcation for {}...".format(group_name))
    speed = random.randint(50, 500)
    for progress in range(0,101,1):
        notify(group_name, "Job {}: Making Progress! {}%".format(job_id, progress), 'progress', progress=progress, job_id=job_id)
        time.sleep(random.randint(0,50) / speed)

    notify(group_name, "Job {}: Job Done! {}%".format(job_id, progress), 'progress', progress=progress, job_id=job_id)

