from lxml import etree
from bs4 import BeautifulSoup


def strip_ns_prefix(tree):
    """ Remove namespace prefixes
        e.g. <con:soup-project ...> will be converted to <soup-project ...>
    """
    #xpath query for selecting all element nodes in namespace
    query = "descendant-or-self::*[namespace-uri()!='']"
    #for each element returned by the above xpath query...
    for element in tree.xpath(query):
        #replace element name with its local name
        element.tag = etree.QName(element).localname
    etree.cleanup_namespaces(tree)
    return tree


def get_xml_parser():
    """ Create a new xml parser and return
    """
    return etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')


def convert_xml_tostring(xml):
    """ Convert given xml to string
    """
    return etree.tostring(xml, encoding="utf-8", method="xml")


def convert_xml_soup(file_path):
    """ Read xml from the file provided and convert it to soup for processing
    """
    # Read copy buildtype XML configuration file
    xmldoc_root = None
    with open(file_path, 'r') as xml_file:
        xmldoc = etree.parse(xml_file)
        xmldoc_root = xmldoc.getroot()

    if xmldoc_root is None:
        # TODO: Add exception handling in future
        return False
    
    # strip namespaces
    xmldoc = strip_ns_prefix(xmldoc_root)
    # Convert to beautiful soup object
    soup = BeautifulSoup(etree.tostring(xmldoc), "lxml-xml")

    return soup


def get_server_credentials(soup):
    """ Get Users credentials
    """
    username = soup.find('username').text
    password = soup.find('password').text

    return (username, password)


def get_build_soup(soup):
    """ Get build soup
    """
    # Get Build configurations
    build = soup.find('request').text
    # Convert Build configurations to beautifulsoup
    build_soup = BeautifulSoup(build, "lxml-xml")

    return build_soup