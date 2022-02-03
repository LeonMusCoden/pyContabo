class ImagesStats:
    def __init__(self, json):
        self.tenantId = json["tenantId"]
        self.customerId = json["customerId"]
        self.currentImagesCount = json["currentImagesCount"]
        self.totalSizeMb = json["totalSizeMb"]
        self.usedSizeMb = json["usedSizeMb"]
        self.freeSizeMb = json["freeSizeMb"]
