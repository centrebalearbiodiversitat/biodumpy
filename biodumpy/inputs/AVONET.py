import json
import os
from pathlib import Path
import requests

from biodumpy import Input, BiodumpyException


class AVONET(Input):
	"""
	AVONET plugin to access bird trait data from the AVONET dataset.
	It allows querying species traits by species name.

	Parameters
	----------
	data_path : str or Path, optional
		Custom path to an AVONET JSON file. If omitted, the default plugin dataset is used.
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

	DATA_URL = "https://github.com/centrebalearbiodiversitat/biodumpy/releases/download/AVONET/AVONET1_BirdLife_plugin.json"

	_DATA_CACHE = None

	def __init__(self, data_path=None, **kwargs):
		super().__init__(**kwargs)

		if self.output_format not in {"json"}:
			raise ValueError('Invalid output_format. Expected "json".')

		if data_path:
			self.json_file = Path(data_path)
		else:
			package_dir = Path(__file__).resolve().parent.parent / "data" / "plugin"
			try:
				package_dir.mkdir(parents=True, exist_ok=True)
				self.json_file = package_dir / "AVONET1_BirdLife_plugin.json"
			except (PermissionError, OSError):
				cache_dir = Path.home() / ".cache" / "biodumpy" / "data" / "plugin"
				cache_dir.mkdir(parents=True, exist_ok=True)
				self.json_file = cache_dir / "AVONET1_BirdLife_plugin.json"

		# Download dataset if not cached locally
		if not self.json_file.exists():
			self._download_dataset()
		else:
			print("AVONET1_BirdLife_plugin... OK")

		# Load dataset into memory once
		if not data_path and AVONET._DATA_CACHE is not None:
			self.data = AVONET._DATA_CACHE
		else:
			with open(self.json_file, "r", encoding="utf-8") as f:
				self.data = json.load(f)
			if not data_path:
				AVONET._DATA_CACHE = self.data

	def _download_dataset(self):
		print("Downloading AVONET1_BirdLife...")
		try:
			response = requests.get(self.DATA_URL, timeout=30)
			if response.status_code == 200:
				data = response.json()
				with open(self.json_file, "w", encoding="utf-8") as f:
					json.dump(data, f, indent=4)
				return
			else:
				raise BiodumpyException(f"Failed to download AVONET dataset from {self.DATA_URL}: HTTP {response.status_code}")
		except requests.RequestException as e:
			raise BiodumpyException(f"Failed to download AVONET dataset from {self.DATA_URL}: {str(e)}")

	def _download(self, query, **kwargs) -> list:
		payload = []

		result = self.data.get(query, None)
		if result is None:
			raise ValueError(f"Taxon '{query}' not found in AVONET dataset.")

		payload.append(result)

		return payload
