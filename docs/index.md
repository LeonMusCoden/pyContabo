This site contains the project documentation for the
[pyContabo](https://github.com/xLeon-python/pyContabo) project that is a python API Client for the Contabo API.

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

## Demo
```py
from pyContabo.Contabo import contabo
cont = contabo("client_id", "client_secret", "api_user", "api_password")
instance = cont.Instances.get()[0]
print(f"IPv4:\t{instance.ipv4}\nCPU Cores:\t{instance.cpuCores}\nRAM:\t{instance.ramMb}\nDrive:\t{instance.diskMb} ({instance.productType})")
print(instance.Snapshots.Audits.get()[0].rawJson)
```

For more examples go to [Examples](examples.md)

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
- [X] Better API key management (auto renewel)
- [X] More types to replace strings in function arguments
- [X] Enable support to set `x-request-id` and `x-trace-id` for requests