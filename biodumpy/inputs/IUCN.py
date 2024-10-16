import requests

from biodumpy import Input, BiodumpyException


class IUCN(Input):
	"""
    Query the IUCN Red List API for information about a specific species in a given region.

    Parameters
    ----------
    query : list
        The list of taxa to query.
    api_key : str
        Your IUCN API key.
    habitat : str
        The name of an IUCN habitat.
    regions : list, optional
        The list of specific IUCN regions. For further information, see the IUCN API documentation. Default is an empty list.
    historical : bool, optional
        If True, the function returns also the historical threats of a taxon. Default is False.
    threats : bool, optional
        If True, the function returns also the threat list of a taxon. Default is False.
    citation : bool, optional
        If True, the function returns the citation for a given species assessment.
    weblink : bool, optional
        If True, the function returns the link to redirect to the Red List website page for this species.
    bulk : bool, optional
        If True, the function creates a bulk file. For further information, see the documentation of the Biodumpy package.
        Default is False.
    output_format : string, optional
        The format of the output file. The options available are: 'json', 'fasta', 'pdf'. Default is 'json'.

    Example
    -------
    >>> from biodumpy import Biodumpy
    >>> from biodumpy.inputs import IUCN
    # Insert your API key
    >>> api_key = 'YOUR_API_KEY'
    # Taxa list
    >>> taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis']
    # Select your output path
    >>> output_path = 'YOUR_OUTPUT_PATH'
    # Select the regions
    >>> regions = ['global', 'europe']
    >>> bdp = Biodumpy([IUCN(api_key=api_key, bulk=True, regions=regions)])
    >>> bdp.start(taxa, output_path=output_path)
	"""


	def __init__(
			self,
			api_key: str,
			habitat: bool = False,
			regions: list = None,
			historical: bool = False,
			threats: bool = False,
			citation: bool = False,
			weblink: bool = False,
			output_format: str = "json",
			bulk: bool = False,
	):
		super().__init__(output_format, bulk)
		if regions is None:
			regions = ["global"]
		self.api_key = api_key
		self.habitat = habitat
		self.regions = regions
		self.historical = historical
		self.threats = threats
		self.citation = citation
		self.weblink = weblink

		iucn_regions = [
			"northern_africa",
			"global",
			"pan-africa",
			"central_africa",
			"eastern_africa",
			"northeastern_africa",
			"western_africa",
			"southern_africa",
			"mediterranean",
			"europe"
		]

		if output_format != "json":
			raise ValueError("Invalid output_format. Expected 'json'.")

		for regions in self.regions:
			if regions not in iucn_regions:
				raise ValueError(f"Choose an IUCN region from the following options: {iucn_regions}.")

	def _download(self, query, **kwargs) -> list:
		payload = []

		for region in self.regions:
			taxon_info = self._icun_request(
				f"https://apiv3.iucnredlist.org/api/v3/species/{query}/region/{region}?token={self.api_key}")

			if not taxon_info or taxon_info[0].get("taxonid") is None:
				continue

			taxon_info = taxon_info[0]
			payload.append(taxon_info)
			taxon_id = taxon_info["taxonid"]

			if taxon_info:
				if self.habitat:
					habitat_info = self._icun_request(
						f"https://apiv3.iucnredlist.org/api/v3/habitats/species/id/{taxon_id}/region/{region}?token={self.api_key}"
					)
					taxon_info.update({"habitat": habitat_info})

				if self.historical:
					historical_info = self._icun_request(
						f"https://apiv3.iucnredlist.org/api/v3/species/history/id/{taxon_id}/region/{region}?token={self.api_key}"
					)
					taxon_info.update({"historical": historical_info})

				if self.threats:
					threats_info = self._icun_request(
						f"https://apiv3.iucnredlist.org/api/v3/threats/species/id/{taxon_id}/region/{region}?token={self.api_key}"
					)
					taxon_info.update({"threats": threats_info})

				if self.citation:
					citation_info = self._icun_request(
						f"https://apiv3.iucnredlist.org/api/v3/species/citation/id/{taxon_id}/region/{region}?token={self.api_key}"
					)
					taxon_info.update({"citation": citation_info})

				if self.weblink:
					weblink_info = f"https://apiv3.iucnredlist.org/api/v3/taxonredirect/{taxon_id}/{region}"
					taxon_info.update({"weblink": weblink_info})

		return payload

	def _icun_request(self, query_path):
		"""
		Query the IUCN Red List API for information about a specific species in a given region.

		Parameters:
			query_path: str The path to the IUCN Red List API properly formatted.

		Returns:
			dict: A dictionary containing information about the species in the specified region if found.

		Example:
			result = icun_request(f"https://apiv3.iucnredlist.org/api/v3/habitats/species/id/{taxon_id}/region/{region}?token={self.api_key}")
		"""
		response = requests.get(query_path)

		if response.status_code != 200:
			raise BiodumpyException(f"Error {response.status_code}")

		if response.content:
			response = response.json()

			if not (len(response.get("result", [])) == 0 or (response.get("value") == "0")):
				result = response.get("result", [])
				if "region_identifier" in response:
					for r in result:
						r.update({"region": response["region_identifier"]})

				return result
