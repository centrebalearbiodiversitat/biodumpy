import json
from pathlib import Path
import requests

from biodumpy import Input, BiodumpyException


class AVONET(Input):
	"""
	AVONET plugin to access bird trait data from the AVONET dataset.
	It allows querying species traits by species name.

	Parameters
	----------
	output_format : str
		Output format for the plugin data. Must be "json".

	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import AVONET
	# Taxa list
	>>> taxa = ['Accipiter albogularis', 'Accipiter fasciatus', 'Accipiter tachiro']
	# Set the module and start the download
	>>> bdp = Biodumpy([AVONET(bulk=True, output_format="json")])
	>>> bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')
	"""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		if self.output_format not in {"json"}:
			raise ValueError('Invalid output_format. Expected "json".')

		# Verify if into the folder plugin exist the AVONET json file
		self.base_dir = Path.cwd()
		json_file = self.base_dir / "biodumpy" / "data" / "plugin" / "AVONET1_BirdLife_plugin.json"

		# Ensure the plugin directory exists
		# self.json_file.parent.mkdir(parents=True, exist_ok=True)

		if json_file.exists():
			print("AVONET1_BirdLife_plugin... OK")
		else:
			print('Downloading AVONET1_BirdLife...')
			response = requests.get('https://github.com/TommasoCanc/prueba_biodumpy/releases/download/AVONET/AVONET1_BirdLife_plugin.json')
			if response.status_code == 200:
				data = response.json()
				with open(f"{self.base_dir}/biodumpy/data/plugin/AVONET1_BirdLife_plugin.json", "w", encoding="utf-8") as f:
					json.dump(data, f, indent=4)
			else:
				print(f"Failed to download file: {response.status_code}")


	def _download(self, query, **kwargs) -> list:

		payload = []

		# Open file with trait information
		with open(f"{self.base_dir}/biodumpy/data/plugin/AVONET1_BirdLife_plugin.json", 'r') as file:
			avonet = json.load(file)

			result = avonet.get(query, None)
			if result is None:
				raise ValueError()

			payload.append(result)

		return payload
