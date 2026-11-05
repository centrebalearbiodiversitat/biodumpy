import requests
from urllib.parse import quote

from biodumpy import Input, BiodumpyException


class BOLD(Input):
	"""
	Query the Barcode of Life Data System (BOLD) database to retrieve taxon genetic or occurrence data.

	Parameters
	----------
	query : list
	    The list of taxa to query.
	summary : bool, optional
	    If True, the function returns a summary of the downloaded metadata instead of the full records.
	    Default is False.

	Details
	-------
	When `summary` is True, the resulting JSON will include the following information:
	- `record_id`: The unique identifier for the BOLD record.
	- `processid`: The process ID associated with the BOLD record.
	- `bin_uri`: The BIN (Barcode Index Number) URI.
	- `taxon`: The name of the lower taxon extracted from the taxonomy information.
	- `country`: The country where the collection event took place.
	- `province_state`: The province or state of the collection event.
	- `region`: The region of the collection event.
	- `lat`: The latitude of the collection event.
	- `lon`: The longitude of the collection event.
	- `markercode`: The marker code from the sequence data.
	- `genbank_accession`: The GenBank accession number from the sequence data.

	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import BOLD
	# Taxa list
	>>> taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']
	# Set the module and start the download
	>>> bdp = Biodumpy([BOLD(bulk=True, summary=False)])
	>>> bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')
	"""

	def __init__(self, summary: bool = False, **kwargs):
		super().__init__(**kwargs)
		self.summary = summary

		if self.output_format not in {"json", "fasta"}:
			raise ValueError('Invalid output_format. Expected "json" or "fasta".')
		
		if self.summary and self.output_format == "fasta":
					raise BiodumpyException("Invalid parameter combination: output_format='fasta' cannot be used when summary=True.")
		
	def _download(self, query, **kwargs) -> list:

		# First query to match the string with BOLD	
		response_json = self._querytax(query)["successful_terms"][0]["matched"]

		# Count
		count_json = self._querycount(response_json)["records"]

		# Generate the query to download the records
		query_download = self._querygenerator(response_json)["query_id"]

		# Download the data
		response = requests.get(f"https://portal.boldsystems.org/api/documents/{query_download}?length={count_json}&start=0")

		if response.status_code != 200:
			raise BiodumpyException(f"Download BOLD. Error {response.status_code}")

		if response.content:
			res = response.json()["data"]
			payload = res

			# Fasta file
			if self.output_format == "fasta":
				fasta_entries = []

				for entry in res:
					if entry.get("nuc"):
						header = (
							f">{entry.get('processid')}|"
							f"{entry.get('identification')}|"
							f"{entry.get('marker_code')}"
						)

						fasta_entries.append(header)
						fasta_entries.append(entry["nuc"])

				payload = fasta_entries

			# Summary
			if self.summary:
				summary_entries = []

				for entry in res:
					summary_entries.append({
						"processid": entry.get("processid", None),
						"sampleid": entry.get("sampleid", None),
						"insdc_acs": entry.get("insdc_acs", None),
						"bin_uri": entry.get("bin_uri", None),
						"collection_date_start": entry.get("collection_date_start", None),
						"coord": entry.get("coord", None),
						"country_ocean": entry.get("country/ocean", None),
						"identified_by": entry.get("identified_by", None),
						"inst": entry.get("inst", None),
						"marker_code": entry.get("marker_code", None),
						"sequence_run_site": entry.get("sequence_run_site", None),
						"sequence_upload_date": entry.get("sequence_upload_date", None),
						"species": entry.get("species", None),
						"identification": entry.get("identification", None),
						"specimens": entry.get("specimens", None)
					})
				
				payload = summary_entries

		return payload

		

	def _querytax(self, query):

		encoded = quote(query, safe="")

		response = requests.get(f"https://portal.boldsystems.org/api/query/preprocessor?query=tax:{encoded}")
		
		if response.status_code != 200:
						raise BiodumpyException(f"Query tax. Error {response.status_code}")

		response_json = response.json()

		return response_json
	
	def _querycount(self, query):

		encoded = quote(query, safe="")
		response = requests.get(f"https://portal.boldsystems.org/api/counts?query={encoded}")

		if response.status_code != 200:
						raise BiodumpyException(f"Query count. Error {response.status_code}")

		response_json = response.json()

		return response_json
	
	def _querygenerator(self, query):

		encoded = quote(query, safe="")
		response = requests.get(f"https://portal.boldsystems.org/api/query?query={encoded}&extent=full")

		if response.status_code != 200:
						raise BiodumpyException(f"Query generator. Error {response.status_code}")

		response_json = response.json()

		return response_json
