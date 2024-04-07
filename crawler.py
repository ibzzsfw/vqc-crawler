"""_summary_
Crawler file for anything.
Please keep this file as isolated as possible.
Objective is to work on system but do not have to touch the main code.
"""

import os
import re
from datetime import datetime, timedelta

# resource
RESULT_PATH = "/home/testuser/project/automatic-vqc-design/results/result_automated"
EXCLUDE = "/old_result"
LOG_PATH = f"{RESULT_PATH}/log.txt"
TOKEN_PATH = "./tokens.txt"

# regex
DURATION_REGEX = (r"\[([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6})\] "
                  r"Duration: ([0-9]+:[0-9]+:[0-9]+\.[0-9]+)")

# value
EXPECTED_KEYWORD = "Done!"
COMBINATIONS = 2 * 2 * 2 * 2 * 2 * 5 * 30


def list_pkl():
    file_names = []
    for root, _, files in os.walk(RESULT_PATH):
        if EXCLUDE in root:
            continue
        for file in files:
            if file.endswith(".pkl"):
                file_names.append(file)
    return file_names


def is_done():
    with open(LOG_PATH) as f:
        log = f.read()
        return EXPECTED_KEYWORD in log


def get_tokens():
    with open(TOKEN_PATH) as f:
        return f.read().splitlines()


def ps():
    return os.popen("ps -ef | grep run.py").read().count("\n") - 1


# deprecated(Very unoptimized, use linear regression instead)
def eta():
    """
    TODO:
    [] Add more factor to this e.g. parameter size for specific combination (Weighted average
    [] Collect data to visualize the progress
    [] ...

    By the way, this job is not included in the Line message.
    """

    # get all durations in log
    durations = []
    with open(LOG_PATH) as f:
        log = f.read()
        for match in re.finditer(DURATION_REGEX, log):
            durations.append(match.group(2))

    # calculate average duration
    total_seconds = 0
    for duration in durations:
        hours, minutes, seconds = map(float, duration.split(":"))
        total_seconds += hours * 3600 + minutes * 60 + seconds
    avg_duration = total_seconds / len(durations)

    # handle parallelism
    eta_time = (COMBINATIONS - len(durations)) * avg_duration / len(durations)

    # calculate ETA
    eta_date = datetime.now() + timedelta(seconds=eta_time)
    eta_days = eta_time // (24 * 3600)

    return eta_date, eta_days, avg_duration


def linear_regression():
    done = {}  # {date as x: count as y} incremental count, date wise granularity
    count = 0
    start_date = None
    with open(LOG_PATH) as f:
        log = f.read()
        for match in re.finditer(DURATION_REGEX, log):
            count += 1
            date = match.group(1).split(" ")[0]
            if start_date is None:
                start_date = date
            done[date] = count

    # calculate linear regression per index (date count from start)
    y = list(done.values())
    y.insert(0, 0)
    x = list(range(len(y)))
    n = len(x)

    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_squared = sum([i ** 2 for i in x])
    sum_y_squared = sum([i ** 2 for i in y])
    sum_xy = sum([x[i] * y[i] for i in range(n)])

    # Check if denominator is zero
    if n * sum_x_squared - sum_x ** 2 == 0:
        raise ValueError("Cannot calculate linear regression: all x values are the same")

    # Y = aX + b with r as correlation coefficient
    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)
    b = (sum_y - a * sum_x) / n

    # Check if denominator is zero
    if (n * sum_x_squared - sum_x ** 2) * (n * sum_y_squared - sum_y ** 2) == 0:
        raise ValueError("Cannot calculate correlation coefficient: all x or y values are the same")

    r = (n * sum_xy - sum_x * sum_y) / ((n * sum_x_squared - sum_x ** 2) * (n * sum_y_squared - sum_y ** 2)) ** 0.5

    return a, b, start_date, r


if __name__ == "__main__":
    a, b, start_date, r = linear_regression()
    Y = COMBINATIONS
    X = (Y - b) / a
    done_date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=X)
    print("equation: Y = {:.4f}X + {:.4f}, with r = {:.4f}".format(a, b, r))
    print("ETA: {} ({:.0f} days from start)".format(done_date, X))
