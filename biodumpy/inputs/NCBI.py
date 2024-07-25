import json

from biodumpy import Input
from biodumpy.utils import split_to_batches

from tqdm import tqdm
import time
from Bio import Entrez, SeqIO
from http.client import IncompleteRead
import logging


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


class NCBI(Input):
	def __init__(self, mail, output_format="json", bulk=False, db="nucleotide", rettype="gb", step=100, max_bp=None):
		super().__init__(output_format, bulk)
		self.max_bp = max_bp
		self.db = db
		self.step = step
		self.rettype = rettype
		Entrez.email = mail

		if output_format == "fasta" and rettype != "fasta":
			raise ValueError("rettype must be fasta.")

	def download(self, query, **kwargs) -> list:
		ids_list = self.download_ids(term=f"{query}[Organism]", step=self.step)

		payload = []
		with tqdm(total=len(ids_list), desc="NCBI sequences retrieve", unit=" Sequences") as pbar:
			for seq_id in split_to_batches(list(ids_list), self.step):
				for seq in self.download_seq(seq_id, rettype=self.rettype):
					payload.append(json.loads(json.dumps(seq, cls=CustomEncoder)))
				pbar.update(len(seq_id))
		return payload

	def download_ids(self, term, step):
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

		handle = Entrez.esearch(db=self.db, term=term, retmax=0)
		record = Entrez.read(handle)
		handle.close()

		id_bp_list = set()
		total_ids = int(record["Count"])
		with tqdm(total=total_ids, desc="NCBI IDs retrieve", unit=" IDs") as pbar:
			for start in range(0, total_ids, step):
				try:
					handle = Entrez.esearch(db=self.db, retstart=start, retmax=step, term=term)
					record = Entrez.read(handle)
					handle.close()

					if self.max_bp:
						# Retrieve summaries and calculate total bp
						summary_handle = Entrez.esummary(db=self.db, id=",".join(record["IdList"]))
						summaries = Entrez.read(summary_handle)
						summary_handle.close()

						for summary in summaries:
							bp = int(summary["Length"])
							if bp <= self.max_bp and summary["Id"] not in id_bp_list:  # Ensure unique entries
								id_bp_list.add(summary["Id"])

					else:
						id_bp_list.update(record["IdList"])

					pbar.update(len(record["IdList"]))
				except Exception as e:
					print(f"Error retrieving IDs or summaries: {e}")
					break

		return id_bp_list

	def download_seq(self, seq_id, rettype="gb", retmode="text", retries=3, webenv=None, query_key=None, history="y"):
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

		attempt = 0
		while attempt < retries:
			try:
				handle = Entrez.efetch(
					db="nucleotide", id=seq_id, rettype=rettype, retmode=retmode, usehistory=history, WebEnv=webenv, query_key=query_key
				)

				if self.rettype == "fasta":
					return handle.read().split("\n\n")[:-1]
				else:
					parsed_records = SeqIO.parse(handle, rettype)
					return SeqIO.to_dict(parsed_records).values()
			except IncompleteRead as e:
				# logging.warning(f"IncompleteRead error: {e}. Retrying {attempt + 1}/{retries}...")
				print(f"IncompleteRead error: {e}. Retrying {attempt + 1}/{retries}...")
				attempt += 1
				time.sleep(2)  # Wait before retrying

			except Exception as e:
				# logging.error(f"Error downloading or processing record: {e}")
				print(f"Error downloading or processing record: {e}")
				break

		if attempt == retries:
			# logging.error(f"Failed to download record {seq_id} after {retries} attempts.")
			print(f"Failed to download record {seq_id} after {retries} attempts.")

	@staticmethod
	def taxonomy_id(taxon: str, lineage=False, mail="A.N.Other@example.com"):
		"""
		Download taxonomy of a taxon from NCBI Taxonomy database.

		Args:
			taxon: String containing taxon name.
			lineage: If False retrieve only the ID of the specific taxon. If True, retrieve the IDs also for the superior taxonomic levels.
			mail: NCBI requires you to specify your email address with each request.

		Returns:
			List of elements.

		Example:
		x = download_taxonomy('Alytes muletensis')
		"""

		Entrez.email = mail

		# Retrieve taxonomy ID by taxon name
		handle = Entrez.esearch(db="Taxonomy", term=f"{taxon}[All Names]", retmode="xml")
		taxon_id = Entrez.read(handle)  # retrieve taxon ID
		handle.close()

		lin = []

		if int(taxon_id["Count"]) > 0:
			# Retrieve taxonomy by taxon ID
			handle = Entrez.efetch(db="Taxonomy", id=taxon_id["IdList"], retmode="xml")
			records = Entrez.read(handle)
			handle.close()

			if lineage is True:
				# Iterate through each dictionary in the list
				for taxonomy_info in records[0]["LineageEx"]:
					# Create a dictionary for the current taxonomy info
					taxonomy_dict = {
						"TaxId": taxonomy_info.get("TaxId", ""),
						"ScientificName": taxonomy_info.get("ScientificName", ""),
						"Rank": taxonomy_info.get("Rank", ""),
					}

					# Append the current taxonomy dictionary to lin list
					lin.append(taxonomy_dict)

				lin.append(
					{"TaxId": records[0]["TaxId"], "ScientificName": records[0]["ScientificName"].split()[-1], "Rank": records[0]["Rank"]}
				)

			else:
				lin = {"TaxId": records[0]["TaxId"], "ScientificName": records[0]["ScientificName"], "Rank": records[0]["Rank"]}

		return lin
