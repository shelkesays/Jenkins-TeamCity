from pyteamcity import pyteamcity as teamcity

# Testing teamcity

server = teamcity.TeamCity(server="localhost", port=8111, username="srahul07", password="rahul")

print("Current Jobs", server.get_projects())

builds = server.get_builds('MavenProject_Build')
print(builds)

# Build Job
server.trigger_build('MavenProject_Build')
