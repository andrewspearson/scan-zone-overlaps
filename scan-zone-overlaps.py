#!/usr/bin/env python3
import argparse
import getpass
import ipaddress
import urllib.request
from urllib.error import HTTPError
import ssl
import json


def api_call(method, host, endpoint, headers=None, data=None, proxy=None, verify=True):
    request = urllib.request.Request('https://' + host + endpoint)
    request.method = method
    request.add_header('Accept', 'application/json')
    context = ''
    if headers:
        for key, value in headers.items():
            request.add_header(key, value)
    if data:
        request.data = json.dumps(data).encode()
    if proxy:
        request.set_proxy(proxy, 'https')
    if verify is False:
        context = ssl._create_unverified_context()
    try:
        response = urllib.request.urlopen(request, context=context)
        return response
    except HTTPError as error:
        print('\nERROR: HTTP ' + str(error.code) + ' - https://' + host + endpoint)
        print(error.reason)


def normalize(ip_range):
    def error_msg(input_exception):
        print('ERROR: Input exception')
        print(input_exception)
        quit()
    ip_range = ip_range.split(',')
    ipList = []
    for item in ip_range:
        if '-' in str(item):
            ips = item.split('-')
            try:
                cidrs = ipaddress.summarize_address_range(ipaddress.IPv4Address(ips[0]), ipaddress.IPv4Address(ips[1]))
                ipList.append({'entry': item, 'networks': [cidr for cidr in cidrs]})
            except:
                error_msg(item)
        else:
            try:
                ipList.append({'entry': item, 'networks': [ipaddress.IPv4Network(item, False)]})
            except:
                error_msg(item)
    return ipList


def default_scan_zone_check(scan_zone):
    if scan_zone['id'] == '1' and \
            scan_zone['name'] == 'Default Scan Zone' and \
            len(scan_zone['ipList']) == 1 and \
            len(scan_zone['ipList'][0]['networks']) == 1 and \
            scan_zone['ipList'][0]['networks'][0] == ipaddress.IPv4Network('0.0.0.0/0'):
        return True


# Gather arguments. Proxy and ssl verification arguments are not required.
arguments = argparse.ArgumentParser(description='Tool to uncover overlaps in Tenable.SC Scan Zones')
arguments.add_argument(
    '-p',
    '--proxy',
    metavar='127.0.0.1:8080',
    default='',
    dest='proxy',
    help='HTTPS proxy'
)
arguments.add_argument(
    '-i',
    '--insecure',
    action='store_false',
    dest='verify',
    help='Disable SSL verification'
)
arguments = arguments.parse_args()

host = input('tenable.sc IP or hostname: ')
username = input('Username: ')
password = getpass.getpass()
proxy = arguments.proxy
verify = arguments.verify

# Login
response = api_call(
    method='GET',
    host=host,
    endpoint='/rest/system',
    proxy=proxy,
    verify=verify
)
cookie = response.headers['Set-Cookie'].split(';', 1)[0]
response = api_call(
    method='POST',
    host=host,
    endpoint='/rest/token',
    headers={
        "Cookie": cookie
    },
    data={
        "username": username,
        "password": password
    },
    proxy=proxy,
    verify=verify
)
token = json.load(response)['response']['token']
cookie = response.headers['Set-Cookie'].split(';', 1)[0]

current_user = api_call(
    method='GET',
    host=host,
    endpoint='/rest/currentUser',
    headers={
        "X-SecurityCenter": token,
        "Cookie": cookie
    },
    proxy=proxy,
    verify=verify
)

# Check if this is an Application Administrator user
current_user = json.load(current_user)
if current_user['response']['organization']['id'] != 0 or current_user['response']['role']['id'] != '1':
    print('\nWARNING: You are logging in with an account that is not a member of the \'Tenable.sc Administration\' '
          'organization and/or is not assigned the \'Administrator\' role. This script will continue to run, however '
          'results may be incomplete.')

# Pull Scan Zones
scan_zones = api_call(
    method='GET',
    host=host,
    endpoint='/rest/zone',
    headers={
        "X-SecurityCenter": token,
        "Cookie": cookie
    },
    proxy=proxy,
    verify=verify
)
scan_zones = json.load(scan_zones)

# Normalize ipList values into IPv4Network objects
for scan_zone in scan_zones['response']:
    scan_zone['ipList'] = normalize(scan_zone['ipList'])

# Find and report overlaps
for scan_zone1 in scan_zones['response']:
    if not default_scan_zone_check(scan_zone1):
        scan_zone1_id = scan_zone1['id']
        alerts = []
        print('\n')
        print('Overlaps in Scan Zone: ' + scan_zone1['name'])
        print('---------------------------------------------')
        for item1 in scan_zone1['ipList']:
            for network1 in item1['networks']:
                for scan_zone2 in scan_zones['response']:
                    if not default_scan_zone_check(scan_zone2):
                        if scan_zone1_id != scan_zone2['id']:
                            for item2 in scan_zone2['ipList']:
                                for network2 in item2['networks']:
                                    if network1.overlaps(network2):
                                        alert = scan_zone1['name'] + ' ' + item1['entry'] + ' overlaps with ' + \
                                                scan_zone2['name'] + ' ' + item2['entry']
                                        # break
                                        alerts.append(alert)
        alerts = list(set(alerts))
        alerts.sort()
        for alert in alerts:
            print(alert)

# Logout
api_call(
    method='DELETE',
    host=host,
    endpoint='/rest/token',
    headers={
        "X-SecurityCenter": token,
        "Cookie": cookie
    },
    proxy=proxy,
    verify=verify
)
