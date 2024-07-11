import json

from biodumpy import Input
from biodumpy.utils import split_to_batches

# Load packages
from tqdm import tqdm
# from dateutil.parser import parse
from datetime import datetime
# import pandas as pd
import string
import time
from Bio import Entrez, SeqIO
from http.client import IncompleteRead
import logging
# import geopandas as gpd
# import numpy as np
# import requests


#----------------------------------------------------------------------------------------------------------------------#
# Copy the list csv file to the server
# scp /Users/tcanc/PycharmProjects/ncbi_download/Lists/Reptilia_cbbdatabase.csv tca352@172.30.248.133:/home/tca352/Desktop/Downmer/Lists

#----------------------------------------------------------------------------------------------------------------------#
# class EFAnalyzer:
#     """
#     A class to download and parse NCBI records using Entrez.
#
#     Attributes:
#     result (list): List to store parsed records.
#     total (int): Total number of records expected to process.
#
#     Methods:
#     download_and_parse_record(organism_id, rettype="gb", retmode="text", save_path=None,
#                               retries=3, webenv=None, query_key=None):
#         Downloads a full Entrez record, saves it to a file, parses it, and updates the result.
#
#     Example usage:
#     analyzer = EFAnalyzer()
#     analyzer.download_and_parse_record(organism_id="AY341621", rettype="gb", retmode="text")
#     print(analyzer.result)
#     """
#
#     # TEMP_FILE = "temp.gb"
#
#     def __init__(self):
#         self.result = []
#         self.total = 0  # or any total number you expect to process
#
#     def download_and_parse_record(self, organism_id, rettype='gb', retmode='text',
#                                   retries=3, webenv=None, query_key=None, history='y'):
#
#         """
#         Downloads a full Entrez record, saves it to a file, parses it, and updates the result.
#
#         Args:
#             organism_id: NCBI database ID of the record to download.
#             rettype: Entrez return type (e.g., "gbwithparts").
#             retmode: Entrez return mode (e.g., "text").
#             retries: Number of retries in case of a connection error.
#             webenv: Web environment key for NCBI history.
#             query_key: Query key for NCBI history.
#
#         Returns:
#             None
#         """
#         #if save_path is None:
#             # save_path = EFAnalyzer.TEMP_FILE
#
#         attempt = 0
#         while attempt < retries:
#             try:
#                 # print("Connecting to NCBI...")
#                 handle = Entrez.efetch(db='nucleotide', id=organism_id, rettype=rettype, retmode=retmode,
#                                        usehistory=history, WebEnv=webenv, query_key=query_key)
#
#                 parsed_records = SeqIO.parse(handle, rettype)
#                 parsed_dict = SeqIO.to_dict(parsed_records)
#
#                 self.result.extend(parsed_dict.values())
#
#                 logging.info (f'{len (self.result)}/{self.total}...{len (self.result) * 100 / self.total:.1f}% ----  {organism_id}')
#                 print(f'{len(self.result)}/{self.total}...{len(self.result) * 100 / self.total:.1f}%')
#                 break
#
#             except IncompleteRead as e:
#                 logging.warning (f"IncompleteRead error: {e}. Retrying {attempt + 1}/{retries}...")
#                 print(f"IncompleteRead error: {e}. Retrying {attempt + 1}/{retries}...")
#                 attempt += 1
#                 time.sleep(2)  # Wait before retrying
#
#             except Exception as e:
#                 logging.error (f"Error downloading or processing record: {e}")
#                 print(f"Error downloading or processing record: {e}")
#                 break
#
#         if attempt == retries:
#             logging.error (f"Failed to download record {organism_id} after {retries} attempts.")
#             print(f"Failed to download record {organism_id} after {retries} attempts.")
#
# def download_taxonomy(taxon: str, mail='A.N.Other@example.com'):
#     """
#     Download taxonomy of a taxon from NCBI Taxonomy database.
#
#     Args:
#         taxon: String containing taxon name.
#         mail: NCBI requires you to specify your email address with each request.
#
#     Returns:
#         None
#
#     Example:
#     x = download_taxonomy('Alytes muletensis')
#     """
#
#     Entrez.email = mail
#
#     # Retrieve taxonomy ID by taxon name
#     handle = Entrez.esearch(db='Taxonomy', term=f'{taxon}[All Names]', retmode='xml')
#     taxon_id = Entrez.read(handle)  # retrieve taxon ID
#     handle.close ()
#
#     if int(taxon_id['Count']) > 0:
#
#         # Retrieve taxonomy by taxon ID
#         handle = Entrez.efetch(db='Taxonomy', id=taxon_id['IdList'], retmode='xml')
#         records = Entrez.read(handle)
#         handle.close ()
#
#         lin = records[0]['LineageEx']
#         df = pd.DataFrame(lin)
#
#         # if records[0]['Rank'] == 'species':
#         #     specificEpithet = records[0]['ScientificName'].split ()[-1]
#         # elif records[0]['Rank'] == 'subspecies':
#         #     specificEpithet = records[0]['ScientificName'].split ()[-2]
#         # else:
#         #     specificEpithet = None
#
#         new_row = {'TaxId': records[0]['TaxId'], 'ScientificName': records[0]['ScientificName'].split ()[-1], 'Rank': records[0]['Rank']}
#         df.loc[len (df)] = new_row
#         df = df.to_dict()
#
#     else:
#         df = None
#
#     return df
# x = download_taxonomy('Alytes muletensis')
#
# def parse_lat_lon(lat_lon: str):
#     """
#     Parse coordinate.
#
#     Args:
#         lat_lon: String containing latitude and longitude.
#
#     Returns:
#         None
#
#     Example:
#     parse_lat_lon("34.0522 N 118.2437 E")
#     [34.0522, 118.2437]
#     """
#
#     if not lat_lon:
#         return None
#
#     lat_lon = lat_lon.split(' ')
#     lat = float(lat_lon[0])
#     lon = float(lat_lon[2])
#
#     if lat_lon[1] == 'S':
#         lat = -lat
#     if lat_lon[3] == 'W':
#         lon = -lon
#
#     return [lat, lon]
#
# def parse_coordinates(input_string: str):
#     """
#     Split a string of coordinates and converts it to a tuple of floats.
#
#     The function removes square brackets from the input string, splits the string
#     by commas, strips any extra whitespace, and converts the split values to floats.
#
#     Parameters:
#     input_string (str): A string representing a couple of coordinates, e.g., "[1.23, 4.56]".
#
#     Returns:
#     tuple: A tuple of floats representing the coordinates.
#
#     Example usage:
#     input_string = "[1.23, 4.56]"
#     coordinates = parse_coordinates(input_string)
#     print(coordinates)
#     """
#
#     # Remove the square brackets
#     cleaned_string = input_string.strip('[]')
#
#     # Split the string by comma and strip any extra whitespace
#     split_values = [value.strip() for value in cleaned_string.split(',')]
#
#     # Convert the split string values to floats
#     float_values = tuple(float(value) for value in split_values)
#
#     return float_values
#
# def pars_date(date):
#     """
#     Parse date into YYYY-MM-DD.
#
#     Args:
#         date: String containing date.
#
#     Returns:
#         None
#
#     Example:
#         pars_date("2023-07-15")
#         {'year': 2023, 'month': 7, 'day': 15}
#     """
#
#     try:
#         parsed_date = parse(date, default=datetime (1, 1, 1))
#         parsed_date_alt = parse(date, default=datetime (2, 2, 2))
#
#         return {
#             'year': parsed_date.year if parsed_date.year == parsed_date_alt.year else None,
#             'month': parsed_date.month if parsed_date.month == parsed_date_alt.month else None,
#             'day': parsed_date.day if parsed_date.day == parsed_date_alt.day else None
#         }
#     except ValueError:
#         # Handle parsing errors (e.g., invalid date format)
#         return {
#             'year': None,
#             'month': None,
#             'day': None
#         }
#
# def sub_comma(input_string: str):
#     """
#     Parse date into YYYY-MM-DD.
#
#     Args:
#         input_string: String.
#
#     Returns:
#         None
#
#     Example:
#     sub_comma("Hello, world! How's everything going?")
#     {'year': 2023, 'month': 7, 'day': 15}
#     """
#
#     # Define a translation table to replace punctuation with commas
#     translation_table = str.maketrans(string.punctuation, ',' * len(string.punctuation))
#     result_string = input_string.translate(translation_table)
#
#     return result_string
#
# def divide_list_into_batches_by_size(input_list, batch_size: int):
#     """
#     Divides a list into smaller batches of a specified size.
#
#     Parameters:
#     input_list (list): The list to be divided into batches.
#     batch_size (int): The size of each batch.
#
#     Returns:
#     list of lists: A list containing the smaller batches.
#
#     Example usage:
#     input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#     batch_size = 3
#     batches = divide_list_into_batches_by_size(input_list, batch_size)
#     print(batches)  # Output: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#     """
#
#     return [input_list[i:i+batch_size] for i in range(0, len(input_list), batch_size)]
#
#
# #----------------------------------------------------------------------------------------------------------------------#
#
# # Set output directory, the number of records present in each batch of sequences, and the maximum number of bp to retrieve
# # with the first download
# output_directory = '/Users/tcanc/PycharmProjects/ncbi_download/NCBI/download_AMPHIBIA'
# num_batches = 40
# max_nbp = 5000 # Maximum number of BP
#
# # Set log configuration
# log_filename = datetime.now().strftime(f'{output_directory}/logs/Log_NCBI_%Y%m%d.log')
# logging.basicConfig(filename=log_filename, level=logging.INFO, force=True)
#
# # Download sequences from NCBI
# for taxa in sp:
#
#     taxon = taxa
#
#     mail = 'hola@domain.com'
#     Entrez.email = mail
#
#     current_date = datetime.now().strftime('%Y-%m-%d')
#
#     # Retrieve taxonomy ID by taxon name
#     handle = Entrez.esearch(db='Taxonomy', term=f'{taxon}[All Names]', retmode='xml')
#     taxon_id = Entrez.read(handle)  # retrieve taxon ID
#
#     if int(taxon_id['Count']) > 0:
#
#         # Retrieve taxonomy by taxon ID
#         handle = Entrez.efetch(db='Taxonomy', id=taxon_id['IdList'], retmode='xml')
#         records = Entrez.read(handle)
#         handle.close()
#
#         lin = records[0]['LineageEx']
#         df = pd.DataFrame(lin)
#
#         if records[0]['Rank'] == 'species':
#             specificEpithet = records[0]['ScientificName'].split ()[-1]
#         elif records[0]['Rank'] == 'subspecies':
#             specificEpithet = records[0]['ScientificName'].split ()[-2]
#         else:
#             specificEpithet = None
#
#
#         # Retrieve IDs and number of bp for each id. Then, we save a .csv file into the BP folder
#         a =
#         # a = download_NCBI_ids_and_count_bp (term=f'{taxon}[Organism]', step=100, db='nucleotide', mail=mail)
#         for dictionary in a[0]:
#             dictionary['taxon'] = taxon
#
#         # Download and parse genetic metadata #####
#         # Filter records with bp <= max_nbp
#         filtered_records = [record['id'] for record in a[0] if record['bp'] <= max_nbp]
#
#         if len(filtered_records) > 0:
#             # Initialize the analyzer
#             analyzer = EFAnalyzer()
#             analyzer.total = len(filtered_records)  # Set the expected total number of sequences
#         else:
#             analyzer = EFAnalyzer()
#             analyzer.total = 0
#             filtered_records = None
#
#     else:
#         analyzer = EFAnalyzer()
#         analyzer.total = 0
#         filtered_records = None
#
#     if analyzer.total > 0 and len(filtered_records) > 0:
#         # Get the WebEnv and QueryKey from the initial search to use in subsequent fetches
#         handle = Entrez.esearch(db='nucleotide', term=f'txid{taxon_id["IdList"][0]}[Organism]', retmax=0, usehistory="y")
#         record = Entrez.read(handle)
#         handle.close()
#         webenv = record['WebEnv']
#         query_key = record['QueryKey']
#
#         # Divide the list of ids in batches
#         batches = divide_list_into_batches_by_size(filtered_records, num_batches)
#
#         # Loop over the retrieved IDs and process each
#         for batch in batches:  # Adjust the slice to your needs
#             batch_ids = ','.join(batch)
#             analyzer.download_and_parse_record(organism_id=batch_ids, rettype='gb', retmode='text',
#                                                webenv=webenv, query_key=query_key)
#             x = analyzer.result
#             print(f'{taxon} \n {batch_ids}\n')
#
#         # Create the object containing parsed data
#         parsed_data = []
#         for i in range(len(x)):
#
#             y = x[i]
#             date_string = y.features[0].qualifiers.get('collection_date', [None])[0]
#
#             parsed_data.append ({
#                 'originalName': taxon,
#                 'sample_id': y.name,
#                 'taxonKey': taxon_id['IdList'][0],
#                 'acceptedTaxonKey': taxon_id['IdList'][0],
#                 'voucher': y.features[0].qualifiers.get ('specimen_voucher', [None])[0],
#                 'basisOfRecord': None,
#                 'occurrenceStatus': None,
#                 'kingdom': df[df['Rank'] == 'kingdom']['ScientificName'].iloc[0] if df['Rank'].isin (
#                     ['kingdom']).any () else None,
#                 'phylum': df[df['Rank'] == 'phylum']['ScientificName'].iloc[0] if df['Rank'].isin (
#                     ['phylum']).any () else None,
#                 'class': df[df['Rank'] == 'class']['ScientificName'].iloc[0] if df['Rank'].isin (
#                     ['class']).any () else None,
#                 'order': df[df['Rank'] == 'order']['ScientificName'].iloc[0] if df['Rank'].isin (
#                     ['order']).any () else None,
#                 'family': df[df['Rank'] == 'family']['ScientificName'].iloc[0] if df['Rank'].isin (
#                     ['family']).any () else None,
#                 'genus': df[df['Rank'] == 'genus']['ScientificName'].iloc[0] if df['Rank'].isin (
#                     ['genus']).any () else None,
#                 'specificEpithet': specificEpithet,
#                 'infraspecificEpithet': records[0]['ScientificName'].split ()[-1] if records[0][
#                                                                                          'Rank'] == 'subspecies' else None,
#                 'kingdomKey': df[df['Rank'] == 'kingdom']['TaxId'].iloc[0] if df['Rank'].isin (
#                     ['kingdom']).any () else None,
#                 'phylumKey': df[df['Rank'] == 'phylum']['TaxId'].iloc[0] if df['Rank'].isin (
#                     ['phylum']).any () else None,
#                 'classKey': df[df['Rank'] == 'class']['TaxId'].iloc[0] if df['Rank'].isin (['class']).any () else None,
#                 'orderKey': df[df['Rank'] == 'order']['TaxId'].iloc[0] if df['Rank'].isin (['order']).any () else None,
#                 'familyKey': df[df['Rank'] == 'family']['TaxId'].iloc[0] if df['Rank'].isin (
#                     ['family']).any () else None,
#                 'genusKey': df[df['Rank'] == 'genus']['TaxId'].iloc[0] if df['Rank'].isin (['genus']).any () else None,
#                 'speciesKey': records[0]['TaxId'].split ()[-1] if records[0]['Rank'] == 'species' else None,
#                 'subspeciesKey': records[0]['TaxId'].split ()[-1] if records[0]['Rank'] == 'subspecies' else None,
#                 'taxonRank': records[0]['Rank'],
#                 'taxonomicStatus': None,
#                 'iucnRedListCategory': None,
#                 'lat_lon': parse_lat_lon (y.features[0].qualifiers.get ('lat_lon', [None])[0]),
#                 'continent': None,
#                 'islandGroup': None,
#                 'island': None,
#                 'country': None,
#                 'countryCode': None,
#                 'stateProvince': None,
#                 'county': None,
#                 'municipality': None,
#                 'locality': sub_comma (y.features[0].qualifiers.get ('geo_loc_name', [None])[0]) if
#                 y.features[0].qualifiers.get ('geo_loc_name', [None])[0] else None,
#                 'geography': [sub_comma (y.features[0].qualifiers.get ('geo_loc_name', [None])[0]) if
#                               y.features[0].qualifiers.get ('geo_loc_name', [None])[0] else None],
#                 'geodeticDatum': None,
#                 'coordinateUncertaintyInMeters': None,
#                 'date1': date_string,
#                 'year': None if date_string is None else pars_date (date_string)['year'],
#                 'month': None if date_string is None else pars_date (date_string)['month'],
#                 'day': None if date_string is None else pars_date (date_string)['day'],
#                 'lifeStage': None,
#                 'recordedBy': y.features[0].qualifiers.get ('collected_by', [None])[0],
#                 'elevation': None,
#                 'depth': None,
#                 'occurrenceSource': 'NCBI',
#                 'occurrenceOrigin': 'database',
#                 # 'geometry': None,
#                 'CONTINENT': None,
#                 'COUNTRY': None,
#                 'AC': None,
#                 'ISLAND': None,
#                 'MUNICIPALI': None,
#                 'TOWN': None,
#                 'WB_0': None,
#                 "isolate": y.features[0].qualifiers.get ('isolate', [None])[0],
#                 "bp": len (y),
#                 "definition": y.description,
#                 "data_file_division": y.annotations.get ('data_file_division', None),
#                 "date": y.annotations.get ('date', None),
#                 "molecule_type": y.annotations.get ('molecule_type', None),
#                 "sequence_version": y.annotations.get ('sequence_version', None),
#                 "references": [{
#                     "authors": ref.authors,
#                     "title": ref.title,
#                     "journal": ref.journal,
#                 } for ref in y.annotations.get ('references', [])],
#                 "genetic_features": [{
#                     "gene": ref.qualifiers.get ('gene', [None])[0],
#                     "product": ref.qualifiers.get ('product', [None])[0],
#                 } for ref in y.features if "gene" in ref.qualifiers or "product" in ref.qualifiers]
#             })
#
#         # Specify the file name and save the .csv
#         filename = f'{output_directory}/sequences/{taxon}_{current_date}'
#
#         print (f'Saving METADATA .csv.....\n')
#         headers = parsed_data[0].keys()
#         dump_to_csv(filename, headers, parsed_data)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return super().default(obj)


