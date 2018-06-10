import jenkins

### Testing Jenkins

server = jenkins.Jenkins("http://localhost:8080", username="srahul07", password="rahul")

print("Jobs Count", server.jobs_count())

user = server.get_whoami()
version = server.get_version()
print("Hello {0} from Jenkins {1}".format(user['fullName'], version))

# Create a Job
server.create_job("Test", jenkins.EMPTY_CONFIG_XML)
jobs = server.get_jobs()
print("Current Jobs: ", jobs)
my_job = server.get_job_config("Test")
print("My Job: ", my_job)  # Print XML configurations
server.build_job("Test")
server.disable_job("Test")
server.copy_job("Test", "Test-copy")
server.enable_job("Test-copy")
server.reconfig_job("Test-copy", jenkins.RECONFIG_XML)

server.delete_job("Test")
server.delete_job("Test-copy")

# Build parameterized job
# requires creating and configuration the api-test job to accept 'param1' & 'param2'
# server.create_job("api-test", jenkins.EMPTY_CONFIG_XML)
# server.build_job('api-test', {'param1': 'Test value 1', 'param2': 'test value 2'})
# last_build_number = server.get_job_info('api-test')['lastCompletedBuild']['number']
# build_info = server.get_build_info('api-test', last_build_number)
# print(build_info)

# Create view
server.create_view("TEST_VIEW", jenkins.EMPTY_VIEW_CONFIG_XML)
view_config = server.get_view_config("TEST_VIEW")
views = server.get_views()
print("Views", views)

# get all jobs from the specific view
jobs = server.get_jobs(view_name="TEST_VIEW")
print("Jobs: ", jobs)

server.delete_view("TEST_VIEW")
print("Views:", views)

# Get all plugins
plugins = server.get_plugins()
print("Plugins: ", plugins)
