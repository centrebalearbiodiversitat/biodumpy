import requests
from urllib.parse import quote
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from biodumpy import Input, BiodumpyException


class BOLD(Input):
	"""
	Query the Barcode of Life Data System (BOLD Portal) database to retrieve taxon genetic or occurrence data.

	Parameters
	----------
	summary : bool, optional
		If True, the function returns a summary of the downloaded metadata instead of the full records.
		Default is False.
	output_format : str, optional
		Output format for the downloaded data ("json" or "fasta"). Default is "json".
	bulk : bool, optional
		Whether to merge results into a single file. Default is False.
	sleep : int, optional
		Delay between requests in seconds. Default is 3.

	Details
	-------
	When `summary` is True, the resulting JSON will include key metadata fields:
	- `record_id`: The unique identifier for the BOLD record.
	- `processid`: The process ID associated with the BOLD record.
	- `sampleid`: The sample identifier.
	- `bin_uri`: The BIN (Barcode Index Number) URI.
	- `taxon`: The taxonomic name (species or identification).
	- `species`: The species name.
	- `identification`: The identification string.
	- `country_ocean`: The country or ocean of collection.
	- `province_state`: The province or state of collection.
	- `region`: The geographic region of collection.
	- `coord`: Geographic coordinates (latitude, longitude).
	- `marker_code`: The marker code (e.g. COI-5P).
	- `insdc_acs`: The GenBank / INSDC accession number.
	- `identified_by`: The identifier person or institution.
	- `inst`: Housing institution.
	- `collection_date_start`: Collection date.
	- `sequence_run_site`: Sequencing facility.
	- `sequence_upload_date`: Date uploaded to BOLD.
	- `specimens`: Specimen information.

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

	HEADERS = {
		"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"),
		"Accept": "application/json, text/plain, */*",
	}

	def __init__(self, summary: bool = False, headers: dict = None, **kwargs):
		super().__init__(**kwargs)
		self.summary = summary
		self.headers = headers if headers is not None else self.HEADERS.copy()

		if self.output_format not in {"json", "fasta"}:
			raise ValueError('Invalid output_format. Expected "json" or "fasta".')

		if self.summary and self.output_format == "fasta":
			raise BiodumpyException("Invalid parameter combination: output_format='fasta' cannot be used when summary=True.")

	def _get_session(self):
		session = requests.Session()
		session.headers.update(self.headers)
		retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
		adapter = HTTPAdapter(max_retries=retries)
		session.mount("https://", adapter)
		session.mount("http://", adapter)
		return session

	def _download(self, query, **kwargs) -> list:
		payload = []
		session = self._get_session()

		# 1. Match the taxon query string with BOLD
		tax_response = self._querytax(query, session=session)
		successful_terms = tax_response.get("successful_terms", [])
		if not successful_terms:
			return payload

		matched = successful_terms[0].get("matched")
		if not matched:
			return payload

		# 2. Check record count
		count_response = self._querycount(matched, session=session)
		record_count = count_response.get("records", 0)
		if record_count == 0:
			return payload

		# 3. Generate query ID to download the records
		query_gen = self._querygenerator(matched, session=session)
		query_download = query_gen.get("query_id")
		if not query_download:
			return payload

		# 4. Download data from BOLD Portal documents endpoint
		try:
			response = session.get(f"https://portal.boldsystems.org/api/documents/{query_download}?length={record_count}&start=0", timeout=30)
		except requests.RequestException as e:
			raise BiodumpyException(f"Download BOLD request failed: {str(e)}")

		if response.status_code != 200:
			raise BiodumpyException(f"Download BOLD. Error {response.status_code}")

		if response.content:
			data_json = response.json()
			res = data_json.get("data", [])
			payload = res

			# Fasta format
			if self.output_format == "fasta":
				fasta_entries = []
				for entry in res:
					if entry.get("nuc"):
						header = f">{entry.get('processid')}|{entry.get('identification')}|{entry.get('marker_code')}"
						fasta_entries.append(header)
						fasta_entries.append(entry["nuc"])
				payload = fasta_entries

			# Summary format
			elif self.summary:
				summary_entries = []
				for entry in res:
					summary_entries.append(
						{
							"record_id": entry.get("record_id", None),
							"processid": entry.get("processid", None),
							"sampleid": entry.get("sampleid", None),
							"insdc_acs": entry.get("insdc_acs", None),
							"bin_uri": entry.get("bin_uri", None),
							"taxon": entry.get("species") or entry.get("identification", None),
							"species": entry.get("species", None),
							"identification": entry.get("identification", None),
							"collection_date_start": entry.get("collection_date_start", None),
							"coord": entry.get("coord", None),
							"country_ocean": entry.get("country/ocean", None),
							"province_state": entry.get("province/state", None),
							"region": entry.get("region", None),
							"identified_by": entry.get("identified_by", None),
							"inst": entry.get("inst", None),
							"marker_code": entry.get("marker_code", None),
							"sequence_run_site": entry.get("sequence_run_site", None),
							"sequence_upload_date": entry.get("sequence_upload_date", None),
							"specimens": entry.get("specimens", None),
						}
					)
				payload = summary_entries

		return payload

	def _querytax(self, query, session=None):
		session = session or self._get_session()
		encoded = quote(query, safe="")
		try:
			response = session.get(f"https://portal.boldsystems.org/api/query/preprocessor?query=tax:{encoded}", timeout=30)
		except requests.RequestException as e:
			raise BiodumpyException(f"Query tax failed: {str(e)}")

		if response.status_code != 200:
			raise BiodumpyException(f"Query tax. Error {response.status_code}")

		return response.json()

	def _querycount(self, query, session=None):
		session = session or self._get_session()
		encoded = quote(query, safe="")
		try:
			response = session.get(f"https://portal.boldsystems.org/api/counts?query={encoded}", timeout=30)
		except requests.RequestException as e:
			raise BiodumpyException(f"Query count failed: {str(e)}")

		if response.status_code != 200:
			raise BiodumpyException(f"Query count. Error {response.status_code}")

		return response.json()

	def _querygenerator(self, query, session=None):
		session = session or self._get_session()
		encoded = quote(query, safe="")
		try:
			response = session.get(f"https://portal.boldsystems.org/api/query?query={encoded}&extent=full", timeout=30)
		except requests.RequestException as e:
			raise BiodumpyException(f"Query generator failed: {str(e)}")

		if response.status_code != 200:
			raise BiodumpyException(f"Query generator. Error {response.status_code}")

		return response.json()
