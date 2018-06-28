import os
import requests

import config
from project_config_reader import (convert_xml_soup, get_xml_parser, convert_xml_tostring,  
        get_server_credentials, get_build_soup)
from utils import (all_subdirs_of, last_build_processed_timestamp, save_last_build_processed_timestamp)


if __name__ == "__main__":
    """ Read xml configuration file and extract credentials to teamcity and project build details
    """
    # Check if file exists, if it does not return false
    if not os.path.isfile(config.XML_PROJECT_CONFIG_FILE):
        # TODO: Add exception handling in future
        print("File {} does not exists".format(config.XML_PROJECT_CONFIG_FILE))
    
    soup = convert_xml_soup(config.XML_PROJECT_CONFIG_FILE)
    # Get method tag tree
    sub_tree = soup.find('method')
    # # Get request type
    # request_method = sub_tree['method']
    # Get request tree
    request = sub_tree.find('request')

    # # Get Endpoint for a request
    # endpoint = request.find('endpoint').text
    # # TODO: Check if endpoint is right
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

    if recent_files:
        headers = {'Content-Type': 'application/xml'} # set what your server accepts
        parser = get_xml_parser()

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
            response = requests.post(original_url, data=xmldoc, headers=headers, auth=auth)
            if response.status_code == requests.codes.ok:
                print("Successfully triggered build for {0}".format(job))
            else:
                print("Failed triggered build for {0}".format(job))
    else:
        print("No Updates to create new builds")
