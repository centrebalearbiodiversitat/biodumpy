from datetime import datetime
from .input import Input
from .utils import dump
from tqdm import tqdm


class Biodumpy:
	def __init__(self, inputs: list[Input], loading_bar: bool = False, debug: bool = True) -> None:
		super().__init__()
		self.inputs = inputs
		self.debug = debug
		self.loading_bar = loading_bar

	# elements must be a flat list of strings
	def start(self, elements, output_path="downloads/{date}/{module}/{name}"):
		current_date = datetime.now().strftime("%Y-%m-%d")
		bulk_input = {}
		try:
			for el in tqdm(elements, desc="Biodumpy list", unit=" elements", disable=not self.loading_bar, smoothing=0):
				if not el:
					continue

				if isinstance(el, str):
					el = {"query": el}

				if "query" not in el:
					raise ValueError(f"Missing 'name' key for {el}")

				name = el["query"]
				clean_name = name.replace("/", "_")
				if self.debug:
					print(f"Downloading {name}...")

				for inp in self.inputs:
					module_name = type(inp).__name__
					if self.debug:
						print(f"\t{module_name}")
					payload = inp._download(**el)

					if inp.bulk:
						if inp not in bulk_input:
							bulk_input[inp] = []
						bulk_input[inp].extend(payload)

					else:
						dump(
							file_name=f"{output_path.format(date=current_date, module=module_name, name=clean_name)}",
							obj_list=payload,
							output_format=inp.output_format,
						)
		finally:
			for inp, payload in bulk_input.items():
				dump(
					file_name=output_path.format(date=current_date, module=type(inp).__name__, name="bulk"),
					obj_list=payload,
					output_format=inp.output_format,
				)
