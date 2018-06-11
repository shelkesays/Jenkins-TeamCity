import os
import jenkins


def all_subdirs_of(dir='.'):
  result = []
  for item in os.listdir(dir):
    path = os.path.join(dir, item)
    if os.path.isdir(path):
      result.append(path)
  return result


latest_subdir = max(all_subdirs_of("tests"), key=os.path.getmtime)
job_file = open("processed.log", "a+")
lines = job_file.readlines()
print(lines)
recent_files = set(latest_subdir) - set(job_file)
print(recent_files)
recent_files = list(recent_files)
print(recent_files)
#job_name = latest_subdir.split(os.sep)[1]

# Connect to Jenkins
server = jenkins.Jenkins("http://localhost:8080", username="srahul07", password="rahul")

for item in recent_files:
    job = item.split(os.sep)[-1]
    print(job)
    server.create_job(job, jenkins.EMPTY_CONFIG_XML)
    server.build_job(job)
    job_file.write(item)

job_file.close()
jobs = server.get_jobs()
print("Jobs: ", jobs)
