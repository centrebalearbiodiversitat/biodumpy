from biodumpy import Input
import requests


class BOLD(Input):
	def download(self, query, **kwargs) -> list:
		response = requests.get(f"http://v4.boldsystems.org/index.php/API_Public/combined?taxon={query}&format=json")
		# response_taxonomy = requests.get(f'https://v4.boldsystems.org/index.php/API_Tax/TaxonSearch?taxName={taxon}')

		if response.status_code != 200:
			return ["Error"]

		if response.content:
			# Parse the response content as a text
			payload = response.json()
			return payload["bold_records"]["records"] if "bold_records" in payload and "records" in payload["bold_records"] else []

		else:
			return []
