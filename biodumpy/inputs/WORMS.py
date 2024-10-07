import requests

from biodumpy import Input, BiodumpyException


class WORMS(Input):
	"""
	Query the World Register of Marine Species (WoRMS) database to retrieve nomenclature and distribution information
	of a list of taxa.

	Parameters
	----------
	query : list
	    The list of taxa to query.
	marine_only: bool = False,
		If True, the function search only for marine taxa.
		Default is False.
	distribution: bool = False,
		If True, the function returns also the WORMS distribution for the taxon.
	    Default is False.
	bulk : bool, optional
		If True, the function creates a bulk file.
		For further information, see the documentation of the Biodumpy package.
		Default is False.
	output_format : string, optional
		The format of the output file.
		The options available are: 'json', 'fasta', 'pdf'.
		Default is 'json'.

	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import WORMS
	# List of taxa
	>>> taxa = ['Pinna nobilis', 'Delphinus delphis', 'Plerogyra sinuosa']
	# Start the download
	>>> bdp = Biodumpy([WORMS(bulk=True, marine_only=True)])
	>>> bdp.start(taxa, output_path='./biodumpy/downloads/{date}/{module}/{name}')
	"""

	def __init__(self,
	             marine_only: bool = False,
	             distribution: bool = False,
	             output_format: str = "json",
	             bulk: bool = False):

		super().__init__(output_format, bulk)
		self.marine_only = marine_only
		self.distribution = distribution

		if output_format != "json":
			raise ValueError("Invalid output_format. Expected 'json'.")

	def _download(self, query, **kwargs) -> list:

		payload = []

		# Download taxon aphia
		aphia = self._download_aphia(taxon=query, marine_only=self.marine_only)

		if not aphia:
			raise BiodumpyException(f"{query} - Aphia not found.")

		# Retrieve nomenclature
		response = requests.get(f"https://www.marinespecies.org/rest/AphiaRecordByAphiaID/{aphia}")

		if response.status_code != 200:
			raise BiodumpyException(f"Occurrences request. Error {response.status_code}")

		if self.distribution:
			taxonomy = response.json()
			dist = self._download_distribution(aphia=aphia)

			taxonomy["distribution"] = dist

			payload.append(taxonomy)

		else:
			payload.append(response.json())

		return payload

	def _download_aphia(self, taxon: list, marine_only: bool = False) -> list:

		response = requests.get(f"https://www.marinespecies.org/rest/AphiaIDByName/{taxon}?marine_only={str(marine_only).lower()}")

		if response.status_code != 200:
			raise BiodumpyException(f"Occurrences request. Error {response.status_code}")

		payload_aphia = response.json()

		return payload_aphia

	def _download_distribution(self, aphia: int) -> list:

		response = requests.get(f"https://www.marinespecies.org/rest/AphiaDistributionsByAphiaID/{aphia}")

		if response.status_code != 200:
			raise BiodumpyException(f"Occurrences request. Error {response.status_code}")

		payload_distribution = response.json()

		return payload_distribution
