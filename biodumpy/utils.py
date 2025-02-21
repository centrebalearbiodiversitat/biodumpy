import csv
import json
import os
import re


class CustomEncoder(json.JSONEncoder):
	def default(self, obj):
		if hasattr(obj, "to_dict"):
			return obj.to_dict()
		elif hasattr(obj, "__dict__"):
			if obj.__dict__:
				return obj.__dict__
			else:
				try:
					return str(obj) if obj else None
				except Exception as e:
					return str(e)
		else:
			return super().default(obj)


def dump(file_name, obj_list, output_format="json"):
	"""
	Dump a list of objects to JSON files. Optionally split into multiple files for bulk processing.

	Parameters:
	    file_name (str): Base name of the output JSON file.
	    obj_list (list): List of objects to be written to JSON.
	    output_format: output format. Default is "json". Other formats can be "fasta", "pdf".
	"""

	create_directory(file_name)

	with open(f"{file_name}.{output_format}", "wb+" if output_format == "pdf" else "w+") as output_file:
		if output_format == "fasta":
			for line in obj_list:
				output_file.write(f"{line}\n")
		elif output_format == "pdf":
			output_file.write(obj_list)
		else:
			json.dump(obj_list, output_file, indent=4)


def create_directory(file_name):
	"""
	Creates a directory for the given file name if it does not already exist.

	Parameters:
	    file_name (str): The path of the file for which the directory should be created.

	Example:
	    create_directory('/path/to/directory/file.txt')
	    This will create '/path/to/directory/' if it does not already exist.
	"""

	directory = os.path.dirname(file_name)
	if not os.path.exists(directory):
		os.makedirs(directory)


def remove_tags(text: str) -> str:
	"""
	Removes XML/HTML-like tags from the input string.

	Args:
	    text (str): The input string containing tags.

	Returns:
	    str: The string with tags removed.
	"""
	# Use regular expression to remove tags
	clean_text = re.sub(r"<.*?>", "", text)
	return clean_text


def clean_nones(value):
	"""
	Recursively remove all None values from dictionaries and lists, and returns
	the result as a new dictionary or list.
	"""
	if isinstance(value, list):
		return [clean_nones(x) for x in value if x is not None]
	elif isinstance(value, dict):
		return {key: clean_nones(val) for key, val in value.items() if val is not None}
	else:
		return value


def dump_to_csv(file_name, obj_list):
	directory = os.path.dirname(file_name)
	if not os.path.exists(directory):
		os.makedirs(directory)

	headers = []
	unroll_headers = []
	if len(obj_list) > 0:
		headers = []
		unroll_headers = []
		for obj in obj_list:
			headers = list(obj_list[0].keys())
			for k, v in obj_list[0].items():
				if isinstance(v, dict):
					for kk, vv in v.items():
						unroll_headers.append(kk)
				else:
					unroll_headers.append(k)

	with open(file_name, mode="w+") as csv_file:
		writer = csv.DictWriter(csv_file, fieldnames=unroll_headers)

		writer.writeheader()
		for obj in obj_list:
			row = {}
			for field in headers:
				if field in obj:
					current = obj[field]
					if isinstance(current, list):
						row[field] = json.dumps(current)
					elif isinstance(current, dict):
						for k, v in current.items():
							row[k] = json.dumps(v) if isinstance(v, dict) or isinstance(v, list) else v
					else:
						row[field] = current
				else:
					row[field] = None

			writer.writerow(row)


def split_to_batches(input_list, batch_size: int):
	"""
	Divides a list into smaller batches of a specified size.

	Parameters:
	input_list (list): The list to be divided into batches.
	batch_size (int): The size of each batch.

	Returns:
	list of lists: A list containing the smaller batches.

	Example usage:
	input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	batch_size = 3
	batches = divide_list_into_batches_by_size(input_list, batch_size)
	print(batches)  # Output: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	"""
	return [input_list[i : i + batch_size] for i in range(0, len(input_list), batch_size)]


def parse_lat_lon(lat_lon: str):
	"""
	Parse coordinate.

	Args:
	    lat_lon: String containing latitude and longitude.

	Returns:
	    List of coordinates.

	Example:
	parse_lat_lon("34.0522 N 118.2437 E")
	[34.0522, 118.2437]
	"""

	if not lat_lon:
		return None

	lat_lon = lat_lon.split(" ")
	lat = float(lat_lon[0])
	lon = float(lat_lon[2])

	if lat_lon[1] == "S":
		lat = -lat
	if lat_lon[3] == "W":
		lon = -lon

	return [lat, lon]


def read_fasta(file_path: str) -> list:
	"""
	Reads a fasta file. The output is a list of dictionaries containing the sequences.

	Parameters
	----------

	file_path: str
	    Path of the fasta file.
	"""

	# Check if the file is .fasta.
	if not file_path.endswith((".fasta", ".fas", ".fa", ".fna", ".ffn", ".faa", ".mpfa", ".frn")):
		raise ValueError(f"Invalid file: '{file_path}'. Please provide a file with a correct extension.")

	sequences = []
	with open(file_path, "r") as file:
		sequence_id = None
		sequence_data = []

		for line in file:
			line = line.strip()
			if line.startswith(">"):  # Header line
				if sequence_id:  # Save the previous sequence
					sequences.append({"id": sequence_id, "sequence": "".join(sequence_data)})
				sequence_id = line[1:]  # Exclude '>'
				sequence_data = []
			else:
				sequence_data.append(line)

		if sequence_id:  # Save the last sequence
			sequences.append({"id": sequence_id, "sequence": "".join(sequence_data)})

	return sequences


def save_fasta(file_path: str, sequences: list):
	"""
	Save a list of sequences to a FASTA file.

	Parameters
	----------

	file_path:
	    Path to the output FASTA file.

	sequences:
	    List of dictionaries with 'id' and 'sequence' data.
	"""

	with open(file_path, "w") as file:
		for seq in sequences:
			# Write the header line (e.g., '>id')
			file.write(f">{seq['id']}\n" if isinstance(seq, dict) else f">{seq[0]}\n")
			# Write the sequence in multiple lines if needed
			sequence = seq["sequence"] if isinstance(seq, dict) else seq[1]
			for i in range(0, len(sequence), 80):  # Break the sequence into chunks of 80 characters
				file.write(sequence[i : i + 80] + "\n")


def haplo_collapse(fasta_file):
	"""
	Function to collapse haplotypes from FASTA file.

	Parameters
	----------
	fasta_file :
	    The input FASTA file containing the sequences to be collapsed.

	Details
	-------
	This function produce a list of dictionary containing two fields:
	    - sequence: Stores the genetic information of the sequence.
	    - ids: Contains the identifiers of all sequences that were collapsed into the respective sequence.

	Example
	-------
	>>> a = haplo_collapse(fasta_file)
	"""

	if not all("id" in item and "sequence" in item for item in fasta_file):
		raise ValueError("The FASTA format is not formatted correctly.")

	haplo = {}
	for item in fasta_file:
		key = item["id"]
		value = item["sequence"]

		if value not in haplo:
			haplo[value] = {"sequence": value, "ids": []}
		haplo[value]["ids"].append(key)

	return list(haplo.values())
