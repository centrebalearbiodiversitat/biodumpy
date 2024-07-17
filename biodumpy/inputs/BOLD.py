from biodumpy import Input

import requests


class BOLD(Input):
	def download(self, name, **kwargs) -> list:
		response = requests.get(f'http://v4.boldsystems.org/index.php/API_Public/combined?taxon={name}&format=json')
		# response_taxonomy = requests.get(f'https://v4.boldsystems.org/index.php/API_Tax/TaxonSearch?taxName={taxon}')

		if response.status_code != 200:
		# if response.status_code != 200 or response_taxonomy.status_code != 200:
			return ['Error']

		# Parse the response content as a text
		# data_taxonomy = response_taxonomy.json()
		payload = response.json()

		return payload['bold_records']['records'] if 'bold_records' in payload and 'records' in payload['bold_records'] else []
