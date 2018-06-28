import os
import time


def all_subdirs_of(dir='.'):
    """ Read all the subdirectories of the directory path provided.
    dir: Path to the directory to be checked, default current directory
    """
    result = []
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if os.path.isdir(path):
            result.append(path)
    return result


def last_build_processed_timestamp(log_file):
    """ Read last build timestamp from the log file
    """
    # Get last build processed timestamp
    last_timestamp = 0
    with open(log_file, "r") as process_file:
        if os.path.getsize(process_file.name) > 0:
            last_timestamp = process_file.readline().strip()
    return last_timestamp


def save_last_build_processed_timestamp(log_file):
    """ Write current timestamp in log file
    """
    with open(log_file, "w") as process_file:
        process_file.write(str(time.time()))
