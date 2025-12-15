import sys
import time
from datetime import datetime
from logging.handlers import MemoryHandler

from .input import Input
from .utils import dump, create_directory
from tqdm import tqdm
import logging

import json
import os


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
	cit_style: str
	Citation style used when generating references for the downloaded data.
	Admitted values include "apa" and "bib".
	Default is "apa".
	"""

	SHOW_REMINDER_CITE = True

	def __init__(self, inputs: list[Input], loading_bar: bool = True, debug: bool = False, cit_style: str = "apa") -> None:
		super().__init__()

		if Biodumpy.SHOW_REMINDER_CITE:
			print(
				"\n 🐔 Please remember to cite biodumpy in your work."
				"\n Consult the citation file to ensure proper attribution of all modules used. "
				"\n Citation: Cancellario, T., Golomb Durán, T., Far, A. J., Roldán, A., & Capa, M. (2025). biodumpy: A Comprehensive Biological Data Downloader. bioRxiv, 2025-07. \n\n"
			)
			Biodumpy.SHOW_REMINDER_CITE = False

		for input in inputs:
			if not isinstance(input, Input):
				raise BiodumpyException(f"Input module/s must be of type Input and got type {type(input)}")

		self.inputs = inputs
		self.debug = debug
		self.loading_bar = loading_bar
		self.cit_style = cit_style

		if self.cit_style not in ("apa", "bib"):
			raise ValueError("Please provide a valid cit_style, the parameter options are 'apa' or 'bib'")

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
				# Check whether the variable el is a string.
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

			citation_path = []
			for folder in output_path.split("/"):
				citation_path.append(folder)
				if "{name}" in folder:
					break

			citation_path = "/".join(citation_path)
			self._generate_citation(citation_path.format(date=current_date, module="", name="citation"))

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

	def _generate_citation(self, output_path):
		# Open file with bibliography information
		base_dir = os.path.dirname(__file__)  # directory of current script
		with open(f"{base_dir}/data/citations.json", "r") as file:
			cit_data = json.load(file)

			citations = [{"module": "biodumpy", "citation": cit_data.get("biodumpy").get(self.cit_style)}]

			for inp in self.inputs:
				module_name = type(inp).__name__
				citations.append({"module": module_name, "citation": cit_data.get(module_name).get(self.cit_style)})

			citation_text = []
			for item in citations:
				citation_text.append(f"---- {item.get('module')} ----\n{item.get('citation')}")

			dump(output_path, "\n\n".join(citation_text), output_format="txt")
