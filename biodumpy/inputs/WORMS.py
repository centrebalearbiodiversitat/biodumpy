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
	marine_only : bool, optional
	    If True, the function searches only for marine taxa.
	    Default is False.
	distribution : bool, optional
	    If True, the function also returns the WORMS distribution for the taxon.
	    Default is False.
	bulk : bool, optional
	    If True, the function creates a bulk file.
	    For further information, see the documentation of the Biodumpy package.
	    Default is False.
	output_format : string, optional
	    The format of the output file. The options available are: 'json', 'fasta', 'pdf'.
	    Default is 'json'.

	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import WORMS
	# List of taxa
	>>> taxa = ['Pinna nobilis', 'Delphinus delphis', 'Plerogyra sinuosa']
	# Start the download
	>>> bdp = Biodumpy([WORMS(bulk=True, marine_only=True)])
	>>> bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')
	"""

	def __init__(self, marine_only: bool = False, distribution: bool = False, output_format: str = "json", bulk: bool = False):
		super().__init__(output_format, bulk)
		self.marine_only = marine_only
		self.distribution = distribution

		if output_format != "json":
			raise ValueError("Invalid output_format. Expected 'json'.")

	def _download(self, query, **kwargs) -> list:
		payload = []

		# Download taxon aphia
		aphia = self._worms_request(f"https://www.marinespecies.org/rest/AphiaIDByName/{query}?marine_only={str(self.marine_only).lower()}")
		if not aphia:
			raise BiodumpyException(f"{query} - Aphia not found.")

		# Retrieve nomenclature
		response = self._worms_request(f"https://www.marinespecies.org/rest/AphiaRecordByAphiaID/{aphia}")

		if self.distribution:
			response["distribution"] = self._worms_request(f"https://www.marinespecies.org/rest/AphiaDistributionsByAphiaID/{aphia}")

		payload.append(response)

		return payload

	def _worms_request(self, url) -> list:
		response = requests.get(url)
		if response.status_code != 200:
			raise BiodumpyException(f"Occurrences request. Error {response.status_code}")

		return response.json()
