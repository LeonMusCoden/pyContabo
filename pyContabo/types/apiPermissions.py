from typing import List


class apiPermission:
    def __init__(self, apiName: str, action: List[str], ressources: List[int] = None):
        self.apiName = apiName
        self.actions = action

        if ressources:
            self.resources = ressources
