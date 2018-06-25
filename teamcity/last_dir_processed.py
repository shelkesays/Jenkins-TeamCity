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

# Read copy buildtype XML configuration file
xmldoc_root = None
with open(config.COPY_BUILDTYPE_XML, 'r') as xml_file:
    xmldoc = etree.parse(xml_file)
    xmldoc_root = xmldoc.getroot()
    
if xmldoc_root is not None:
    # Connect to Jenkins
    if recent_files:
        builders = []
        headers = {'Content-Type': 'application/xml'} # set what your server accepts
        xml_url = "{0}/httpAuth/app/rest/projects/id:{1}/buildTypes".format(config.SERVER_URL, config.PROJECT_ID)
        trigger_url = "{0}/app/rest/buildQueue".format(config.SERVER_URL)
        parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')

        # Read Enqueue build / Trigger build XML configuration file
        build_trigger = None
        with open(config.TRIGGER_BUILD_XML, 'r') as xml_file:
            xmldoc = etree.parse(xml_file)
            build_trigger = xmldoc.getroot()

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
                if response.status_code == requests.codes.ok and build_trigger is not None:
                    response_xml = etree.fromstring(response.text.encode('utf-8'), parser=parser)
                    source_buildtype_id = response_xml.get(config.SOURCE_TRIGGER_BUILD_ATTRIBUTE)
                    build = build_trigger
                    buildtype = build.find(config.TRIGGER_BUILDTYPE_ATTRIBUTE)
                    if buildtype is not None:
                        buildtype.attrib[config.TARGET_TRIGGER_BUILD_ATTRIBUTE] = source_buildtype_id
                    xmldoc = etree.tostring(build, encoding="utf-8", method="xml")
                    response = requests.post(trigger_url, data=xmldoc, headers=headers, 
                        auth=(config.SERVER_USER, config.SERVER_PASSWORD))
                    if response.status_code == requests.codes.ok:
                        print("Successfully triggered build for {0}".format(source_buildtype_id))
                    else:
                        print("Failed triggered build for {0}".format(source_buildtype_id))
else:
    print("No Updates to create new builds")

# Write current timestamp in log file
with open(config.LAST_PROCESSED_TIMESTAMP_LOG, "w") as process_file:
    process_file.write(str(time.time()))
