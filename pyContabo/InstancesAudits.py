from .errors import NotFound
from .types.Audit import InstancesAudit
from .util import makeRequest, statusCheck


class InstancesAudits:

    def __init__(self):
        pass

    def get(self, page=None, pageSize=None, orderByField=None, orderBy=None, instanceId=None, requestId=None,
            changedBy=None):
        """gets audits history through the paging system"""

        url = f"https://api.contabo.com/v1/compute/instances/audits?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderByField}:{orderBy}&' if orderByField is not None else ''}{f'instanceId={instanceId}&' if instanceId is not None else ''}{f'requestId={requestId}&' if requestId is not None else ''}{f'instanceId={instanceId}&' if instanceId is not None else ''}{f'changedBy={changedBy}&' if changedBy is not None else ''}"
        url = url[:-1]
        resp = makeRequest(type="get",
                           url=url)

        statusCheck(resp.status_code)
        if resp.status_code != 200:
            data = resp.json()["data"]
            if len(data) == 0:
                raise NotFound("InstancesAudits")

            audits = []
            for i in resp.json()["data"]:
                audits.append(InstancesAudit(i))
            return audits
        else:
            return False
