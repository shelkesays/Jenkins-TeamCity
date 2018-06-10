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

# Connect to Jenkins
server = jenkins.Jenkins("http://localhost:8080", username="srahul07", password="rahul")
server.create_job(latest_subdir, jenkins.EMPTY_CONFIG_XML)
server.build_job(latest_subdir)
