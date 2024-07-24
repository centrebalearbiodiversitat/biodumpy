from biodumpy import Input
import requests

# It is the datasetKeyof the GBIF taxonomy backbone
# datasetKey=d7dddbf4-2cf0-4f39-9b2a-bb099caae36c


query = 'Alytes muletensis'


class GBIF(Input):

	def __init__(self, dataset_key='d7dddbf4-2cf0-4f39-9b2a-bb099caae36c', limit=20, output_format='json', bulk=False):
		super().__init__(output_format, bulk)
		self.dataset_key = dataset_key
		self.limit = limit

		if output_format != 'json':
			raise ValueError('output_format must be json.')

	def download(self, query, **kwargs) -> list:

		response = requests.get(
			f'https://api.gbif.org/v1/species/search?datasetKey={self.dataset_key}&q={query}&limit={self.limit}')

		if response.status_code != 200:
			return ['Error']

		if response.content:
			payload = response.json()
			return payload['results'] if payload['count'] > 0 else []

	def download_gbif_occ(self, taxon_key: int):

		response_occ = requests.get(
			f'https://api.gbif.org/v1/occurrence/search',
			params={
				'acceptedTaxonKey': taxon_key,
				'occurrenceStatus': 'PRESENT',
				'limit': 300
			}
		)

		if response_occ.status_code != 200:
			return ['Error']

		if response_occ.content:
			payload_occ = response_occ.json()

			if payload_occ['endOfRecords'] and payload_occ['count'] > 0:
				return payload_occ['results']

			elif payload_occ['endOfRecords'] is not True:
				total_records = payload_occ['count']

				# Initialize variables
				payload_occ = []
				offset = 0

				# Loop to download data
				while offset < total_records:
					response_occ = requests.get(
						f'https://api.gbif.org/v1/occurrence/search',
						params={
							'acceptedTaxonKey': taxon_key,
							'occurrenceStatus': 'PRESENT',
							'limit': 300,
							'offset': offset
						}
					)

					data = response_occ.json()
					occurrences = data['results']
					payload_occ.extend(occurrences)
					offset = offset + 300
			else:
				return []


