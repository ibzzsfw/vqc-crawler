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
