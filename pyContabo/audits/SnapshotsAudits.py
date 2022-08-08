from .Audit import SnapshotsAudit
from typing import List


class SnapshotsAudits:
    def __init__(self, _http):
        self._http = _http

    def get(
        self,
        page: int = None,
        pageSize: int = None,
        orderBy: str = None,
        instanceId: int = None,
        snapshotId: str = None,
        requestId: str = None,
        changedBy: str = None,
        startDate: str = None,
        endDate: str = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> List[SnapshotsAudit]:
        """fetches audits

        Examples:
            >>> Snapshots.Audits.get()
            [SnapshotsAudit]

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            page: Number of page to be fetched.
            pageSize: Number of elements per page.
            orderBy: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`
            snapshotId: The identifier of the snapshot.
            requestId: The requestId of the API call which led to the change.
            changedBy: UserId of the user which led to the change.
            startDate: Start of search time range.
            endDate: End of search time range.

        Returns:
            List of SnapshotsAudit
        """

        url = f"https://api.contabo.com/v1/compute/snapshots/audits?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'instanceId={instanceId}&' if instanceId is not None else ''}{f'snapshotId={snapshotId}&' if snapshotId is not None else ''}{f'requestId={requestId}&' if requestId is not None else ''}{f'instanceId={instanceId}&' if instanceId is not None else ''}{f'changedBy={changedBy}&' if changedBy is not None else ''}{f'startDate={startDate}&' if startDate is not None else ''}{f'endDate={endDate}&' if endDate is not None else ''}"
        url = url[:-1]
        resp = self._http.request(
            type="get", url=url, x_request_id=x_request_id, x_trace_id=x_trace_id
        )

        if resp.status_code == 200:
            data = resp.json()["data"]
            if len(data) == 0:
                return []

            audits = []
            for i in resp.json()["data"]:
                audits.append(SnapshotsAudit(i))
            return audits
        else:
            return []
