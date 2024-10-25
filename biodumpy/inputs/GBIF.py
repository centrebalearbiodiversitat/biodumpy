import requests

from biodumpy import Input, BiodumpyException


class GBIF(Input):
	"""
	Query the GBIF database to retrieve taxon data.

	Parameters
	----------
	query : list
	    The list of taxa to query.
	dataset_key : str
	    GBIF dataset key. The default is set to the GBIF Backbone Taxonomy dataset key.
	limit : int
	    The maximum number of names to retrieve from the taxonomy backbone for a taxon. Default is 20.
	accepted_only : bool, optional
	    If True, the function returns only the accepted name. Default is True.
	occ : bool, optional
	    If True, the function also returns the occurrences of a taxon. Default is False.
	geometry : str, optional
	    A spatial polygon to filter occurrences within a specified area. Default is an empty string.
	bulk : bool, optional
	    If True, the function creates a bulk file. For further information, see the documentation of the Biodumpy package. Default is False.
	output_format : str, optional
	    The format of the output file. The options available are: 'json', 'fasta', 'pdf'. Default is 'json'.

	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import GBIF
	# GBIF dataset key
	>>> gbif_backbone = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'
	# Taxa list
	>>> taxa = ['Alytes muletensis (Sanchíz & Adrover, 1979)', 'Bufotes viridis (Laurenti, 1768)']
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

		# if occ and not accepted_only:
		# 	raise ValueError("Invalid accepted_only. Expected True.")

	def _download(self, query, **kwargs) -> list:
		payload = []

		# Search taxonomy
		# response = requests.get(f"https://api.gbif.org/v1/species/search?datasetKey={self.dataset_key}&q={query}&limit={self.limit}")

		response = requests.get(f"https://api.gbif.org/v1/species?",
		                        params={"datasetKey": self.dataset_key,
		                                "name": query,
		                                "limit": self.limit,
		                                "offset": 0}
		                        )

		if response.status_code != 200:
			raise BiodumpyException(f"Taxonomy request. Error {response.status_code}")

		if response.content:

			payload = response.json()["results"]

			if self.accepted:
				# We keep the record only if the query corresponds to the scientific name in the data downloaded.
				# payload = list(filter(lambda x: x.get("taxonomicStatus") == "ACCEPTED" and str(query[0]) in x.get("scientificName", ""), payload))

				if payload[0].get("taxonomicStatus") != "ACCEPTED":
					acceptedKey = payload[0].get("acceptedKey")
					response_accepted = requests.get(f"https://api.gbif.org/v1/species/{acceptedKey}")
					payload = response_accepted.json()

				if self.occ and len(payload) > 0:
					payload = self._download_gbif_occ(accepted_taxon_key=acceptedKey, geometry=self.geometry)

			else:
				payload = payload[0]

				if self.occ and len(payload) > 0:
					payload = self._download_gbif_occ(taxon_key=payload["key"], geometry=self.geometry)

		return payload

	def _download_gbif_occ(self, taxon_key: int = None, accepted_taxon_key: int = None, geometry: str = None):
		response_occ = requests.get(
			f"https://api.gbif.org/v1/occurrence/search",
			params={"taxonKey": taxon_key,
			        "acceptedTaxonKey": accepted_taxon_key,
			        "occurrenceStatus": "PRESENT",
			        "geometry": geometry,
			        "limit": 300}
		)

		if response_occ.status_code != 200:
			raise BiodumpyException(f"Occurrence request. Error {response_occ.status_code}")

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
						params={"taxonKey": taxon_key,
						        "acceptedTaxonKey": accepted_taxon_key,
						        "occurrenceStatus": "PRESENT",
						        "geometry": geometry,
						        "limit": 300,
						        "offset": offset}
					)

					data = response_occ.json()
					occurrences = data["results"]
					payload_occ.extend(occurrences)
					offset = offset + 300

				return payload_occ
			else:
				return []
