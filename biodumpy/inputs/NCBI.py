import json

from biodumpy import Input
from biodumpy.utils import split_to_batches

from tqdm import tqdm
import time
from Bio import Entrez, SeqIO
from http.client import IncompleteRead


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
	"""
	Query the National Center for Biotechnology Information (NCBI) database to retrieve taxon retlated data.

	Parameters
	----------
	query : list
	    A list of taxa to query in the BOLD database.
	mail : str, optional
	    Email address used with Entrez functions to identify the user.
	    This is required by NCBI to track usage and report problems.
	    Default is None.
	db : str, optional
	    NCBI database to search and download data from. Options include "nucleotide", "protein", "gene", and others.
	    Default is "nucleotide".
	rettype : str, optional
	    The format for data retrieval from NCBI. Common formats include 'gb' (GenBank), 'fasta', 'xml', etc.
	    Default is 'gb'.
	query_type : str, optional
	    Defines the type of query search, such as "[Organism]" or "[Gene]".
	    This determines how the query is interpreted by NCBI.
	    Default is "[Organism]".
	step : int, optional
	    Number of records to download per chunk. For example, if the total data to download is 10,000 and the step is set to 100,
	    the function will download in chunks of 100 records per request.
	    Default is 100.
	max_bp : int, optional
	    Maximum number of base pairs allowed for each sequence. Records with more base pairs than this value will be excluded.
	    If None, all records will be downloaded regardless of size.
	    Default is None.
	summary : bool, optional
	    If True, the function returns a summary of the downloaded metadata instead of the full records.
	    Default is False.
	by_id : bool, optional
		If True, the function downloads the data using NCBI accession numbers as inputs.
		Default is False.
	bulk : bool, optional
	    If True, the function creates a bulk file for large downloads.
	    For more information, refer to the Biodumpy package documentation.
	    Default is False.
	output_format : str, optional
	    The format of the output file. Available options are: 'json', 'fasta', 'pdf'.
	    Default is 'json'.

	Details
	-------
	When `summary` is True, the resulting JSON will include the following information:
	- `Id`: A numerical identifier (GI Number) that used to be assigned to each sequence version (e.g., "345678912").
	- `Caption`: A unique identifier (accession number) assigned to a sequence when it is submitted to GenBank (e.g., "NM_001256789").
	- `Title`: A short description or title of the sequence, often including information about the gene, organism, and type of sequence.
	- `Length`: The length of the sequence in base pairs (for nucleotide sequences) or amino acids (for protein sequences).
	- `query`: The original search term or query string used to retrieve this result.

	Example
	-------
	>>> from biodumpy import Biodumpy
	>>> from biodumpy.inputs import NCBI
	# List of taxa
	>>> taxa = ['Alytes muletensis', 'Hyla meridionalis', 'Anax imperator', 'Bufo roseus', 'Stollia betae']
	# Set the module and start the download
	>>> bdp = Biodumpy([NCBI(bulk=False, mail="hola@quetal.com", db="nucleotide", rettype="gb", query_type='[Organism]')])
	>>> bdp.start(taxa, output_path='./downloads/{date}/{module}/{name}')
	"""


	def __init__(
			self,
			mail: str = None,
			db: str = "nucleotide",
			rettype: str = "gb",
			query_type: str = "[Organism]",
			step: int = 100,
			max_bp: int = None,
			summary: bool = False,
			by_id: bool = False,
			output_format: str = "json",
			bulk: bool = False):

		super().__init__(output_format, bulk)
		self.max_bp = max_bp
		self.db = db
		self.step = step
		self.rettype = rettype
		self.query_type = query_type
		self.summary = summary
		self.by_id = by_id
		Entrez.email = mail

		if self.output_format == "fasta" and self.rettype != "fasta":
			raise ValueError("Invalid output_format. Expected fasta.")

		if self.by_id and self.query_type is not None:
			raise ValueError("Invalid parameters: 'by_id' is True, so 'query_type' must be None.")

		if self.summary and self.output_format == "fasta" and self.rettype == "fasta":
			raise ValueError("Invalid parameters: 'summary' is True, so 'output_format' cannot be 'fasta'.")

		if output_format not in {"json", "fasta"}:
			raise ValueError('Invalid output_format. Expected "json" or "fasta".')

	def _download(self, query, **kwargs) -> list:

		if self.by_id:
			ids_list = {query}
		else:
			ids_list = self._download_ids(term=f"{query}{self.query_type}", step=self.step)

		payload = []
		if self.summary:
			with tqdm(total=len(ids_list), desc="NCBI summary retrieve", unit=" Summary") as pbar:
				for seq_id in split_to_batches(list(ids_list), self.step):
					for sumr in self._download_summary(seq_id):
						sumr["query"] = f"{query}{self.query_type}"
						payload.append(json.loads(json.dumps(sumr, cls=CustomEncoder)))
					pbar.update(len(seq_id))

		else:
			with tqdm(total=len(ids_list), desc="NCBI sequences retrieve", unit=" Sequences") as pbar:
				for seq_id in split_to_batches(list(ids_list), self.step):
					for seq in self._download_seq(seq_id, rettype=self.rettype, db=self.db):
						payload.append(json.loads(json.dumps(seq, cls=CustomEncoder)))
					pbar.update(len(seq_id))

		return payload

	def _download_ids(self, term, step):
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

	def _download_summary(self, seq_id):

		keys_to_keep = ["Id", "Caption", "Title", "Length"]
		summary_list = list()
		try:
			summary_handle = Entrez.esummary(db=self.db, id=seq_id)
			summaries = Entrez.read(summary_handle)
			summary_handle.close()
			for summary in summaries:
				summary_list.append({key: summary[key] for key in keys_to_keep})
		except Exception as e:
			print(f"Error retrieving IDs or summaries: {e}")

		return summary_list

	def _download_seq(self, seq_id, db=None, rettype=None, retmode="text", retries=3, webenv=None, query_key=None, history="y"):
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
					db=db, id=seq_id, rettype=rettype, retmode=retmode, usehistory=history, WebEnv=webenv, query_key=query_key
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
