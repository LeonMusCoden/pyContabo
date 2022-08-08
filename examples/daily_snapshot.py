from time import sleep
import schedule
from pyContabo.Contabo import contabo

client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"
api_user = "API_USER"
api_password = "API_PASSWORD"
cont = contabo(client_id, client_secret, api_user, api_password)

instance = cont.Instances.get()[0]


def take_snapshot():
    snapshots = instance.Snapshots.get()
    if len(snapshots) > 0:
        snapshots[0].delete()
    instance.Snapshots.create("DailySnapshot", description="Created by pyContabo")


schedule.every().day.at("01:00").do(take_snapshot)

while True:
    schedule.run_pending()
    sleep(60)  # wait one minute
