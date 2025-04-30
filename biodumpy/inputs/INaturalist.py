import requests
import sys

from biodumpy import Input, BiodumpyException


class INaturalist(Input):
    """
    Query the iNaturalist database to retrieve photo links of a list of taxa.

    Parameters
    ----------
    query : list
        The list of taxa to query.
    info : bool
        If set to True, the function returns metadata about a taxon. The order parameter defaults to desc, and order_by defaults to observations_count, as proposed by the iNaturalist API endpoint (https://api.inaturalist.org/v1/docs/#!/Taxa/get_taxa). If the API returns multiple results, only the first one will be returned.
        Default is False.

    Details
    -------
    To view the photo, append the image_id value to the end of the following link:
    https://inaturalist-open-data.s3.amazonaws.com/photos/

    Photos can be downloaded only if they have one of the valid licenses. If an iNaturalist photo has a different license than those specified, it can't be downloaded.

    A detailed list of the available licenses can be found here:

    - CC0 (Public Domain Dedication): No rights reserved. The creator waives all copyright, allowing anyone to use the work for any purpose without permission.
    - CC BY (Attribution): Others can distribute, remix, adapt, and build upon the work, even commercially, as long as they give the appropriate credit to the creator.
    - CC BY-NC (Attribution-NonCommercial): Others can remix, adapt, and build upon the work non-commercially. While new works must also acknowledge the creator, they don’t have to be licensed on the same terms.
    - CC BY-NC-ND (Attribution-NonCommercial-NoDerivs): Others can download and share the work, but can’t change it or use it commercially, and must give credit to the creator.
    - CC BY-SA (Attribution-ShareAlike): Others can remix, adapt, and build upon the work, even commercially, but must credit the creator and license their new creations under the same terms.
    - CC BY-ND (Attribution-NoDerivs): Others can share the work, but they can't alter it or use it commercially, and they must credit the creator.
    - CC BY-NC-SA (Attribution-NonCommercial-ShareAlike): Others can remix, adapt, and build upon the work non-commercially, as long as they give credit and license their new creations under the same terms.

    Example
    -------
    >>> from biodumpy import Biodumpy
    >>> from biodumpy.inputs import INaturalist
    # List of taxa
    >>> taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']
    # Start the download
    >>> bdp = Biodumpy([INaturalist(bulk=True)])
    >>> bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')
    """

    def __init__(self,
                 info: bool = False,
                 **kwargs
                 ):

        super().__init__(**kwargs)
        self.info = info

        if self.output_format != "json":
            raise ValueError('Invalid output_format. Expected "json".')

    def _download(self, query, **kwargs) -> list:
        # API request
        response = requests.get(f"https://api.inaturalist.org/v1/taxa?q={query}&order=desc&order_by=observations_count")

        if response.status_code != 200:
            raise BiodumpyException(f"Observation request. Error {response.status_code}")

        # Dictionary for empty records
        photo_details_empty = {"taxon": query, "image_id": None, "license_code": None, "attribution": None}
        photo_details = photo_details_empty

        # Photo license values valid for the download
        photo_license = ["cc0", "cc-by", "cc-by-nc", "cc-by-nc-nd", "cc-by-sa", "cc-by-nd", "cc-by-nc-sa"]

        if response.status_code == 200:
            results = response.json()["results"]

            if self.info:
                payload = []

				if len(results) == 1:
					payload.append(results[0])
				else:
					payload.append(results[0])
					print(f"More than one result for the taxon: {query}. \nOnly the first result was used in the output.", file=sys.stderr)

                return payload

            else:
                results_filtered = next(filter(lambda x: x["name"] == query, results), None)
                if results_filtered:
                    taxon_id = results_filtered["id"]

                    if results_filtered["default_photo"] is not None:
                        photo_info = results_filtered["default_photo"] if results_filtered["default_photo"][
                            "license_code"] else None
                    else:
                        photo_info = None

                    # Search the photo into the occurrences
                    if photo_info is None:
                        response_id = requests.get(f"https://api.inaturalist.org/v1/taxa/{taxon_id}")

                        if response_id.status_code == 200:
                            results_id = response_id.json()["results"]
                            photo_id = results_id[0]["taxon_photos"]

							photo_details = next(filter(lambda x: x["photo"]["license_code"] in photo_license, photo_id), None)

							if photo_details:
								url_photo = photo_details["photo"]["url"]
								url_photo = url_photo.split("/")[-2] + "/" + url_photo.split("/")[-1]
								photo_details = {
									"taxon": query,
									"image_id": url_photo.replace("square", "medium"),
									"license_code": photo_details["photo"]["license_code"],
									"attribution": photo_details["photo"]["attribution"],
								}
							else:
								photo_details = photo_details_empty
					else:
						url_photo = photo_info["url"]
						url_photo = url_photo.split("/")[-2] + "/" + url_photo.split("/")[-1]
						photo_details = {
							"taxon": query,
							"image_id": url_photo.replace("square", "medium"),
							"license_code": photo_info["license_code"],
							"attribution": photo_info["attribution"],
						}

				return [photo_details]
