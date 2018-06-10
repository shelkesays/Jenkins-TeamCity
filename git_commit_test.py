import os


def all_subdirs_of(dir='.'):
  result = []
  for item in os.listdir(dir):
    path = os.path.join(dir, item)
    if os.path.isdir():
      result.append(path)
  return result


print(all_subdirs_of())
