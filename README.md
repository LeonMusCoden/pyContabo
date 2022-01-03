# pyContabo
basic python wrapper for the [Contabo API](https://api.contabo.com).

This wrapper is currently incomplete.
Everything in the "Compute Instances" category has been implemented.
Some functions have not been tested yet: Instance.reinstall, Instance.cancel, and Instances.create.
## Example 
```
from pyContabo.ComputeInstances import computeInstances
comp = computeInstances("client_id", "client_secret", "api_user", "api_password")
instance = comp.Instances.get()[0]
print(f"IPv4:\t{instance.ipv4}\nCPU Cores:\t{instance.cpuCores}\nRAM:\t{instance.ramMb}\nDrive:\t{instance.diskMb} ({instance.productType})")
print(instance.Snapshots.Audits.get()[0].rawJson)
```
