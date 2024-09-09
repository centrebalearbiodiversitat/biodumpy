from biodumpy import Input
import requests

# Try if I can use summary=True and fasta=True


class BOLD(Input):
	"""
	Query the Barcode of Life Data System (BOLD) database to retrieve taxon genetic or occurrence data.

	Parameters
	----------
	query : list
	    The list of taxa to query.
	summary : bool, optional
	    If True, the function returns only a summary of a metadata informatio.
	    See Detail section for further information.
	    Default is False.
	fasta : bool, optional
		If True, the function downloads the FASTA file.
		Default is False.
	bulk : bool, optional
		If True, the function creates a bulk file.
		For further information, see the documentation of the Biodumpy package.
		Default is False.
	output_format : string, optional
		The format of the output file.
		The options available are: 'json', 'fasta', 'pdf'.
		Default is 'json'.

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

	def __init__(self, summary=False, fasta=False, output_format="json", bulk=False):
		super().__init__(output_format, bulk)
		self.summary = summary
		self.fasta = fasta

		if self.fasta and output_format != "fasta":
			raise ValueError("Invalid output_format. Expected fasta.")

		if output_format not in {"json", "fasta"}:
			raise ValueError('Invalid output_format. Expected "json" or "fasta".')

	def _download(self, query, **kwargs) -> list:
		if self.fasta:
			response = requests.get(f"http://v4.boldsystems.org/index.php/API_Public/sequence?taxon={query}")
			response = response.content

			# Decode bytes to string
			data_str = response.decode()

			# Split the data by '>'
			fasta_entries = [f">{entry}" for entry in data_str.split(">") if entry]

			return fasta_entries

		else:
			response = requests.get(f"http://v4.boldsystems.org/index.php/API_Public/combined?taxon={query}&format=json")

			payload = []

			if response.status_code != 200:
				return [f"Error: {response.status_code}"]

			if response.content:
				results = response.json()

				if self.summary:
					results_summary = results.get("bold_records", {}).get("records", [])

					for entry in results_summary:
						entry_summary = results_summary[entry]

						# Extract the necessary fields with default None values if keys are missing.
						# Sequence could contain more than one marker code.

						sequences = entry_summary.get("sequences", {}).get("sequence", [])
						markercodes = [seq.get("markercode") for seq in sequences if "markercode" in seq]
						genbank_accession = [seq.get("genbank_accession") for seq in sequences if "genbank_accession" in seq]

						# Retrieve taxonomy
						taxonomy = entry_summary.get("taxonomy", {})
						taxon_name = taxonomy.get(list(taxonomy.keys())[-1], {}).get("taxon", {}).get("name")

						# Retrieve collection event metadata
						collection_event = entry_summary.get("collection_event", {})
						coordinates = collection_event.get("coordinates", {})

						payload.append(
							{
								"record_id": entry_summary.get("record_id"),
								"processid": entry_summary.get("processid"),
								"bin_uri": entry_summary.get("bin_uri"),
								"taxon": taxon_name,
								"country": collection_event.get("country"),
								"province_state": collection_event.get("province_state"),
								"region": collection_event.get("region"),
								"lat": coordinates.get("lat") if coordinates else None,
								"lon": coordinates.get("lon") if coordinates else None,
								"markercode": "/".join(markercodes) if markercodes else None,
								"genbank_accession": genbank_accession[0] if genbank_accession else None,
							}
						)
				else:
					payload.append(
						results["bold_records"]["records"] if "bold_records" in results and "records" in results["bold_records"] else []
					)

				return payload
			else:
				return payload