class NCBI(Input):
	def __init__(self, mail, db='nucleotide', step=100, max_bp=5000):
		super().__init__()
		self.max_bp = max_bp
		self.db = db
		self.step = step
		# self.parse_data = parse_data
		Entrez.email = mail

	def download(self, query, **kwargs) -> list:
		ids_list = self.download_ids(term=query, step=self.step)

		payload = []
		with tqdm(total=len(ids_list), desc="NCBI sequences retrieve", unit=" Sequences") as pbar:
			for seq_id in split_to_batches(list(ids_list), self.step):
				# payload.extend(self.download_seq(seq_id).values())
				for seq in self.download_seq(seq_id).values():
					payload.append(json.loads(json.dumps(seq, cls=CustomEncoder)))
				# logging.info(f'{len(payload)}/{len(ids_list)}...{len(self.result) * 100 / self.total:.1f}% ----  {seq_id}')
				# print(f'{len(self.result)}/{self.total}...{len(self.result) * 100 / self.total:.1f}%')
				pbar.update(len(seq_id))
		return payload

	"""
		Downloads NCBI IDs based on a search term and counts the total base pairs (bp) for the retrieved sequences.

		Parameters:
		term (str): Search term for querying the NCBI database.
		db (str): NCBI database to search (default is 'nucleotide').
		step (int): Number of IDs to retrieve per batch (default is 10).
		mail (str): Email address to be used with Entrez (required by NCBI).

		Returns:
		tuple: A list of dictionaries with 'id' and 'bp' keys, and the total count of base pairs.

		Example usage:
		id_bp_list, total_bp = download_NCBI_ids_and_count_bp(term="Alytes muletensis[Organism]", db='nucleotide', step=10, mail='your-email@example.com')
		print(id_bp_list)
		"""
	def download_ids(self, term, step):
		handle = Entrez.esearch(db=self.db, term=term, retmax=0)
		record = Entrez.read(handle)
		handle.close()

		id_bp_list = set()
		total_ids = int(record['Count'])
		with tqdm(total=total_ids, desc="NCBI IDs retrieve", unit=" IDs") as pbar:
			for start in range(0, total_ids, step):
				try:
					handle = Entrez.esearch(db=self.db, retstart=start, retmax=step, term=term)
					record = Entrez.read(handle)
					handle.close()

					# Retrieve summaries and calculate total bp
					summary_handle = Entrez.esummary(db=self.db, id=",".join(record['IdList']))
					summaries = Entrez.read(summary_handle)
					summary_handle.close()

					for summary in summaries:
						bp = int(summary['Length'])
						if bp <= self.max_bp and summary['Id'] not in id_bp_list:  # Ensure unique entries
							id_bp_list.add(summary['Id'])

					pbar.update(len(record['IdList']))
				except Exception as e:
					print(f'Error retrieving IDs or summaries: {e}')
					break

		return id_bp_list

	"""
	Downloads a full Entrez record, saves it to a file, parses it, and updates the result.
	
	Args:
		organism_id: NCBI database ID of the record to download.
		rettype: Entrez return type (e.g., "gbwithparts").
		retmode: Entrez return mode (e.g., "text").
		retries: Number of retries in case of a connection error.
		webenv: Web environment key for NCBI history.
		query_key: Query key for NCBI history.

	Returns:
		A list of sequences.
	"""
	def download_seq(self, seq_id, rettype='gb', retmode='text', retries=3, webenv=None, query_key=None, history='y'):
		attempt = 0
		while attempt < retries:
			try:

				handle = Entrez.efetch(db='nucleotide', id=seq_id, rettype=rettype, retmode=retmode, usehistory=history, WebEnv=webenv, query_key=query_key)
				parsed_records = SeqIO.parse(handle, rettype)

				return SeqIO.to_dict(parsed_records)

			except IncompleteRead as e:
				logging.warning (f"IncompleteRead error: {e}. Retrying {attempt + 1}/{retries}...")
				print(f"IncompleteRead error: {e}. Retrying {attempt + 1}/{retries}...")
				attempt += 1
				time.sleep(2)  # Wait before retrying

			except Exception as e:
				logging.error (f"Error downloading or processing record: {e}")
				print(f"Error downloading or processing record: {e}")
				break

		if attempt == retries:
			logging.error (f"Failed to download record {seq_id} after {retries} attempts.")
			print(f"Failed to download record {seq_id} after {retries} attempts.")
