# Teamcity configurations
SERVER_PROTCOL = "http"
SERVER_HOST = "localhost"
SERVER_PORT = 8111
SERVER_USER = "srahul07"
SERVER_PASSWORD = "rahul"

SERVER_URL = "{0}://{1}:{2}".format(SERVER_PROTCOL, SERVER_HOST, SERVER_PORT)

PROCESSED_LOG = "processed.log"
LAST_PROCESSED_TIMESTAMP_LOG = "last_processed_timestamp.log"
SUB_DIR_OF = "tests"

COPY_BUILDTYPE_XML = "copybuildtype.xml"
TRIGGER_BUILD_XML = "triggerbuild.xml"
PROJECT_ID = "XmlImport"
SOURCE_ATTRIBUTE = "sourceBuildTypeLocator"
TARGET_ATTRIBUTE = "name"
SOURCE_BUILD_TYPE_ID = "XmlImport_Template"  # "XmlImport_Builder"
TRIGGER_BUILDTYPE_ATTRIBUTE = "buildType"
SOURCE_TRIGGER_BUILD_ATTRIBUTE = "id"
TARGET_TRIGGER_BUILD_ATTRIBUTE = "id"

# Project configuration in xml
XML_PROJECT_CONFIG_FILE = "project_config.xml"
