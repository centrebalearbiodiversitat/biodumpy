import requests

from biodumpy.utils import remove_tags
from biodumpy import Input, BiodumpyException


class Crossref(Input):
    """
    Query the Crossref database to retrieve scientific bibliographic metadata information.

    Parameters
    ----------
    query : list
        The list of DOIs to query.
    summary : bool, optional
        If True, the function returns a summary of the downloaded metadata instead of the full records.
        Default is False.

    Details
    -------
    When `summary` is True, the resulting JSON will include the following information:
    - `publisher`: The name of the publishing entity responsible for releasing the publication.
    - `container-title`: The title of the journal or book in which the research is published.
    - `DOI`: The Digital Object Identifier assigned to the publication.
    - `type`: The type of the publication, such as article, book chapter, report, etc.
    - `language`: The language in which the publication is written.
    - `URL`: A direct link to the publication.
    - `published`: The date when the research was published.
    - `title`: The title of the publication.
    - `author`: The names of the authors who contributed to the research along with their main academic information.
    - `abstract`: The publication abstract (if available).

    Example
    -------
    >>> from biodumpy import Biodumpy
    >>> from biodumpy.inputs import Crossref
    # Create a list of DOIs
    >>> dois = ["10.1038/s44185-022-00001-3", "10.1111/gcb.17059", "10.1016/j.ecoinf.2024.102629"]
    # Set the Biodumpy functions with the specific parameters
    >>> bdp = Biodumpy([Crossref(bulk=True)])
    >>> bdp.start(dois, output_path='./downloads/{date}/{module}/{name}')
    """

    def __init__(self,
                 summary: bool = False,
                 **kwargs
                 ):

        super().__init__(**kwargs)
        self.summary = summary

        if self.output_format != "json":
            raise ValueError("Invalid output_format. Expected 'json'.")

    def _download(self, query, **kwargs) -> list:
        payload = []

        response = requests.get(f"https://api.crossref.org/works/{query}")

        if response.status_code != 200:
            raise BiodumpyException(f"Reference request. Error {response.status_code}")

        if response.content:
            message = response.json().get("message", {})
            if self.summary:
                abstract = message.get("abstract", None)
                payload.append(
                    {
                        "publisher": message.get("publisher"),
                        "container-title": message.get("container-title")[0],
                        "DOI": message.get("DOI"),
                        "type": message.get("type"),
                        "language": message.get("language"),
                        "URL": message.get("URL"),
                        "published": message.get("published")["date-parts"],
                        "title": message.get("title")[0],
                        "author": message.get("author"),
                        "abstract": remove_tags(abstract) if abstract else None,
                    }
                )
            else:
                payload = [message]

        return payload
