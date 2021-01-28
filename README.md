# scan-zone-overlaps
scan-zone-overlaps.py finds Tenable.SC Scan Zones with overlapping IP ranges.
## Requirements
* python3
* [pyTenable](https://github.com/tenable/pyTenable)
## Installation
### Python virtual environment
```
$ git clone https://github.com/andrewspearson/scan-zone-overlaps.git /usr/local/bin/scan-zone-overlaps
$ python3 -m venv /usr/local/bin/scan-zone-overlaps/venv
$ . /usr/local/bin/scan-smuggler/venv/bin/activate
$ pip install -r requirements.txt
$ deactivate
```
## Usage
### Python virtual environment
```
$ cd /usr/local/bin
$ ./venv/bin/python scan-zone-overlaps.py
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
