import getpass
from tenable.sc import TenableSC
import ipaddress


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


# Login
address = input('tenable.sc IP or hostname: ')
username = input('Username: ')
password = getpass.getpass()
sc = TenableSC(address)
sc.login(username, password)

# Check if this is an Application Administrator user
current_user = sc.current.user()
if current_user['organization']['id'] != 0 or current_user['role']['id'] != '1':
    print('\nWARNING: You are logging in with an account that is not a member of the \'Tenable.sc Administration\' '
          'organization and/or is not assigned the \'Administrator\' role. This script will continue to run, however '
          'results may be incomplete.')

# Pull Scan Zones
scan_zones = sc.scan_zones.list()

# Normalize ipList values into IPv4Network objects
for scan_zone in scan_zones:
    scan_zone['ipList'] = normalize(scan_zone['ipList'])

# Find and report overlaps
for scan_zone1 in scan_zones:
    if not default_scan_zone_check(scan_zone1):
        scan_zone1_id = scan_zone1['id']
        alerts = []
        print('\n')
        print('Overlaps in Scan Zone: ' + scan_zone1['name'])
        print('---------------------------------------------')
        for item1 in scan_zone1['ipList']:
            for network1 in item1['networks']:
                for scan_zone2 in scan_zones:
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
sc.logout()
