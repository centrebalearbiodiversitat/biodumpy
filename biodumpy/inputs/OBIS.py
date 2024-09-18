from biodumpy import Input
import requests
from tqdm import tqdm
import logging


class OBIS(Input):
	"""
	Query the OBIS database to retrieve taxon data.

	Parameters
	----------
	query : list
	    The list of taxa to query.
	occ : bool, optional
	    If True, the function also returns the occurrences of a taxon. Default is False.
	geometry : str, optional
	    A spatial polygon to filter occurrences within a specified area. Default is an empty string.
	area : int, optional
	    A marine area to filter occurrences. Default is an empty string.
	bulk : bool, optional
		If True, the function creates a bulk file. For further information, see the documentation of the Biodumpy package.
		Default is False.
	output_format : string, optional
		The format of the output file. The options available is: 'json'. Default is 'json'.

	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import OBIS
	# Taxa list
	>>> taxa = ['Pinna nobilis', 'Delphinus delphis', 'Plerogyra sinuosa']
	# Set the module and start the download
	>>> bdp = Biodumpy([OBIS(bulk=False, occ=True)])
	>>> bdp.start(taxa, output_path='./downloads/{date}/{module}_occ/{name}')
	"""

	def __init__(self, occ: bool = False, geometry: str = None, areaid: int = None, output_format: str = "json", bulk: bool = False):
		super().__init__(output_format, bulk)
		self.occ = occ
		self.geometry = geometry
		self.areaid = areaid

		if output_format != "json":
			raise ValueError('Invalid output_format. Expected "json".')

		# if occ is False, areaid and pylogon cannot both be True
		if not self.occ and (self.areaid is not None or self.geometry):
			raise ValueError('"If "occ" is False, "areaid" and "geometry" cannot be set."')

	def _download(self, query, **kwargs) -> list:
		payload = []
		response = requests.get(f"https://api.obis.org/v3/taxon/{query}")

		if response.status_code != 200:
			logging.error("OBIS response code: %s", response.status_code)
		else:
			pass

		# if response.status_code != 200:
		# 	return [f"Error: {response.status_code}"]

		if response.content:
			payload = response.json()["results"]

			if self.occ and len(payload) > 0:
				tax_key = payload[0]["taxonID"]
				payload = self._download_obis_occ(taxon_key=tax_key, geometry=self.geometry, areaid=self.areaid)

		return payload

	def _download_obis_occ(self, taxon_key: int, geometry: str = None, areaid: int = None):
		total_records = None
		payload_occ = []

		params = {
			"taxonid": taxon_key,
			"size": 10000,  # Max size in OBIS is 10000
			"after": None,
			"geometry": geometry,
			"areaid": areaid,
		}

		try:
			while True:
				response = requests.get("https://api.obis.org/v3/occurrence", params=params)

				if response.status_code != 200:
					raise Exception(f"Error: {response.status_code}")

				response_json = response.json()
				data = response_json["results"]

				if not data:  # If the data list is empty, break the loop
					break

				# Initialize the progress bar on the first request
				if total_records is None:
					total_records = response_json["total"]
					pbar = tqdm(total=total_records, desc="Downloading")

				# Update the progress bar
				pbar.update(len(data))

				# Append the current batch of results to the list
				payload_occ.extend(data)

				# Check if we've retrieved all records
				if len(payload_occ) >= total_records:
					break

				# Update the 'after' parameter with the last id
				params["after"] = data[-1]["id"]

		finally:
			# Ensure the progress bar is closed properly even if an error occurs
			if total_records is not None:
				pbar.close()

		return payload_occ
