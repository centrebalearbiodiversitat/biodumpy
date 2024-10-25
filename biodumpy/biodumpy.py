from datetime import datetime
from logging.handlers import MemoryHandler

from .input import Input
from .utils import dump, create_directory
from tqdm import tqdm
import logging


class BiodumpyException(Exception):
	pass


class Biodumpy:
	"""
	This class is designed to download biodiversity data from various sources using multiple input modules.

	Parameters
	----------
	inputs : list
		A list of input modules that handle specific biodiversity data downloads.
	loading_bar : bool
		 If True, shows a progress bar when downloading data. If False, disable the progress bar.
		 Default is False
	debug : bool
		If True, enables printing of detailed information during execution.
		Default is True
	"""

	def __init__(self, inputs: list[Input], loading_bar: bool = False, debug: bool = True) -> None:
		super().__init__()
		self.inputs = inputs
		self.debug = debug
		self.loading_bar = loading_bar

	# elements must be a flat list of strings
	def start(self, elements, output_path="downloads/{date}/{module}/{name}"):
		if not isinstance(elements, list):
			raise ValueError("Invalid query. Expected a list of taxa to query.")

		current_date = datetime.now().strftime("%Y-%m-%d")

		log_handler = MemoryHandler(capacity=1024)

		logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", handlers=[log_handler])

		bulk_input = {}
		try:
			for el in tqdm(elements, desc="Biodumpy list", unit=" elements", disable=not self.loading_bar, smoothing=0):
				if not el:
					continue

				if isinstance(el, str):
					el = {"query": el}

				if "query" not in el:
					logging.error(f"Missing 'query' key for {el}")
					raise ValueError(f"Missing 'name' key for {el}")

				name = el["query"]
				clean_name = name.replace("/", "_")
				if self.debug:
					print(f"Downloading {name}...")

				for inp in self.inputs:
					module_name = type(inp).__name__
					logging.info(f"biodumpy initialized with {module_name} inputs. Taxon: {name}")

					try:
						payload = inp._download(**el)
					except Exception as e:
						logging.error(f'[{module_name}] Failed to download data for "{name}": {str(e)} \n')
						continue

					if inp.bulk:
						if inp not in bulk_input:
							bulk_input[inp] = []
						bulk_input[inp].extend(payload)

					else:
						dump(file_name=f"{output_path.format(date=current_date, module=module_name, name=clean_name)}", obj_list=payload, output_format=inp.output_format)
		finally:
			for inp, payload in bulk_input.items():
				dump(file_name=output_path.format(date=current_date, module=type(inp).__name__, name="bulk"), obj_list=payload, output_format=inp.output_format)

			if log_handler.buffer:
				print("---- Please review the dump file; errors have been detected ----")
				down_path = str()
				for folder in output_path.split("/"):
					if "{" in folder:
						break
					down_path = f"{down_path}{folder}/"

				create_directory(down_path)
				with open(f"{down_path}/dump_{current_date}.log", "w") as f:
					for record in log_handler.buffer:
						log_entry = f"{record.levelname}: {record.getMessage()}\n"
						f.write(log_entry)
