# pyContabo
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

python API Client for the [Contabo API](https://api.contabo.com).

Contabo offers web hosting with dedicated servers, colocation, and VPS hosting plans.
Contabo API allows you to manage your resources using HTTP requests.

This Client aims to make using the API easier, for example with a simple-to-understand syntax and automatic authentication.

This client is unofficial.

[Documentation](https://xleon-python.github.io/pyContabo/)

## Installation

### Using pip
```sh
pip install git+https://github.com/xLeon-python/pyContabo.git
```
### Using setuptools
```sh
git clone https://github.com/xLeon-python/pyContabo.git
cd pyContabo
python3 setup.py install --user
```

## Example
```py
from pyContabo.Contabo import contabo
cont = contabo("client_id", "client_secret", "api_user", "api_password")
instance = cont.Instances.get()[0]
print(f"IPv4:\t{instance.ipv4}\nCPU Cores:\t{instance.cpuCores}\nRAM:\t{instance.ramMb}\nDrive:\t{instance.diskMb} ({instance.productType})")
print(instance.Snapshots.Audits.get()[0].rawJson)
```

## Support
### Testing
I can't test parts of this client because I only own a single VPS. Testing the code is highly appreciated!

The following parts have not been tested yet:
- Tags, Tag Assignments, Tags Audits, Tag Assignments Audits
- Users, Roles, User Audits, Roles Audits
- Secrets, Secrets Audits

### Contributing
pyContabo is supported on a volunteer basis. Pull requests or bug reports are welcome to optimize the code and fix errors.

[Open an issue](https://github.com/xLeon-python/pyContabo/issues/new)

[Create a pull request](https://github.com/xLeon-python/pyContabo/compare)

## TODO
- [X] Instances, Instances Audits, Instance Actions, Instance Actions Audits, Snapshots, Snapshots Audits
- [X] Images and Images Audits
- [X] Tags, Tag Assignments, Tags Audits, Tag Assignments Audits
- [X] Users, Roles, User Audits, Roles Audits
- [X] Secrets, Secrets Audits
- [ ] Object Storages, Object Storages Audits
- [ ] Private Networks, Private Networks Audits
- [ ] Logging
- [X] Documentation
- [X] Better API key management (auto renewel and maybe get rid of global variables)
- [X] More types to replace strings in function arguments
- [X] Enable support to set `x-request-id` and `x-trace-id` for requests

