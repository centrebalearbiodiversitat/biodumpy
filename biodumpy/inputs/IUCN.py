from biodumpy import Input
import requests

class IUCN(Input):

	def __init__(self, api_key, output_format='json', bulk=False):
		super().__init__(output_format, bulk)
		self.api_key = api_key

		if output_format != 'json':
			raise ValueError('output_format must be json.')

	def download(self, query, **kwargs) -> list:

		response = requests.get(f'https://apiv3.iucnredlist.org/api/v3/species/{query}?token={self.api_key}')

		if response.status_code != 200:
			return ['Error']

		if response.content:
			# Parse the response content as a text
			payload = response.json()
			return payload['result'] if 'result' in payload else []

		else:
			return []
