from biodumpy import Input
import requests

# query = 'Opiliones'

class COL(Input):

	TAXA_URL = 'https://api.checklistbank.org/dataset/9923/nameusage/search?'
	ACCEPTED_TERMS = ['accepted', 'provisionally accepted']

	def __init__(self, check_syn: bool = False, output_format='json', bulk=False):
		super().__init__(output_format, bulk)
		self.check_syn = check_syn

	def _download(self, query, **kwargs) -> list:

		# Parameters for the request
		params = {'q': query,
		          'content': 'SCIENTIFIC_NAME',
		          'type': 'EXACT',
		          'offset': 0,
		          'limit': 10}

		response = requests.get(COL.TAXA_URL, params=params)

		if response.status_code != 200:
			return ['Error']

		payload = response.json()

		if payload['empty']:
			payload = [{'origin_taxon': query,
			            'taxon_id': None,
			            'status': None,
			            'usage': None,
			            'classification': None}]

		else:
			payload = response.json()['result']

			# Retrieve ID
			if len(payload) > 1:
				ids = [item['id'] for item in payload if 'id' in item]
				ids = ', '.join(ids)
				id_input = input(f'Please enter the correct taxon ID of {query} \n ID: {ids}; Skip \n'
				                 f'Insert the ID:')

			else:
				id_input = payload[0]['id']

			if self.check_syn:
				if payload[0]['usage']['status'] not in COL.ACCEPTED_TERMS:
					id_input = payload[0]['usage']['accepted']['id']

			# Retrieve higher taxonomy
			hight_classification = requests.get(f'https://api.checklistbank.org/dataset/9923/taxon/{id_input}/classification').json()
			# hight_classification = hight_classification_response.json()
			hight_classification = hight_classification[::-1]

			# Retrieve lower taxonomy with the same format of the higher one
			low_classification = requests.get(f'https://api.checklistbank.org/dataset/9923/taxon/{id_input}').json()
			# low_classification = low_classification_response.json()
			low_classification = {
				'id': low_classification.get('id'),
				'name': low_classification.get('name', {}).get('scientificName'),
				'authorship': low_classification.get('name', {}).get('authorship'),
				'rank': low_classification.get('name', {}).get('rank'),
				'label': low_classification.get('label'),
				'labelHtml': low_classification.get('labelHtml')
			}

			hight_classification.append(low_classification)

			payload = [{'origin_taxon': query,
			            'taxon_id': id_input,
			            'status': payload[0]['usage']['status'],
			            'usage': payload[0]['usage'],
			            'classification': hight_classification}]

		return payload
