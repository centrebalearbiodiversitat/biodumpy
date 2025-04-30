import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import BOLD

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()


def bold_query(query, summary, output_format):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([BOLD(bulk=True, summary=summary, output_format=output_format)])
	bdp.start(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
	dir_module = os.listdir(f"{dynamic_path}/downloads/{dir_date}")[0]
	file_list = os.listdir(f"{dynamic_path}/downloads/{dir_date}/{dir_module}")[0]

	file = os.path.join(f"{dynamic_path}/downloads/{dir_date}/{dir_module}/{file_list}")
	if output_format == "json":
		with open(file, "r") as f:
			data = json.load(f)
	elif output_format == "fasta":
		with open(file, "r") as file:
			data = file.read()

	return data


def test_bold_initialization():
	# Test default initialization
	bold = BOLD()

	# Verify default parameters
	assert bold.summary == False
	assert bold.bulk == False
	assert bold.output_format == "json"

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match='Invalid output_format. Expected "json" or "fasta".'):
		BOLD(output_format="xml")


@pytest.mark.parametrize(
	"query, summary, output_format",
	[
		(["Alytes muletensis"], True, "json"),
		(["Alytes muletensis"], True, "json"),
		(["Alytes muletensis"], False, "json"),
		(["Alytes muletensis"], False, "fasta")
	]
)
def test_download(query, summary, output_format):
	with redirect_stdout(trap):
		data = bold_query(query=query, summary=summary, output_format=output_format)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	if summary is False and output_format != "fasta":
		# Check the main info in a BOLD JSON file
		data = data[0]

		# Check if data is not empty
		assert len(data) > 0, "data length is 0"

		assert "record_id" in data, "record_id is not in data"
		assert "processid" in data, "processid is not in data"
		assert "bin_uri" in data, "bin_uri is not in data"
		assert data["bin_uri"] == "BOLD:ABY0152", "bin_uri is not 'BOLD:ABY0152'"

		assert "specimen_identifiers" in data, "specimen_identifiers is not in data"
		sp_ident = data["specimen_identifiers"]
		assert "sampleid" in sp_ident, "specimen_identifiers is not in specimen_identifiers"
		assert "catalognum" in sp_ident, "catalognum is not in specimen_identifiers"
		assert "fieldnum" in sp_ident, "fieldnum is not in specimen_identifiers"
		assert "institution_storing" in sp_ident, "institution_storing is not in specimen_identifiers"

		assert "taxonomy" in data, "taxonomy is not in data"
		taxon = data["taxonomy"]
		assert "phylum" in taxon, "phylum is not in taxonomy"
		assert "class" in taxon, "class is not in taxonomy"
		assert "order" in taxon, "order is not in taxonomy"
		assert "family" in taxon, "family is not in taxonomy"
		assert "genus" in taxon, "genus is not in taxonomy"
		assert "species" in taxon, "species is not in taxonomy"
		species = taxon["species"]["taxon"]
		assert "taxID" in species, "taxID is not in species level"
		assert "name" in species, "name is not in species level"
		assert "reference" in species, "reference is not in species level"
		assert species["taxID"] == "455292", "species taxID is not in 455292"
		assert species["name"] == "Alytes muletensis", "species name is not in Alytes muletensis"
		assert species["reference"] == "(Sanchíz and Adrover, 1979)", "species reference is not in (Sanchíz and Adrover, 1979)"

		assert "specimen_desc" in data, "specimen_desc is not in data"
		sp_desc = data["specimen_desc"]
		assert "voucher_status" in sp_desc, "voucher_status is not in specimen_desc"
		assert "extrainfo" in sp_desc, "extrainfo is not in specimen_desc"

		assert "collection_event" in data, "collection_event is not in data"
		coll_event = data["collection_event"]
		assert "collectors" in coll_event, "collectors is not in collection_event"
		assert "country" in coll_event, "country is not in collection_event"

		assert "sequences" in data, "sequences is not in data"
		seq = data["sequences"]["sequence"][0]
		assert "sequenceID" in seq, "sequenceID is not in sequences"
		assert "markercode" in seq, "markercode is not in sequences"
		assert "genbank_accession" in seq, "genbank_accession is not in sequences"
		assert "nucleotides" in seq, "nucleotides is not in sequences"

	if summary and output_format != "fasta":
		# Check the summary structure
		assert "record_id" in data[0], "record_id is not in data"
		assert "processid" in data[0], "processid is not in data"
		assert "bin_uri" in data[0], "bin_uri is not in data"
		assert "taxon" in data[0], "taxon is not in data"
		assert "country" in data[0], "country is not in data"
		assert "province_state" in data[0], "province_state is not in data"
		assert "region" in data[0], "region is not in data"
		assert "lat" in data[0], "lat is not in data"
		assert "lon" in data[0], "lon is not in data"
		assert "markercode" in data[0], "markercode is not in data"
		assert "genbank_accession" in data[0], "genbank_accession is not in data"

	if summary is False and output_format == "fasta":
		# Check if the fasta file starts with >
		assert data.startswith(">")
