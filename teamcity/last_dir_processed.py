import os
import time

from lxml import etree
import requests
from requests.auth import HTTPBasicAuth

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
with open(config.LAST_PROCESSED_TIMESTAMP_LOG, "r") as process_file:
    if os.path.getsize(process_file.name) > 0:
        last_timestamp = process_file.readline().strip()

latest_subdir = all_subdirs_of(config.SUB_DIR_OF)
recent_files = [item for item in latest_subdir if os.path.getmtime(item) > float(last_timestamp)]

# Read XML configuration file
xmldoc_root = None
with open(config.XML_CONFIG, 'r') as xml_file:
    xmldoc = etree.parse(xml_file)
    xmldoc_root = xmldoc.getroot()
    
if xmldoc_root is not None:
    # Connect to Jenkins
    if recent_files:
        builders = []
        headers = {'Content-Type': 'application/xml'} # set what your server accepts
        xml_url = "{0}/httpAuth/app/rest/projects/id:{1}/buildTypes".format(config.SERVER_URL, "XmlImport")
        for item in recent_files:
            job = item.split(os.sep)[-1]
            # Create a job and make a build
            build_type_id = xmldoc_root.get(config.SOURCE_ATTRIBUTE)
            if build_type_id and build_type_id == config.SOURCE_BUILD_TYPE_ID:
                build = xmldoc_root
                build.attrib[config.TARGET_ATTRIBUTE] = job
                xmldoc = etree.tostring(build, encoding="utf-8", method="xml")
                response = requests.post(xml_url, data=xmldoc, headers=headers, 
                    auth=(config.SERVER_USER, config.SERVER_PASSWORD))
else:
    print("No Updates to create new builds")

# Write current timestamp in log file
with open(config.LAST_PROCESSED_TIMESTAMP_LOG, "w") as process_file:
    process_file.write(str(time.time()))
