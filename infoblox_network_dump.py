import requests
from ipaddress import *
import csv
import getpass
import logging

# Set up logging.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuration variables.
infoblox_ip = ''
username = ''
password = getpass.getpass()
base_url = 'https://{}/wapi/v1.0/'.format(infoblox_ip)

# Instantiate the lists. Change 2
networks = []
comments = []
first_ip = []
last_ip = []

# Attempt to make a connection to Infoblox. Change 3
try:
    response = requests.get(base_url + 'network?_return_type=json&_max_results=99999', auth=(username, password), verify=False).json()
except:
    raise

# Iterate through the networks we got back from Infoblox.
if response: # This doesn't work, needs to fix.
    for network in response:
        networks.append(network['network'])
        if network.get('comment'):
            logging.debug('Comment existed: {}'.format(network['comment']))
            comments.append(network['comment'])
        else:
            logging.debug('Appending blank comment.')
            comments.append('')

        # Defines a IPv4 network object with the network address and subnet mask returned from Infoblox.
        # Then we're going to get the first and last IP addresses and add them to the list.
        ip = IPv4Network(network['network'])
        first_ip.append(ip[0])
        last_ip.append(ip[-1])

    # Dump it all to a CSV.
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        rows = zip(networks, comments, first_ip, last_ip)
        for row in rows:
            writer.writerow(row)

    logging.debug('Networks: {}, Comments: {}, First IPs: {}, Last IPs: {}'.format(len(networks), len(comments), len(first_ip), len(last_ip)))
