from biodumpy import Input
import requests


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
	historical : bool, optional
	    If True, the function returns also the historical threats of a taxon. Default is False.
	threats : bool, optional
	    If True, the function returns also the threat list of a taxon. Default is False.
	regions : list, optional
	    The list of specific IUCN regions. For further information, see the IUCN API documentation. Default is an empty list.
	bulk : bool, optional
		If True, the function creates a bulk file. For further information, see the documentation of the Biodumpy package. Default is False.
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
		historical: bool = False,
		threats: bool = False,
		regions: list = None,
		output_format: str = "json",
		bulk: bool = False
	):
		super().__init__(output_format, bulk)
		if regions is None:
			regions = ["global"]
		self.api_key = api_key
		self.habitat = habitat
		self.regions = regions
		self.historical = historical
		self.threats = threats

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
			taxon_info = self._icun_request(f"https://apiv3.iucnredlist.org/api/v3/species/{query}/region/{region}?token={self.api_key}")
			payload.append(taxon_info)
			taxon_id = taxon_info["taxonid"]

			if taxon_info:
				if self.habitat:
					habitat_info = self._icun_request(
						f"https://apiv3.iucnredlist.org/api/v3/habitats/species/id/{taxon_id}/region/{region}?token={self.api_key}"
					)
					taxon_info.update({"habitat": habitat_info})

				if self.historical:
					habitat_info = self._icun_request(
						f"https://apiv3.iucnredlist.org/api/v3/species/history/id/{taxon_id}/region/{region}?token={self.api_key}"
					)
					taxon_info.update({"historical": habitat_info})

				if self.threats:
					habitat_info = self._icun_request(
						f"https://apiv3.iucnredlist.org/api/v3/threats/species/id/{taxon_id}/region/{region}?token={self.api_key}"
					)
					taxon_info.update({"threats": habitat_info})

		return payload

	def _icun_request(self, query_path):
		"""
		Query the IUCN Red List API for information about a specific species in a given region.

		Parameters:
			query_path: str The path to the IUCN Red List API properly formatted.

		Returns:
			dict: A dictionary containing information about the species in the specified region if found.

		Example:
			result = taxon_iucn(f"https://apiv3.iucnredlist.org/api/v3/habitats/species/id/{taxon_id}/region/{region}?token={self.api_key}")
		"""
		response = requests.get(query_path)

		if response.status_code != 200:
			print(f"Error ---- {query_path}: {response.status_code}")

		if response.content:
			response = response.json()

			if not (len(response.get("result", [])) == 0 or (response.get("value") == "0")):
				result = response.get("result", [])[0]
				if "region_identifier" in response:
					result.update({"region": response["region_identifier"]})

				return result
