from biodumpy import Input
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class ZOOBANK(Input):

	def __init__(self, output_format="json", bulk=False, dataset_size = 'small'):
		super().__init__(output_format, bulk)
		self.dataset_size = dataset_size

		if self.dataset_size not in ['small', 'large']:
			raise ValueError("Invalid dataset size parameter. Expected 'small' or 'large'.")

	def download(self, query, **kwargs) -> list:
		payload = []

		if self.dataset_size == 'large':
			print('Searching in ZOOBANK...')
			response_pub = requests.get(f'https://zoobank.org/Search?search_term={query}')

			if response_pub.status_code != 200:
				return ['Error']

			html_content = response_pub.text

			# Parsing the HTML content with BeautifulSoup
			soup = BeautifulSoup(html_content, 'html.parser')
			referenceuuid = [entry['href'].replace('/References/', '')
			                 for entry in soup.find_all(class_='biblio-entry') if 'href' in entry.attrs]

			# payload = []
			for ref in tqdm(referenceuuid, desc="Fetching paper info"):
				response_pub = requests.get(f'http://zoobank.org/References.json/{ref}')
				if response_pub.status_code == 200:  # Check if the request was successful
					try:
						json_content = response_pub.json()[0]
						payload.append(json_content)
					except Exception as e:
						print(f"An error occurred: {e} .... referenceuuid: {ref}")
				else:
					print(f"Failed to retrieve data for {ref}")

			return payload

		if self.dataset_size == 'small':

			PUB_URL = 'https://zoobank.org/References.json?'

			params_pub = {'search_term': query}
			response_pub = requests.get(PUB_URL, params=params_pub)

			if response_pub.status_code != 200:
				print(response_pub.text)
			else:
				payload = response_pub.json()

			return payload

	@staticmethod
	def zoobank_info(referenceuuid: str):
		data_total = []
		response_id = requests.get(f'http://zoobank.org/Identifiers.json/{referenceuuid}')

		if response_id.status_code != 200:
			print(response_id.text)
		else:
			try:
				data_total.append(response_id.json())

			except requests.exceptions.JSONDecodeError as e:
				print(f'{e} ---- referenceuuid: {referenceuuid}')

		return data_total
