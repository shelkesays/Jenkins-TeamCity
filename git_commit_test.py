import os


def all_subdirs_of(dir='.'):
  result = []
  for item in os.listdir(dir):
    path = os.path.join(dir, item)
    if os.path.isdir(path):
      result.append(path)
  return result


latest_subdir = max(all_subdirs_of("tests"), key=os.path.getmtime)
print(latest_subdir)
