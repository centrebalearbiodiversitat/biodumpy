from datetime import datetime

from .input import Input
from .utils import dump_to_csv, dump_to_json


class Biodumpy:
	def __init__(self, inputs: list[Input]) -> None:
		super().__init__()
		self.inputs = inputs

	# elements must be a flat list of strings or dictionaries with "name" key
	def start(self, elements: list, output_path="downloads/{date}/{module}/{name}.json"):
		current_date = datetime.now().strftime('%Y-%m-%d')
		for el in elements:
			if isinstance(el, str):
				el = {"name": el}

			if "name" not in el:
				raise ValueError(f"Missing 'name' key for {el}")

			name = el['name']
			print(f'Downloading {name}...')

			for inp in self.inputs:
				module_name = type(inp).__name__
				print(f'\t{module_name}')
				payload = inp.download(**el)
				dump_to_json(
					output_path.format(date=current_date, module=module_name, name=name),
					payload
				)