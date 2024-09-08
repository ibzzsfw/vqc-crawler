"""
Instructions:
- To run this script in the background: 
    nohup python cron-vqc.py &
- To kill the process: 
    ps -ef | grep cron-vqc.py  # PID is the second column
    kill -9 <PID>
    - where <PID> is the process ID of cron-vqc.py
"""

from datetime import datetime, timedelta
import sched
import time

from crawler import get_tokens, is_done, linear_regression, list_pkl, ps
from line import Line
from static import COMBINATIONS


def main():
    tokens = get_tokens()
    line = Line(tokens)
    message_tpl = ("Experiment status: {status}\n"
                   "Done count: {count} ({percent}%)\n"
                   "equation: Y = {a}X + {b}, with r = {r}\n"
                   "ETA: {done_date} ({X} days from start)")
    status = "Done" if is_done() else f"Running {ps()} processes"
    a, b, start_date, r, outage = linear_regression()
    X = (COMBINATIONS - b) / a + outage
    done_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=X)
    done = len(list_pkl()) - 2
    percent = '{:.4f}'.format(done / COMBINATIONS * 100)
    message = message_tpl.format(
        status=status, count=done, percent=percent, a=a, b=b, r=r, done_date=done_date, X=X)

    line.send_all(message)
    return status == "Done"


def void():
    pass


if __name__ == "__main__":
    print("Start cron job")
    s = sched.scheduler(time.time)
    while not main():
        s.enter(60 * 60 * 6, 1, void, ())
        s.run()
