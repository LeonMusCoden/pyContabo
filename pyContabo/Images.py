import json
from typing import List, Union

from .Image import Image
from .audits.ImagesAudits import ImagesAudits
from .types.ImagesStats import ImagesStats


class Images:
    def __init__(self, _http):

        self._http = _http
        self.Audits = ImagesAudits(_http)

    def get(
        self,
        id: str = None,
        page: int = None,
        pageSize: int = None,
        orderBy: str = None,
        name: str = None,
        standardImage: bool = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> Union[Image, List[Image]]:
        """fetches any image(s) by id or other parameters

        Examples:
            >>> Images.get()
            [image]
            >>> Images.get(name="Arch", standardImage="true", orderBy="name:asc")
            [image]
            >>> Assignments.get(id=" Example: 9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d")
            image

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            id: The identifier of the image
            name: The name of the image
            standardImage: Flag indicating that image is either a standard (true) or a custom image (false)
            page: Number of page to be fetched.
            pageSize: Number of elements per page.
            orderBy: Specify fields and ordering (ASC for ascending, DESC for descending) in following format `field:ASC|DESC`

        Returns:
            List and filter all available standard images provided by Contabo and your uploaded custom images.
        """

        if id:
            resp = self._http.request(
                type="get",
                url=f"https://api.contabo.com/v1/compute/images/{id}",
                x_request_id=x_request_id,
                x_trace_id=x_trace_id,
            )

            if resp.status_code == 404:
                return []

            return Image(resp.json()["data"][0], self._http)

        else:
            url = f"https://api.contabo.com/v1/compute/images?{f'page={page}&' if page is not None else ''}{f'size={pageSize}&' if pageSize is not None else ''}{f'orderBy={orderBy}&' if orderBy is not None else ''}{f'name={name}&' if name is not None else ''}{f'standardImage={standardImage}&' if standardImage is not None else ''}"
            url = url[:-1]  # Remove the "?" at the end of the url
            resp = self._http.request(
                type="get", url=url, x_request_id=x_request_id, x_trace_id=x_trace_id
            )

            data = resp.json()["data"]
            if len(data) == 0:
                return []

            images = []
            for i in resp.json()["data"]:
                images.append(Image(i, self._http))
            return images

    def create(
        self,
        name: str,
        url: str,
        osType: str,
        version: str,
        description: str = None,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """Provide a custom image.

        Examples:
            >>> Images.create(name="Arch", url="https://api.contabo.com", osType="Linux", version="1.0", description="btw")
            True

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.
            name: Image Name
            description: Image Description
            url: URL from where the image has been downloaded / provided.
            osType: Provided type of operating system (OS). Please specify `Windows` for MS Windows and `Linux` for other OS.

        Returns:
            Bool respresenting if the image has been succesfully created.
        """

        data = json.dumps(
            {
                "name": name,
                "description": description,
                "url": url,
                "osType": osType,
                "version": version,
            }
        )

        resp = self._http.request(
            type="post",
            url=f"https://api.contabo.com/v1/compute/images",
            data=data,
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 201:
            return True
        return False

    def statistics(
        self,
        x_request_id: str = None,
        x_trace_id: str = None,
    ) -> bool:
        """List statistics regarding the customer's custom images such as the number of custom images uploaded, used disk space, free available disk space and total available disk space.

        Examples:
            >>> Images.statistics()
            [ImagesStats]

        Args:
            x_request_id: Uuid4 to identify individual requests for support cases.
            x_trace_id: Identifier to trace group of requests.

        Returns:
            List of ImagesStats
        """

        resp = self._http.request(
            type="get",
            url=f"https://api.contabo.com/v1/compute/images/stats",
            x_request_id=x_request_id,
            x_trace_id=x_trace_id,
        )

        if resp.status_code == 200:
            stats = []
            for i in resp.json()["data"]:
                stats.append(ImagesStats(i))
            return stats
        else:
            return False
