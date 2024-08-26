from biodumpy import Input
import requests
import json

class BOLD(Input):
	def _download(self, query, **kwargs) -> list:
		response = requests.get(f'http://v4.boldsystems.org/index.php/API_Public/combined?taxon={query}&format=json')
		# response_taxonomy = requests.get(f'https://v4.boldsystems.org/index.php/API_Tax/TaxonSearch?taxName={taxon}')

		payload = []

		if response.status_code != 200:
			return ["Error"]

		if response.content:
			# Parse the response content as a text
			results = response.json()
			payload.append(results["bold_records"]["records"] if "bold_records" in results and "records" in results["bold_records"] else [])
			return payload

		else:
			return payload

	@staticmethod
	def bold_summary(json_path: str):
		"""
			Extracts and summarizes specific information from a JSON file containing BOLD records.

			The function reads a JSON file specified by `json_path`, processes each entry to extract relevant
			details such as record IDs, taxonomy, collection events, and sequence information, and compiles
			this data into a structured format.

			Parameters:
			-----------
			json_path : str
				The file path to the JSON file that contains the BOLD data to be processed.

			Returns:
			--------
			List[Dict[str, Dict[str, Any]]]
				A list where each element is a dictionary representing a processed entry from the JSON file.
				Each entry dictionary maps `record_id` to another dictionary containing the following keys:
				- 'record_id': The unique identifier for the BOLD record.
				- 'processid': The process ID associated with the BOLD record.
				- 'bin_uri': The BIN (Barcode Index Number) URI.
				- 'taxon': The name of the lower taxon extracted from the taxonomy information.
				- 'country': The country where the collection event took place.
				- 'province_state': The province or state of the collection event.
				- 'region': The region of the collection event.
				- 'markercode': The marker code from the sequences data.
				- 'genbank_accession': The GenBank accession number from the sequences data.

			Example:
			--------
			Suppose you have a JSON file at 'data/records.json' with the appropriate structure. You can use
			the function as follows:

			```python
			summary = bold_summary('data/records.json')
			for entry in summary:
				for record_id, details in entry.items():
					print(f"Record ID: {details['record_id']}")
					print(f"Taxon: {details['taxon']}")
					print(f"Country: {details['country']}")
					# ... print other details as needed
			```

			This will output the summarized information for each record in the JSON file.

			Notes:
			------
			- This function is designed to work with records downloaded using Biodumpy with the BOLD(bulk=True)
			option. For further details, refer to the documentation for the Biodumpy function and its usage with
			BOLD mode.
			"""

		# Check if the file is a JSON file
		try:
			with open(json_path, 'r') as file:
				data = json.load(file)
		except Exception as e:
			raise Exception(f"An error occurred: {e}")

		result = []
		markercodes = None
		genbank_accession = None
		for entry in data:
			for record_id, record_data in entry.items():
				# Extract necessary fields with default None values if keys are missing
				sequences = record_data.get('sequences', None)

				if sequences:
					sequences = sequences['sequence']
					markercodes = [i['markercode'] for i in sequences] if 'markercode' in sequences[0].keys() else None
					genbank_accession = [i['genbank_accession'] for i in sequences] if 'genbank_accession' in sequences[0].keys() else None

				collection_event = record_data.get('collection_event', None)
				taxonomy = record_data.get('taxonomy', None)

				# Get the last taxon in the taxonomy dictionary
				taxon_name = taxonomy.get(list(taxonomy.keys())[-1], {}).get('taxon', {}).get('name')

				result.append({
					'record_id': record_data.get('record_id', None),
					'processid': record_data.get('processid', None),
					'bin_uri': record_data.get('bin_uri', None),
					'taxon': taxon_name,
					'country': collection_event.get('country', None),
					'province_state': collection_event.get('province_state', None),
					'region': collection_event.get('region', None),
					'markercode': '/'.join(markercodes) if markercodes else None,
					'genbank_accession': genbank_accession[0] if genbank_accession else None
				})

		return result
