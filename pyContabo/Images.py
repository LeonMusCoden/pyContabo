import json

from .Image import Image
from .ImagesAudits import ImagesAudits
from .types.ImagesStats import ImagesStats


class Images:

    def __init__(self, _http):

        self._http = _http
        self.Audits = ImagesAudits(_http)

    def get(self, id: str = None, page: int = None, pageSize: int = None, orderByFields: str = None,
            orderBy: str = None, name: str = None, standardImage: boolean = None):
        """gets any image by id or other parameters through the paging system"""

        if id:
            resp = self._http.request(type="get",
                               url=f"https://api.contabo.com/v1/images/{id}")

            if resp.status_code == 404:
                return []

            return Image(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/images?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderByFields}:{orderBy}&' if orderByFields is not None else ''}{f'name={name}&' if name is not None else ''}{f'standardImage={standardImage}&' if standardImage is not None else ''}"
            url = url[:-1] # Remove the "?" at the end of the url
            resp = self._http.request(type="get",
                               url=url)

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            images = []
            for i in resp.json()["data"]:
                images.append(Image(i, self._http))
            return images

    def create(self, name: str, url: str, osType: str, version: str, description: str=None):
        """uploads image using name, url, OS type, OS version and description"""

        data = json.dumps({
            "name": name,
            "description": description,
            "url": url,
            "osType": osType,
            "version": version
        })

        resp = self._http.request(type="post",
                           url=f"https://api.contabo.com/v1/images",
                           data=data)

        if resp.status_code == 201:
            return True
        return False

    def statistics(self):
        resp = self._http.request(type="get",
                                  url=f"https://api.contabo.com/v1/images/stats")

        if resp.status_code == 200:
            return ImagesStats(resp.json()["data"])
        else:
            return False

