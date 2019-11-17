import time
import random
import math
from decimal import Decimal
from pyfiglet import Figlet

from .celery import app
from .notify import notify

@app.task
def calculate(group_name, job_id):
    f = Figlet(font='standard')
    print("\nStarting Calculcation for {}...\n".format(group_name))
    speed = random.randint(50, 500)

    total = 10000000
    inside = 0
    for i in range(0, total):
        x2 = random.random()**2
        y2 = random.random()**2
        if math.sqrt(x2 + y2) < 1.0:
            inside += 1
        progress = 100 * i / total
        if i % (total / 100) == 0:
            notify(group_name, "Job {}: Making Progress! {}%".format(job_id, progress), 'progress', progress=progress, job_id=job_id)

    pi = (float(inside) / total) * 4
    print(f.renderText("\nPI is {}\n".format(pi)))

    notify(group_name, "Job {}: Job Done! {}%! The new Value of PI is: {}".format(job_id, 100, pi), 'progress', progress=100, job_id=job_id)


