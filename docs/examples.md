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

Or using [schedule](https://pypi.org/project/schedule/):

```python
from time import sleep
import schedule
from pyContabo.Contabo import contabo

client_id="CLIENT_ID"
client_secret="CLIENT_SECRET"
api_user="API_USER"
api_password="API_PASSWORD"
cont = contabo(client_id, client_secret, api_user, api_password)

instance = cont.Instances.get()[0]

def take_snapshot():
    snapshots = instance.Snapshots.get()
    if len(snapshots) > 0: # No need to delete snapshot 0 if it doesn't exist
        snapshots[0].delete()
    instance.Snapshots.create("DailySnapshot", description="Created by pyContabo")

schedule.every().day.at("01:00").do(take_snapshot) # runs function at 1am

while True:
    schedule.run_pending()
    sleep(60) # wait one minute
```