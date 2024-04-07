from datetime import datetime, timedelta
import sched
import time

from crawler import COMBINATIONS, get_tokens, is_done, linear_regression, list_pkl, ps
from line import Line


def main():
    tokens = get_tokens()
    line = Line(tokens)
    message_tpl = ("Experiment status: {status}\n"
                   "Done count: {count} ({percent}%)\n"
                   "equation: Y = {a}X + {b}, with r = {r}\n"
                   "estimated ETA: {done_date} ({X} days from start)")
    status = "Done" if is_done() else f"Running {ps()} processes"
    a, b, start_date, r = linear_regression()
    X = (COMBINATIONS - b) / a
    done_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=X)
    done = len(list_pkl()) - 2
    percent = '{:.4f}'.format(done / (2 * 2 * 2 * 2 * 2 * 5 * 30) * 100)
    message = message_tpl.format(status=status, count=done, percent=percent, a=a, b=b, r=r, done_date=done_date, X=X)

    line.send_all(message)
    return status == "Done"


def void():
    pass


if __name__ == "__main__":
    s = sched.scheduler(time.time)
    while not main():
        s.enter(60 * 60 * 4, 1, void, ())
        s.run()

# to run this script in the background, use the following command:
# nohup python cron-vqc.py &
# to kill the process, use the following command:
# ps -ef | grep cron-vqc.py # pid is the second column
# kill -9 <PID>
# where <PID> is the process ID of cron-vqc.py
