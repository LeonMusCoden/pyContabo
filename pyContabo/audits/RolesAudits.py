from .Audit import RolesAudit
from typing import List


class RolesAudits:
    def __init__(self, _http):
        self._http = _http

    def get(
        self,
        page: int = None,
        pageSize: int = None,
        orderBy: str = None,
        roleId: int = None,
        requestId: str = None,
        changedBy: str = None,
    ) -> List[RolesAudit]:

        url = f"https://api.contabo.com/v1/tags/audits?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'roleId={roleId}&' if roleId is not None else ''}{f'requestId={requestId}&' if requestId is not None else ''}{f'changedBy={changedBy}&' if changedBy is not None else ''}"
        url = url[:-1]
        resp = self._http.request(type="get", url=url)

        if resp.status_code == 200:
            data = resp.json()["data"]
            if len(data) == 0:
                return []

            audits = []
            for i in resp.json()["data"]:
                audits.append(RolesAudit(i))
            return audits
        else:
            return []
