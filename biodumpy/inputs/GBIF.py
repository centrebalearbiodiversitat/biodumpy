import requests

from biodumpy import Input, BiodumpyException


class GBIF(Input):
	"""
	Query the GBIF database to retrieve taxonomic and occurrence data.

	Parameters
	----------
	query : list
	    The list of taxa to query.
	dataset_key : str
	    GBIF dataset key. The default is set to the GBIF Backbone Taxonomy dataset key.
	limit : int
	    The maximum number of names to retrieve from the taxonomy backbone for a taxon.
	    Default is 20.
	accepted_only : bool, optional
	    If True, the function returns only the accepted name. See the Details section for more information.
	    Default is True.
	occ : bool, optional
	    If True, the function also returns the occurrences of a taxon. See the Details section for more information.
	    Default is False.
	geometry : str, optional
	    A spatial polygon to filter occurrences within a specified area.
	    Default is an empty string.
	bulk : bool, optional
	    If True, the function creates a bulk file. For further information, see the documentation of the Biodumpy package.
	    Default is False.
	output_format : str, optional
	    The format of the output file. The options available are: 'json', 'fasta', 'pdf'.
	    Default is 'json'.

	Details
	-------
	If accepted_only and occ are both set to True, the function returns the occurrences of the taxon, including all synonyms. If accepted_only is set to False and occ is set to True, the function also downloads occurrences for lower taxonomic levels.
	Refer to the acceptedTaxonKey and taxonKey parameters of the GBIF API endpoint at https://api.gbif.org/v1/occurrence/search for further details.


	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import GBIF
	# GBIF dataset key
	>>> gbif_backbone = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'
	# Taxa list
	>>> taxa = ['Alytes muletensis', 'Bufotes viridis']
	# Set the module and start the download
	>>> bdp = Biodumpy([GBIF(dataset_key=gbif_backbone, limit=20, accepted_only=True, occ=False, bulk=False, output_format='json')])
	>>> bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')
	"""

	def __init__(
		self,
		dataset_key: str = "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c",
		limit: int = 20,
		accepted_only: bool = True,
		occ: bool = False,
		geometry: str = None,
		output_format: str = "json",
		bulk: bool = False,
	):
		super().__init__(output_format, bulk)
		self.dataset_key = dataset_key
		self.limit = limit  # Limit to find name in taxonomy backbone
		self.accepted = accepted_only
		self.occ = occ
		self.geometry = geometry

		if output_format != "json":
			raise ValueError('Invalid output_format. Expected "json".')

	def _download(self, query, **kwargs) -> list:
		payload = []

		# Search taxonomy
		response = requests.get(
			f"https://api.gbif.org/v1/species?",
				params={
					"datasetKey": self.dataset_key,
					"name": query,
					"limit": self.limit,
					"offset": 0
				}
		)

		if response.status_code != 200:
			raise BiodumpyException(f"Taxonomy request. Error {response.status_code}")

		if response.content:
			payload = response.json()["results"]
			if len(payload) > 1:
				# raise BiodumpyException(f"Multiple equal matches for {query}")
				keys = [entry["key"] for entry in payload]

				# Display the list of taxon ID options
				options = [{"index": i, "taxon_id": keys} for i, keys in enumerate(keys)]
				print(f"\nOptions for {query}:\n")
				for option in options:
					print(f"Taxon ID: {option['taxon_id']} - Index: {option['index']}.")
				print(f"{len(keys) + 1}. Skip")

				# Get user selection
				choice = input("Please enter the index corresponding to the correct taxon GBIF ID or choose 'Skip': ")

				# Process selection
				try:
					choice = int(choice)
					if 0 <= choice < len(keys):
						payload = [payload[choice]]
					else:
						print("Skipped selection.")
				except ValueError:
					print("Invalid input, please enter a number.")


			if self.accepted:
				if payload[0].get("taxonomicStatus") != "ACCEPTED":
					acceptedKey = payload[0].get("acceptedKey")
					response_accepted = requests.get(f"https://api.gbif.org/v1/species/{acceptedKey}")
					payload = response_accepted.json()
				else:
					acceptedKey = payload[0].get("key")

				if self.occ and len(payload) > 0:
					# A taxon key from the GBIF backbone. Only synonym taxa are included in the search, so a search for Aves with acceptedTaxonKey=212 (i.e. /occurrence/search?taxonKey=212) will match occurrences identified as birds, but not any known family, genus or species of bird.Parameter may be repeated.
					payload = self._download_gbif_occ(accepted_taxon_key=acceptedKey, geometry=self.geometry)

			else:
				payload = payload[0]

				if self.occ and len(payload) > 0:
					# A taxon key from the GBIF backbone. All included (child) and synonym taxa are included in the search, so a search for Aves with taxonKey=212 (i.e. /occurrence/search?taxonKey=212) will match all birds, no matter which species.Parameter may be repeated.
					payload = self._download_gbif_occ(taxon_key=payload["key"], geometry=self.geometry)

		return payload

	def _download_gbif_occ(self, taxon_key: int = None, accepted_taxon_key: int = None, geometry: str = None):
		response_occ = requests.get(
			f"https://api.gbif.org/v1/occurrence/search",
			params={
				"taxonKey": taxon_key,
				"acceptedTaxonKey": accepted_taxon_key,
				"occurrenceStatus": "PRESENT",
				"geometry": geometry,
				"limit": 300
			}
		)

		if response_occ.status_code != 200:
			raise BiodumpyException(f"Occurrence request. Error {response_occ.status_code}")

		# if response_occ.status_code == 0:
		# 	raise BiodumpyException(f"Occurrence not found.")

		if response_occ.content:
			payload_occ = response_occ.json()
			if payload_occ["endOfRecords"] and payload_occ["count"] > 0:
				return payload_occ["results"]
			elif not payload_occ["endOfRecords"]:
				total_records = payload_occ["count"]

				# Initialize variables
				payload_occ = []
				offset = 0

				# Loop to download data
				while offset < total_records:
					response_occ = requests.get(
						f"https://api.gbif.org/v1/occurrence/search",
						params={
							"taxonKey": taxon_key,
							"acceptedTaxonKey": accepted_taxon_key,
							"occurrenceStatus": "PRESENT",
							"geometry": geometry,
							"limit": 300,
							"offset": offset
						}
					)

					data = response_occ.json()
					occurrences = data["results"]
					payload_occ.extend(occurrences)
					offset = offset + 300

				return payload_occ
			else:
				return []
