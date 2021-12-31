class Audit:  # Class for the different sub classes

    def __init__(self, json):
        self.id = json["id"]
        self.action = json["action"]
        self.timestamp = json["timestamp"]
        self.tenantId = json["tenantId"]
        self.customerId = json["customerId"]
        self.changedBy = json["changedBy"]
        self.username = json["username"]
        self.requestId = json["requestId"]
        self.traceId = json["traceId"]
        try:  # Because some Audits don't have changes
            self.previous = json["changes"]["prev"]
            self.new = json["changes"]["new"]
        except KeyError:
            pass

        self.rawJson = json


class InstancesAudit(Audit):

    def __init__(self, json):
        super().__init__(json)
        self.instanceId = json["instanceId"]


class InstanceActionsAudit(Audit):

    def __init__(self, json):
        super().__init__(json)
        self.instanceId = json["instanceId"]


class SnapshotsAudit(Audit):

    def __init__(self, json):
        super().__init__(json)
        self.instanceId = json["instanceId"]
        self.snapshotId = json["snapshotId"]


class ImagesAudit(Audit):

    def __init__(self, json):
        super().__init__(json)
        self.imageId = json["imageId"]


class TagsAudit(Audit):

    def __init__(self, json):
        super().__init__(json)
        self.tagId = json["tagId"]


class TagAssignmentsAudit(Audit):

    def __init__(self, json):
        super().__init__(json)
        self.tagId = json["tagId"]
        self.resourceId = json["resourceId"]
        self.resourceType = json["resourceType"]


class UsersAudit(Audit):

    def __init__(self, json):
        super().__init__(json)
        self.userId = json["userId"]


class RolesAudit(Audit):

    def __init__(self, json):
        super().__init__(json)
        self.roleId = json["roleId"]


class SecretsAudit(Audit):

    def __init__(self, json):
        super().__init__(json)
        self.secretId = json["secretId"]
