[![Build Status](https://travis-ci.org/dm-drogeriemarkt/nesbi.svg?branch=master)](https://travis-ci.org/dm-drogeriemarkt/nesbi)

nesbi
=======
Nesbi (Network Scan, Build and Import data) is a python-library which gives the possibility to scan defined network-ranges for network-devices, read out facts of them, build structured data and import them to a cmdb. At the moment the only supported cmdb is nsot.
The heart of nesbi is a config-file which makes it very flexible and generic.

How it works
=======
##### Nesbi is based on
* [napalm](https://github.com/napalm-automation/napalm)
* [nsot](https://github.com/dropbox/nsot)
* [nelsnmp](https://github.com/networklore/nelsnmp)

##### The following procedure is running with multiple threads per given network/location
1. network-range gets scanned with multiple threads for opened ports (=nesbi_port_scan variable)
2. reachable devices get scanned with nelsnmp to find out the device OS
3. napalm scans the device to get facts
4. dictionary/data for nsot-import gets built
5. data gets imported into nsot

##### Supported napalm-facts
All facts that are collected by the following napalm-functions are supported ([napalm documentation](https://napalm.readthedocs.io/en/latest/base.html)):
* get_facts()
* get_interfaces()
* get_interfaces_ip()
* get_snmp_information()

Installing nesbi
=======
```
$ pip install nesbi
```

##### Requirements
Requirements are defined in: [requirements.txt](requirements.txt).
Nesbi needs at least python 3.6 and doesn't support earlier versions.

Configuring nesbi
=======
### Defining the config
The very first step is defining the config file. The file contains of different parts.

##### cmdb-attributes
attribute-name | purpose 
--------------- | --------------- 
networks | *contains name, range and static key/value pairs which should be added to cmdb*
types | *map device-model dependent variables to cmdb attributes. Given model-name has to match the model-fact which gets read out by napalm.*
attr_functions | *map return-values of functions to cmdb attributes*
napalm | *map napalm variables to cmdb attributes*

attr_functions have to be: defined in config + python code and given as function argument when calling Nesbi().

If you need to exclude addresses (e.g. when using HSRP for high availability of gateway addresses) you can set the **exclude** attribute. It has to contain a list of IPv4 addresses. Network- and broadcast-addresses are excluded by default (for networks greater than /31).
It is possible to scan a single IP when defining the network-range with a **/32** subnet-mask.

##### application-attributes
Application-attributes can be given in the config file, as environment-variables (UPPER-CASE) or as function-arguments when calling nesbi(). Only attributes which have no default value and are required for nesbi to work correctly are marked as required.
**The variables get overwritten in the following order: Nesbi() > config > ENV > default**.

attribute-name | required | default | description 
-------------- | --------------- | --------------- | ---------------
nsot_url | yes | *not defined* | /
nsot_email | yes/no | *not defined* | required when using nsot_secret_key as nsot auth method
nsot_secret_key | yes/no | *not defined* | required when using nsot_secret_key as nsot auth method
nsot_auth_header | yes/no | X-NSoT-Email | required when using auth_header as nsot auth method
nsot_site_id | no | 1 | /
nsot_delete_objects | no | False | if set to True existing nsot-objects will be deleted before adding them
nesbi_network_driver | no | *not defined* | overwrites the network driver detected by nelsnmp
nesbi_username | yes | *not defined* | username for napalm
nesbi_password | yes | *not defined* | password for napalm
nesbi_snmp_version | yes | 2c | only v2c is supported at the moment
nesbi_snmp_community | yes | *not defined* | snmp community with read rights
nesbi_scan_ports | no | [22] | tcp-ports which should be scanned to get reachable network devices
nesbi_dry_run | no | False | if set to True nothing will be changed in the cmdb
nesbi_logging_level | no | info | valid log-levels are *notset, debug, info, warning, error, critical*
nesbi_logging_file | no | nesbi.log | custom log file name. If set to False no log file will be generated
nesbi_logging_to_stdout | no | False | /
nesbi_thread_limit | no | 5 | limits maximum parallel running threads

##### config example
[config.yml](examples/config.yml)

Using nesbi
=======
nesbi is a library which has to be used in pure python. As soon as your config-file is ready you can do something like:
[nesbi-example.py](examples/nesbi-example.py) and execute it:
```
python3 nesbi-example.py
```

Logging
=======
Nesbi uses the [logging-module](https://docs.python.org/3/library/logging.html) of the python standard-library. By default **nesbi_logging_file** is set to *nesbi.log* and the **nesbi_logging_level** is set to *info*. This will generate the log-file in the directory from where you run the python-script.

##### Sample Output
```
2018-04-13 21:34:55,463 -        nesbi.core.scanner -     INFO - Start port-scan for network/location mylocation
2018-04-13 21:34:55,504 -        nesbi.core.scanner -     INFO - 192.168.0.131 reachable at tcp-port 22
2018-04-13 21:34:55,505 -        nesbi.core.scanner -     INFO - 192.168.0.132 reachable at tcp-port 22
2018-04-13 21:34:55,505 -        nesbi.core.scanner -     INFO - 192.168.0.133 reachable at tcp-port 22
2018-04-13 21:34:58,520 -        nesbi.core.scanner -     INFO - Start device-scan for network/location mylocation
2018-04-13 21:35:05,521 -        nesbi.core.scanner -     INFO - 192.168.0.131: detected os "ios"
2018-04-13 21:35:06,047 -        nesbi.core.scanner -     INFO - 192.168.0.132: detected os "ios"
2018-04-13 21:35:06,301 -        nesbi.core.scanner -     INFO - 192.168.0.133: detected os "ios"
2018-04-13 21:35:21,402 -        nesbi.core.scanner -     INFO - Switch131 scanned with napalm
2018-04-13 21:35:22,308 -        nesbi.core.scanner -     INFO - Switch132 scanned with napalm
2018-04-13 21:35:22,363 -        nesbi.core.scanner -     INFO - Switch133 scanned with napalm
2018-04-13 21:37:00,808 -           nesbi.core.nsot -     INFO - Switch131 create dry-run
2018-04-13 21:37:00,809 -           nesbi.core.nsot -     INFO - Switch132 create dry-run
2018-04-13 21:37:00,809 -           nesbi.core.nsot -     INFO - Switch133 create dry-run
```

Contributing
=======
Fork and send a Pull Request. Thanks!

License
=======
Copyright (c) 2018 dm-drogerie markt GmbH & Co. KG, https://dm.de

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.