import sys
import time
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

	def __init__(self, inputs: list[Input], loading_bar: bool = True, debug: bool = False) -> None:
		super().__init__()
		self.inputs = inputs
		self.debug = debug
		self.loading_bar = loading_bar
		# self.loading_bar = not debug and loading_bar

	# elements must be a flat list of strings
	def start(self, elements, output_path="downloads/{date}/{module}/{name}"):
		if not isinstance(elements, list):
			raise ValueError("Invalid query. Expected a list of taxa to query.")

		current_date = datetime.now().strftime("%Y-%m-%d")

		log_handler = MemoryHandler(capacity=1024)

		logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", handlers=[log_handler])

		bulk_input = {}
		last_tick = {}
		try:
			for el in tqdm(elements, desc="Biodumpy list", unit=" elements", disable=not self.loading_bar, smoothing=0, file=sys.stdout, colour="#FECC45"):
				if isinstance(el, str):
					el = {"query": el}

				if "query" not in el:
					logging.error(f"Missing 'query' key for {el}")
					raise ValueError(f"Missing 'name' key for {el}")

				name = el["query"]
				clean_name = name.replace("/", "_")
				tqdm.write(f"Downloading {name}...")

				for inp in self.inputs:
					module_name = type(inp).__name__
					logging.info(f"biodumpy initialized with {module_name} inputs. Taxon: {name}")

					try:
						if module_name in last_tick:
							delta_last_call = time.time() - last_tick[module_name]
							if delta_last_call < inp.sleep:
								if self.debug:
									tqdm.write(f"[{module_name}] Blocking for {inp.sleep - delta_last_call} seconds...")
								time.sleep(inp.sleep - delta_last_call)
						tqdm.write(f"[{module_name}] Downloading...")
						payload = inp._download(**el)
						last_tick[module_name] = time.time()
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
