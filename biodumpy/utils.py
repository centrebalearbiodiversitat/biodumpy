import csv
import json
import os


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
	directory = os.path.dirname(file_name)
	if not os.path.exists(directory):
		os.makedirs(directory)


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


# def download_taxonomy(taxon: str, mail="A.N.Other@example.com"):
# 	"""
# 	Download taxonomy of a taxon from NCBI Taxonomy database.
#
# 	Args:
# 	    taxon: String containing taxon name.
# 	    mail: NCBI requires you to specify your email address with each request.
#
# 	Returns:
# 	    None
#
# 	Example:
# 	x = download_taxonomy('Alytes muletensis')
# 	"""
#
# 	Entrez.email = mail
#
# 	# Retrieve taxonomy ID by taxon name
# 	handle = Entrez.esearch(db="Taxonomy", term=f"{taxon}[All Names]", retmode="xml")
# 	taxon_id = Entrez.read(handle)  # retrieve taxon ID
# 	handle.close()
#
# 	if int(taxon_id["Count"]) > 0:
# 		# Retrieve taxonomy by taxon ID
# 		handle = Entrez.efetch(db="Taxonomy", id=taxon_id["IdList"], retmode="xml")
# 		records = Entrez.read(handle)
# 		handle.close()
#
# 		lin = records[0]["LineageEx"]
# 		lin.append = {"TaxId": records[0]["TaxId"], "ScientificName": records[0]["ScientificName"].split()[-1], "Rank": records[0]["Rank"]}
#
# 	else:
# 		lin = None
#
# 	return lin
