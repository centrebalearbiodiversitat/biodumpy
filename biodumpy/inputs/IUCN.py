from biodumpy import Input
import requests

class IUCN(Input):

	def __init__(self, api_key: str, habitat: bool = False, historical: bool = False, threats: bool = False,
	             region: list = None, output_format: str = 'json', bulk: bool = False):
		super().__init__(output_format, bulk)
		if region is None:
			region = ['global']
		self.api_key = api_key
		self.habitat = habitat
		self.region = region
		self.historical = historical
		self.threats = threats

		iucn_regions = ['northern_africa', 'global', 'pan-africa', 'central_africa', 'eastern_africa', 'northeastern_africa',
		                'western_africa', 'southern_africa', 'mediterranean', 'europe']

		if output_format != 'json':
			raise ValueError('output_format must be json.')

		for region in self.region:
			if region not in iucn_regions:
				raise ValueError(f'Choose an IUCN region from the following options: {iucn_regions}.')

	def download(self, query, **kwargs) -> list:

		payload = []

		for regions in self.region:

			taxon_info = self.taxon_iucn(query, regions)
			payload.append(taxon_info)

			if self.habitat and taxon_info is not None:
				habitat_info = self.habitat_iucn(taxon_info['taxonid'], regions)
				taxon_info.update({'habitat': habitat_info})

			if self.historical and taxon_info is not None:
				habitat_info = self.historical_iucn(taxon_info['taxonid'], regions)
				taxon_info.update({'historical': habitat_info})

			if self.threats and taxon_info is not None:
				habitat_info = self.threats_iucn(taxon_info['taxonid'], regions)
				taxon_info.update({'threats': habitat_info})

		return payload

	def taxon_iucn(self, query: str, region: str) -> dict:

		"""
	       Query the IUCN Red List API for information about a specific species in a given region.

	       Parameters:
	       query (str): The name of the species to query.
	       region (str): The name of a specific region.

	       Returns:
	       dict: A dictionary containing information about the species in the specified region if found.


	       Example:
	       result = taxon_iucn('Alytes muletensis', 'europe')
		"""

		response = requests.get(
			f'https://apiv3.iucnredlist.org/api/v3/species/{query}/region/{region}?token={self.api_key}')

		if response.status_code != 200:
			print(f'Error ---- {query}: {response.status_code}')

		if response.content:
			response_json = response.json()

			if not (len(response_json.get('result', [])) == 0 or (response_json.get('value') == '0')):
				result = response_json.get('result', [])[0]
				result.update({'region': response_json['region_identifier']})

				return result

	def habitat_iucn(self, taxonid: int, region: str) -> dict:

		"""
        Query the IUCN Red List API for habitat information about a specific species in a given region.

        Parameters:
        query (str): The taxon id of the species to query.
        region (str): The name of a specific region.

        Returns:
	    dict: A dictionary containing information about the habitat of the species in the specified region if found.


	    Example:
	    result = habitat_iucn(977, 'europe')
		"""

		response = requests.get(
			f'https://apiv3.iucnredlist.org/api/v3/habitats/species/id/{taxonid}/region/{region}?token={self.api_key}')

		if response.status_code != 200:
			print(f'Error ---- {taxonid}: {response.status_code}')

		if response.content:
			response_json = response.json()

			if not (len(response_json.get('result', [])) == 0 or (response_json.get('value') == '0')):
				result = response_json.get('result', [])

				return result

	def historical_iucn(self, taxonid: int, region: str) -> dict:

		"""
        Query the IUCN Red List API for historical assessment information about a specific species in a given region.

        Parameters:
        query (str): The taxon id of the species to query.
        region (str): The name of a specific region.

        Returns:
	    dict: A dictionary containing information about the historical assessment of the species in the specified region if found.


	    Example:
	    result = historical_iucn(977, 'europe')
		"""

		response = requests.get(
			f'https://apiv3.iucnredlist.org/api/v3/species/history/id/{taxonid}/region/{region}?token={self.api_key}')

		if response.status_code != 200:
			print(f'Error ---- {taxonid}: {response.status_code}')

		if response.content:
			response_json = response.json()

			if not (len(response_json.get('result', [])) == 0 or (response_json.get('value') == '0')):
				result = response_json.get('result', [])

				return result

	def threats_iucn(self, taxonid: int, region: str) -> dict:

		"""
		Query the IUCN Red List API for threat information about a specific species in a given region.

		Parameters:
		query (str): The taxon id of the species to query.
		region (str): The name of a specific region.

		Returns:
		dict: A dictionary containing information about threats of the species in the specified region if found.


		Example:
		result = threats_iucn(977, 'europe')
		"""

		response = requests.get(
			f'https://apiv3.iucnredlist.org/api/v3/threats/species/id/{taxonid}/region/{region}?token={self.api_key}')

		if response.status_code != 200:
			print(f'Error ---- {taxonid}: {response.status_code}')

		if response.content:
			response_json = response.json()

			if not (len(response_json.get('result', [])) == 0 or (response_json.get('value') == '0')):
				result = response_json.get('result', [])

				return result




