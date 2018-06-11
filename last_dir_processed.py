import os
import time
import jenkins

import config


def all_subdirs_of(dir='.'):
    result = []
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if os.path.isdir(path):
            result.append(path)
    return result


# Get last build processed timestamp
last_timestamp = 0
with open(config.LAST_PROCESSED_TIMESTAMP_LOG, "r", newline="\n") as process_file:
    if os.path.getsize(process_file.name) > 0:
        last_timestamp = process_file.readline().strip()

latest_subdir = all_subdirs_of(config.SUB_DIR_OF)
recent_files = [item for item in latest_subdir if os.path.getmtime(item) > float(last_timestamp)]

# Connect to Jenkins
# NOTE: Might need to change this for TeamCity
server = jenkins.Jenkins(config.SERVER_URL, username=config.SERVER_USER, password=config.SERVER_PASSWORD)
for item in recent_files:
    job = item.split(os.sep)[-1]
    # Create a job and make a build
    # NOTE: Might need to change this for TeamCity
    job_exists = server.get_job_name(job)
    if not job_exists:
        print("Creating a new job:", job)
        server.create_job(job, jenkins.EMPTY_CONFIG_XML)
    print("Start new Build: ", job)
    server.build_job(job)

# jobs = server.get_jobs()
# print("Jobs: ", jobs)

# Write current timestamp in log file
with open("last_processed_timestamp.log", "w", newline="\n") as process_file:
    process_file.write(str(time.time()))
