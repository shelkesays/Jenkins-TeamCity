import os
import jenkins


def all_subdirs_of(dir='.'):
  result = []
  for item in os.listdir(dir):
    path = os.path.join(dir, item)
    if os.path.isdir(path):
      result.append(path)
  return result


# latest_subdir = max(all_subdirs_of("tests"), key=os.path.getmtime)
latest_subdir = all_subdirs_of("tests")
job_file = open("processed.log", "a+")
lines = job_file.readlines()
recent_files = []
print(lines)
if lines:
    recent_files = set(latest_subdir) - set(lines)
    print(recent_files)
    recent_files = list(recent_files)
    print(recent_files)
else:
    recent_files = recent_files + latest_subdir
#job_name = latest_subdir.split(os.sep)[1]

# Connect to Jenkins
# NOTE: Might need to change this for TeamCity
server = jenkins.Jenkins("http://localhost:8080", username="srahul07", password="rahul")

for item in recent_files:
    job = item.split(os.sep)[-1]
    print(job)
    # Create a job and make a build
    # NOTE: Might need to change this for TeamCity
    server.create_job(job, jenkins.EMPTY_CONFIG_XML)
    server.build_job(job)
    job_file.write(item + "\n")

job_file.close()
jobs = server.get_jobs()
print("Jobs: ", jobs)
