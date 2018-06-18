from pyteamcity import TeamCity
import requests

import config

# Testing teamcity

server = TeamCity(server=config.SERVER_HOST, port=config.SERVER_PORT, 
                    username=config.SERVER_USER, password=config.SERVER_PASSWORD)

print("Current Jobs", server.get_projects())

builds = server.get_builds('MavenProject_Build')
print(builds)

# Build Job
server.trigger_build('MavenProject_Build')
