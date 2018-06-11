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
job_file = open("processed.log", "r+")
lines = job_file.readlines()
# Strip all new lines
lines =map(lambda s: s.strip(), lines)
recent_files = []
print(lines)
if lines:
    recent_files = set(latest_subdir) - set(lines)
    print(recent_files)
    recent_files = list(recent_files)
else:
    recent_files = recent_files + latest_subdir
# Close File
job_file.close()
#job_name = latest_subdir.split(os.sep)[1]

# Connect to Jenkins
# NOTE: Might need to change this for TeamCity
server = jenkins.Jenkins("http://localhost:8080", username="srahul07", password="rahul")
job_file = open("processed.log", "a+")
for item in recent_files:
    job = item.split(os.sep)[-1]
    print(job)
    # Create a job and make a build
    # NOTE: Might need to change this for TeamCity
    server.create_job(job, jenkins.EMPTY_CONFIG_XML)
    server.build_job(job)
job_file.write("\n".join(recent_files))

job_file.close()
jobs = server.get_jobs()
print("Jobs: ", jobs)
