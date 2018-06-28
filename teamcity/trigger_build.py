import os
import requests

import config
from project_config_reader import (convert_xml_soup, convert_string_toxml, convert_xml_tostring,  
        get_server_credentials, get_build_soup, get_xml_root)
from utils import (all_subdirs_of, last_build_processed_timestamp, save_last_build_processed_timestamp)


if __name__ == "__main__":
    """ Read xml configuration file and extract credentials to teamcity and project build details
    """
    # Check if file exists, if it does not return false
    if not os.path.isfile(config.XML_PROJECT_CONFIG_FILE):
        # TODO: Add exception handling in future
        print("File {} does not exists".format(config.XML_PROJECT_CONFIG_FILE))
    
    soup = convert_xml_soup(config.XML_PROJECT_CONFIG_FILE)
    # Get build type url
    build_type_url = soup.find('resource')['path']
    # Get method tag tree
    sub_tree = soup.find('method')
    # # Get request type
    # request_method = sub_tree['method']
    # Get request tree
    request = sub_tree.find('request')

    # # Get Endpoint for a request
    endpoint = request.find('endpoint').text
    # TODO: Check if endpoint is right
    # Get Original URL
    original_url = request.find('originalUri').text
    # TODO: check if original url is right
    # get users authentication details
    auth = get_server_credentials(request)
    # TODO: Check if authentication details are right
    # Get Build configurations
    build_soup = get_build_soup(request)

    # Get all the sub directories of the directory path provided
    latest_subdir = all_subdirs_of(config.SUB_DIR_OF)
    # Get last build processed timestamp
    last_timestamp = last_build_processed_timestamp(config.LAST_PROCESSED_TIMESTAMP_LOG)
    # Get recent updated directories
    recent_files = [item for item in latest_subdir if os.path.getmtime(item) > float(last_timestamp)]

    xml_url = "{0}{1}".format(endpoint, build_type_url)
    trigger_url = "{0}/app/rest/buildQueue".format(endpoint)
    # Read Enqueue build / Trigger build XML configuration file
    build_trigger = get_xml_root(config.TRIGGER_BUILD_XML)
    
    if recent_files:
        headers = {'Content-Type': 'application/xml'} # set what your server accepts

        for item in recent_files:
            # Get the directory name from the path
            job = item.split(os.sep)[-1]
            # Set Buildtype id and name
            buildtype = build_soup.find('buildType')
            buildtype['id'] = job
            buildtype['name'] = job

            # Set parameters
            property_pr = build_soup.find('property')
            property_pr['value'] = job
            # Convert build xml to string
            xmldoc = str(build_soup)
            # Send request for build
            response = requests.post(xml_url, data=xmldoc, headers=headers, auth=auth)
            
            if response.status_code == requests.codes.ok and build_trigger is not None:
                response_xml = convert_string_toxml(response.text)
                source_buildtype_id = response_xml.get(config.SOURCE_TRIGGER_BUILD_ATTRIBUTE)
                buildtype = build_trigger.find(config.TRIGGER_BUILDTYPE_ATTRIBUTE)
                if buildtype is not None:
                    buildtype.attrib[config.TARGET_TRIGGER_BUILD_ATTRIBUTE] = source_buildtype_id
                xmldoc = convert_xml_tostring(build_trigger)  # etree.tostring(build, encoding="utf-8", method="xml")
                response = requests.post(trigger_url, data=xmldoc, headers=headers, auth=auth)
                if response.status_code == requests.codes.ok:
                    print("Successfully triggered build for {0}".format(source_buildtype_id))
                else:
                    print("Failed to trigger build for {0}".format(source_buildtype_id))
            else:
                print("Failed to create build for {0}".format(job))
    else:
        print("No Updates to create new builds")
