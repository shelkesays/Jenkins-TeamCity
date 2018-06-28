import os
import jenkins
import config


def all_subdirs_of(dir='.'):
    result = []
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if os.path.isdir(path):
            result.append(path)
    return result


# Check if last build was processed 2 days back
# If yes, start processing
# Else, exit / return 0

# latest_subdir = max(all_subdirs_of("tests"), key=os.path.getmtime)
latest_subdir = all_subdirs_of(config.SUB_DIR_OF)
job_file = open(config.PROCESSED_LOG, "r+")
lines = job_file.readlines()
# Strip all new lines
lines = map(lambda s: s.strip(), lines)
recent_files = []
if lines:
    recent_files = set(latest_subdir) - set(lines)
    recent_files = list(recent_files)
else:
    recent_files = recent_files + latest_subdir
# Close File
job_file.close()

# Connect to Jenkins
# NOTE: Might need to change this for TeamCity
server = jenkins.Jenkins(config.SERVER_URL, username=config.SERVER_USER, password=config.SERVER_PASSWORD)
job_file = open(config.PROCESSED_LOG, "a+")
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
    job_file.write(item + "\n")

job_file.close()
jobs = server.get_jobs()
print("Jobs: ", jobs)
