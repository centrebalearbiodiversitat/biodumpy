from biodumpy import Input
import requests


class SCOPUS(Input):
	def __init__(self, api_key, download_type="doi", output_format="json", bulk=False):
		super().__init__(output_format, bulk)
		self.api_key = api_key
		self.download_type = download_type

		if output_format != "json":
			raise ValueError("output_format must be json.")

	def _download(self, query, **kwargs) -> list:
		response = requests.get(f"https://api.elsevier.com/content/abstract/doi/{query}?&httpaccept=application/json&apiKey={self.api_key}")

		if response.status_code != 200:
			payload = {"doi": query, "info": None}
		else:
			if response.content:
				payload = response.json()
				payload = {"doi": query, "info": payload["abstracts-retrieval-response"]}

		return payload


# with open('/Users/tcanc/PycharmProjects/biodumpy/Odonata_Poloni.json', 'r') as f:
# 	data = json.load(f)
#
# api_key = '831a5b31345ffea74945d64198e20581'
#
# # API request
# parsed_data = []
# for i in range(len(data)):
# 	doi = next(iter(data[i].keys()))
# 	response = requests.get(
# 		f'https://api.elsevier.com/content/abstract/doi/{doi}?&httpaccept=application/json&apiKey={api_key}')
#
# 	if response.status_code != 200:
# 		parsed_data.append({'doi': doi,
# 		                    'info': None})
# 	else:
# 		if response.content:
# 			payload = response.json()
# 			parsed_data.append({'doi': doi,
# 			                    'info': payload['abstracts-retrieval-response']})
#
#
# 	print(f'{i} of {len(data)}')
#
# # Save json
# with open('/Users/tcanc/PycharmProjects/biodumpy/Odonata_Poloni_scopus.json', 'w+') as output_file:
# 		json.dump(parsed_data, output_file, indent=4)
#
#
# # Open Json
# with open('/Users/tcanc/PycharmProjects/biodumpy/Odonata_Poloni_scopus.json', 'r') as f:
# 	data = json.load(f)
#
#
# abstract = []
# for i in range(len(data)):
# 	info = data[i].get('info', None)
#
# 	if info is not None:
# 		coredata = info['coredata']
# 		abs = coredata['dc:description'] if 'dc:description' in coredata else None
# 		title = coredata['dc:title'] if 'dc:title' in coredata else None
# 	else:
# 		abs = None
# 		title = None
#
# 	abstract.append({'doi': data[i].get('doi'),
# 	                 'title': title,
# 	                 'abstract': abs})
#
# 	print(f'{i} of {len(data)}')
#
# # Save json
# with open('/Users/tcanc/PycharmProjects/biodumpy/Odonata_Poloni_abstract.json', 'w+') as output_file:
# 	json.dump(abstract, output_file, indent=4)
#
# ################
# import requests
#
# # Replace with your Scopus API key
#
# # Replace with the title you want to search for
# title = 'Survival and dispersal routes of head-started loggerhead sea turtle (Caretta caretta) post-hatchlings in the Mediterranean Sea'
#
# # Define the URL and headers for the API request
# url = 'https://api.elsevier.com/content/search/scopus'
# headers = {
#     'Accept': 'application/json',
#     'X-ELS-APIKey': api_key
# }
# # Define the parameters for the search query
# params = {
#     'query': f'TITLE("{title}")'
# }
#
# # Send the GET request to the Scopus API
# response = requests.get(url, headers=headers, params=params)
#
# # Check if the request was successful
# if response.status_code == 200:
#     data = response.json()
#     # Print the JSON response for debugging purposes
#     print(data)
# else:
#     # Print the error if the request was not successful
#     print(f'Error: {response.status_code}')
#     print(response.text)
