from biodumpy import Input
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class ZOOBANK(Input):
	"""
	Query the Official Registry of Zoological Nomenclature (ZooBank) database to retrieve scientific bibliographic
	information.

	Parameters
	----------
	query : list
	    The list of taxa to query.
	dataset_size : str, optional
	    This parameter is useful for managing the download of bibliographic information based on the number of
	    scientific articles stored in ZooBank for each taxon. You can set this parameter to either 'small' or 'large'.
	    We recommend choosing 'small' if the number of articles for a given taxon is fewer than 200, and 'large' if
	    it exceeds 200. Default is 'small'.
	info : bool, optional
	    If set to True, the function will download additional article information not included in the main research,
	    such as the DOI. Default is False.
	bulk : bool, optional
	    If True, the function creates a bulk file. For further information, see the documentation of the Biodumpy
	    package. Default is False.
	output_format : str, optional
	    The format of the output file. The available option is 'json'. Default is 'json'.

	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import ZOOBANK
	# Taxa list
	>>> taxa = ['Alytes muletensis', 'Bufotes viridis', 'Hyla meridionalis', 'Anax imperator']
	# Set the module and start the download
	>>> bdp = Biodumpy([ZOOBANK(bulk=True, dataset_size='small', info=False)])
	>>> bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')
	"""

	def __init__(self, dataset_size: str = "small", output_format: str = "json", info: bool = False, bulk: bool = False):
		super().__init__(output_format, bulk)
		self.dataset_size = dataset_size
		self.info = info

		if self.dataset_size not in ["small", "large"]:
			raise ValueError("Invalid dataset_size. Expected 'small' or 'large'.")

		if output_format != "json":
			raise ValueError("Invalid output_format. Expected 'json'.")

	def _download(self, query, **kwargs) -> list:
		payload = []

		if self.dataset_size == "small":
			response = requests.get(f"https://zoobank.org/References.json?search_term={query}")

			if response.status_code != 200:
				return [f"Error: {response.status_code}"]

			payload = response.json()

		if self.dataset_size == "large":
			print("Searching in ZOOBANK...")
			response_pub = requests.get(f"https://zoobank.org/Search?search_term={query}")

			if response_pub.status_code != 200:
				return [f"Error: {response_pub.status_code}"]

			html_content = response_pub.text

			# Parsing the HTML content with BeautifulSoup
			soup = BeautifulSoup(html_content, "html.parser")
			referenceuuid = [
				entry["href"].replace("/References/", "") for entry in soup.find_all(class_="biblio-entry") if "href" in entry.attrs
			]

			for ref in tqdm(referenceuuid, desc="Fetching paper info"):
				response_pub = requests.get(f"https://zoobank.org/References.json/{ref}")

				if response_pub.status_code == 200:  # Check if the request was successful
					try:
						json_content = response_pub.json()[0]
						payload.append(json_content)
					except Exception as e:
						print(f"An error occurred: {e} .... referenceuuid: {ref}")
				else:
					print(f"Failed to retrieve data for {ref}")

		if self.info:
			referenceuuid = [item["referenceuuid"] for item in payload]

			referenceuuid_data = []
			if referenceuuid != [""]:
				for refuid in referenceuuid:
					response_id = requests.get(f"http://zoobank.org/Identifiers.json/{refuid}")

					if response_id.status_code != 200:
						return [f"Error: {response_id.status_code}"]

					referenceuuid_data.append(response_id.json())

			else:
				print("No referenceuuid found.")

			return referenceuuid_data

		else:
			return payload
