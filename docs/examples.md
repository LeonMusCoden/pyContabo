## Daily Snapshot

This assumes the instance 0 has a limit of 1 snapshot. Every 86400s (= 1 day) the snapshot 0 gets deleted and a new one is created.

```python
from time import sleep
from pyContabo.Contabo import contabo

client_id="CLIENT_ID"
client_secret="CLIENT_SECRET"
api_user="API_USER"
api_password="API_PASSWORD"
cont = contabo(client_id, client_secret, api_user, api_password)

instance = cont.Instances.get()[0]

while 1:
    snapshots = instance.Snapshots.get()
    if len(snapshots) > 0:
        snapshots[0].delete()
        print("Deleted Snapshot")
    instance.Snapshots.create("AutoCreate", description="Created by pyContabo")
    print("Created Snapshot")
    sleep(86400)
```