class apiPermissions:
    def __init__(self, json):
        self.apiName = json["apiName"]
        self.actions = json["actions"]
