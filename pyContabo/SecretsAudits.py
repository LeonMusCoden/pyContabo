from .types.Audit import SecretsAudit


class SecretsAudits:

    def __init__(self, _http):
        self._http = _http

    def get(self, page=None, pageSize=None, orderBy=None, secretId=None,
            requestId=None, changedBy=None):
        """gets audits history through the paging system"""

        url = f"https://api.contabo.com/v1/secrets/audits?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'instanceId={instanceId}&' if instanceId is not None else ''}{f'requestId={requestId}&' if requestId is not None else ''}{f'secretId={secretId}&' if secretId is not None else ''}{f'changedBy={changedBy}&' if changedBy is not None else ''}"
        url = url[:-1]
        resp = self._http.request(type="get",
                           url=url)

        if resp.status_code == 200:
            data = resp.json()["data"]
            if len(data) == 0:
                return []

            audits = []
            for i in resp.json()["data"]:
                audits.append(SecretsAudit(i))
            return audits
        else:
            return False
