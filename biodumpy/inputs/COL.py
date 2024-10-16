import requests

from biodumpy import Input, BiodumpyException


class COL(Input):
	"""
	Query the Catalogue of Life (COL) database to retrieve nomenclature information of a list of taxa.

	Parameters
	----------
	query : list
	    The list of taxa to query.
	check_syn : bool, optional
	    If True, the function returns only the accepted nomenclature of a taxon.
	    See Detail section for further information.
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
	When check_syn is set to True, the resulting JSON will include only the nomenclature of the accepted taxon.
	For instance, if check_syn is True, the output for the species Bufo roseus will only show the nomenclature for
	Bufotes viridis. Conversely, if check_syn is set to False, the JSON will include the nomenclature for both
	Bufo roseus and Bufotes viridis.

	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import COL
	# List of taxa
	>>> taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator', 'Bufo roseus', 'Stollia betae']
	# Start the download
	>>> bdp = Biodumpy([COL(bulk=True, check_syn=False)])
	>>> bdp.start(taxa, output_path='./biodumpy/downloads/{date}/{module}/{name}')
	"""

	ACCEPTED_TERMS = ["accepted", "provisionally accepted"]

	def __init__(self, output_format: str = "json", bulk: bool = False, check_syn: bool = False):
		super().__init__(output_format, bulk)
		self.check_syn = check_syn

		if output_format != "json":
			raise ValueError("Invalid output_format. Expected 'json'.")

	def _download(self, query, **kwargs) -> list:
		response = requests.get(
			f"https://api.checklistbank.org/dataset/9923/nameusage/search?q={query}&content=SCIENTIFIC_NAME&type=EXACT&offset=0&limit=10"
		)

		if response.status_code != 200:
			raise BiodumpyException(f"Taxonomy request. Error {response.status_code}")

		payload = response.json()

		if payload["empty"]:
			payload = [{"origin_taxon": query, "taxon_id": None, "status": None, "usage": None, "classification": None}]
		else:
			result = response.json()["result"]

			# Multiple IDs
			if len(result) > 1:
				ids = [item.get("id") for item in result if "id" in item]
				ids = ", ".join(ids)
				id_input = input(f"Please enter the correct taxon ID of {query} \n ID: {ids}; Skip \n" f"Insert the ID:")

				if id_input == "Skip":
					result = [{"id": None, "usage": None, "status": None, "classification": None}]
				else:
					result = [item for item in result if item["id"] == id_input]

			id = result[0].get("id")
			usage = result[0].get("usage")
			status = usage.get("status") if usage else None

			classification = result[0].get("classification")
			if self.check_syn and status not in COL.ACCEPTED_TERMS:
				synonym_id = usage.get("id") if usage else None
				classification = [item for item in classification if item["id"] != synonym_id] if classification else None

			payload = [{"origin_taxon": query, "taxon_id": id, "status": status, "usage": usage, "classification": classification}]

		return payload
