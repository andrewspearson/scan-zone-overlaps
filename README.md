# scan-zone-overlaps
scan-zone-overlaps.py finds Tenable.SC Scan Zones with overlapping IP ranges.
## Requirements
* python3
## Installation
### Python virtual environment
```
$ git clone https://github.com/andrewspearson/scan-zone-overlaps.git /usr/local/bin/scan-zone-overlaps
```
Or
```
$ curl https://raw.githubusercontent.com/andrewspearson/scan-zone-overlaps/main/scan-zone-overlaps.py -O
```
## Usage
View the help menu
```
$ python3 scan-zone-overlaps.py -h
usage: scan-zone-overlaps.py [-h] [-p 127.0.0.1:8080] [-i]

Tool to uncover overlaps in Tenable.SC Scan Zones

optional arguments:
  -h, --help            show this help message and exit
  -p 127.0.0.1:8080, --proxy 127.0.0.1:8080
                        HTTPS proxy
  -i, --insecure        Disable SSL verification
```
Run the script
```
$ python3 scan-zone-overlaps.py -i
tenable.sc IP or hostname: tsc.corp.local
Username: admin
Password: 


Overlaps in Scan Zone: External zone
---------------------------------------------
External zone 192.0.2.0/24 overlaps with Test 3 192.0.2.1-192.0.2.128


Overlaps in Scan Zone: Internal zone
---------------------------------------------
Internal zone 10.0.0.0/8 overlaps with Test 1 10.0.0.1
Internal zone 10.0.0.0/8 overlaps with Test 2 10.0.0.5
Internal zone 192.168.0.0/16 overlaps with Test 1 192.168.0.2-192.168.0.252
Internal zone 192.168.0.0/16 overlaps with Test 2 192.168.3.1


Overlaps in Scan Zone: Test 1
---------------------------------------------
Test 1 10.0.0.1 overlaps with Internal zone 10.0.0.0/8
Test 1 192.168.0.2-192.168.0.252 overlaps with Internal zone 192.168.0.0/16


Overlaps in Scan Zone: Test 2
---------------------------------------------
Test 2 10.0.0.5 overlaps with Internal zone 10.0.0.0/8
Test 2 192.168.3.1 overlaps with Internal zone 192.168.0.0/16


Overlaps in Scan Zone: Test 3
---------------------------------------------
Test 3 192.0.2.1-192.0.2.128 overlaps with External zone 192.0.2.0/24

```
