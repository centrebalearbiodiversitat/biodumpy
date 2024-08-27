from biodumpy import Input
import requests


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
		If True, the function creates a bulk file. For further information, see the documentation of the Biodumpy package.
		Default is False.
	output_format : string, optional
		The format of the output file. The options available are: 'json', 'fasta', 'pdf'. Default is 'json'.

	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import GBIF
	# GBIF dataset key
	>>> gbif_backbone = 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c'
	# Taxa list
	>>> taxa = ['Alytes muletensis (Sanchíz & Adrover, 1979)', 'Bufotes viridis (Laurenti, 1768)', 'Hyla meridionalis Boettger, 1874', 'Anax imperator Leach, 1815']
	# Set the module and start the download
	>>> bdp = Biodumpy([GBIF(dataset_key=gbif_backbone, limit=20, bulk=False, accepted=True, occ=False)])
	>>> bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')
	"""

	def __init__(
		self,
		dataset_key="d7dddbf4-2cf0-4f39-9b2a-bb099caae36c",
		limit=20,
		accepted_only=True,
		occ=False,
		geometry=None,
		output_format="json",
		bulk=False,
	):
		super().__init__(output_format, bulk)
		self.dataset_key = dataset_key
		self.limit = limit  # Limit to find name in taxonomy backbone
		self.accepted = accepted_only
		self.occ = occ
		self.geometry = geometry

		if output_format != "json":
			raise ValueError("output_format must be json.")

		if occ is True and accepted_only is False:
			raise ValueError("accepted must be True.")

	def _download(self, query, **kwargs) -> list:
		payload = []
		response = requests.get(f"https://api.gbif.org/v1/species/search?datasetKey={self.dataset_key}&q={query}&limit={self.limit}")

		if response.status_code != 200:
			return ["Error"]

		if response.content:
			if self.accepted:
				payload = response.json()
				data = payload["results"]

				# We keep the record only if the query corresponds to the scientific name in the data downloaded.
				payload = list(
					filter(lambda x: x.get("taxonomicStatus") == "ACCEPTED" and str(query[0]) in x.get("scientificName", ""), data)
				)

			else:
				payload = response.json()["results"]

			if self.occ:
				if len(payload) > 0:
					payload = self._download_gbif_occ(taxon_key=payload[0]["nubKey"], geometry=self.geometry)

		return payload

	def _download_gbif_occ(self, taxon_key: int, geometry):
		response_occ = requests.get(
			f"https://api.gbif.org/v1/occurrence/search",
			params={"acceptedTaxonKey": taxon_key, "occurrenceStatus": "PRESENT", "geometry": geometry, "limit": 300},
		)

		if response_occ.status_code != 200:
			return ["Error"]

		if response_occ.content:
			payload_occ = response_occ.json()

			if payload_occ["endOfRecords"] and payload_occ["count"] > 0:
				return payload_occ["results"]

			elif payload_occ["endOfRecords"] is not True:
				total_records = payload_occ["count"]

				# Initialize variables
				payload_occ = []
				offset = 0

				# Loop to download data
				while offset < total_records:
					response_occ = requests.get(
						f"https://api.gbif.org/v1/occurrence/search",
						params={
							"acceptedTaxonKey": taxon_key,
							"occurrenceStatus": "PRESENT",
							"geometry": geometry,
							"limit": 300,
							"offset": offset,
						},
					)

					data = response_occ.json()
					occurrences = data["results"]
					payload_occ.extend(occurrences)
					offset = offset + 300

				return payload_occ
			else:
				return []
