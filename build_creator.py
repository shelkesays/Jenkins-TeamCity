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
job_name = latest_subdir.split(os.sep)[1]

# Connect to Jenkins
server = jenkins.Jenkins("http://localhost:8080", username="srahul07", password="rahul")
server.create_job(job_name, jenkins.EMPTY_CONFIG_XML)
server.build_job(job_name)
