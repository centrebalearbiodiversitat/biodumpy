from biodumpy import Input
import requests


class ZOOBANK(Input):
	PUB_URL = 'https://zoobank.org/References.json?'

	def download(self, query, **kwargs) -> list:

		params_pub = {'search_term': query}
		response_pub = requests.get(ZOOBANK.PUB_URL, params=params_pub)

		if response_pub.status_code != 200:
			print(response_pub.text)
		else:
			data = response_pub.json()

		return [data]

	@staticmethod
	def zoobank_info(referenceuuid: str):

		ID_URL = 'http://zoobank.org/Identifiers.json/'
		data_total = []

		referenceuuid = referenceuuid
		params_id = {'search_term': referenceuuid}
		response_id = requests.get(ID_URL, params=params_id)

		if response_id.status_code != 200:
			print(response_id.text)
		else:
			if response_id.status_code != 200:
				print(response_id.text)
			else:
				try:
					data_total.append = response_id.json()

				except requests.exceptions.JSONDecodeError as e:
					print(f'{e} ---- referenceuuid: {referenceuuid}')

		return data_total
