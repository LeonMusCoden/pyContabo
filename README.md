# pyContabo
basic python wrapper for the [Contabo API](https://api.contabo.com).


This wrapper is currently incomplete. 
Everything in the "Compute Instances" category has been implemented. 
Some functions have not been tested yet: Instance.reinstall, Instance.cancel, Instances.create, and Snapshot.rollback.

## Example
```
from pyContabo.Contabo import contabo
cont = contabo("client_id", "client_secret", "api_user", "api_password")
instance = cont.Instances.get()[0]
print(f"IPv4:\t{instance.ipv4}\nCPU Cores:\t{instance.cpuCores}\nRAM:\t{instance.ramMb}\nDrive:\t{instance.diskMb} ({instance.productType})")
print(instance.Snapshots.Audits.get()[0].rawJson)
```

## TODO
- [X] Instances, Instances Audits, Instance Actions, Instance Actions Audits, Snapshots, Snapshots Audits
- [X] Images and Images Audits
- [X] Tags, Tag Assignments, Tags Audits, Tag Assignments Audits
- [X] Users, Roles, User Audits, Roles Audits
- [X] Secrets, Secrets Audits
- [ ] Logging
- [ ] Documentation
- [X] Better API key management (auto renewel and maybe get rid of global variables)
- [ ] More types to replace strings in function arguments
- [ ] Enable support to set `x-request-id` and `x-trace-id` for requests

