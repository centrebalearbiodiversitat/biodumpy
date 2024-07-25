from biodumpy import Input
import requests


class COL(Input):
	TAXA_URL = "https://api.checklistbank.org/dataset/9923/nameusage/search"

	def download(self, query, **kwargs) -> list:
		# name = 'Anax imperator'
		# Parameters for the request
		params = {"q": query, "offset": 0, "limit": 10}

		# Make the GET request with parameters
		response = requests.get(COL.TAXA_URL, params=params)

		if response.status_code != 200:
			return ["Error"]

		data = response.json()["result"]

		return [data[0]["classification"]]
