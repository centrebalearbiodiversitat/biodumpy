import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import NCBI

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()


def ncbi_query(query, summary, output_format, max_bp, db, step, rettype, query_type, by_id, mail):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy(
		[
			NCBI(
				bulk=True,
				summary=summary,
				output_format=output_format,
				max_bp=max_bp,
				db=db,
				step=step,
				rettype=rettype,
				query_type=query_type,
				by_id=by_id,
				mail=mail,
			)
		]
	)
	bdp.download_data(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

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


def test_ncbi_initialization():
	# Test default initialization
	ncbi = NCBI()

	# Verify default parameters
	assert ncbi.db == "nucleotide"
	assert ncbi.rettype == "gb"
	assert ncbi.query_type == "[Organism]"
	assert ncbi.step == 100
	assert ncbi.max_bp is None
	assert ncbi.summary == False
	assert ncbi.by_id == False
	assert ncbi.bulk == False
	assert ncbi.output_format == "json"

	with pytest.raises(ValueError, match="Invalid output_format. Expected fasta."):
		NCBI(output_format="fasta", rettype="gb")  # Should raise the error

	with pytest.raises(ValueError, match="Invalid parameters: 'by_id' is True, so 'query_type' must be None."):
		NCBI(by_id=True, query_type="[Organism]")  # Should raise the error

	with pytest.raises(ValueError, match="Invalid parameters: 'summary' is True, so 'output_format' cannot be 'fasta'."):
		NCBI(summary=True, output_format="fasta", rettype="fasta")  # Should raise the error

	with pytest.raises(ValueError, match='Invalid output_format. Expected "json" or "fasta".'):
		NCBI(output_format="xml")  # Should raise the error


@pytest.mark.parametrize(
	"query, summary, output_format, max_bp, db, step, rettype, query_type, by_id, mail",
	[
		(["Anax imperator"], False, "json", 5000, "nucleotide", 100, "gb", "[Organism]", False, "hola@quetal.com"),
		(["Anax imperator"], False, "json", 5000, "nucleotide", 100, "gb", "[Organism] AND COX1[Gene]", False, "hola@quetal.com"),
		(["OQ507551"], False, "json", 5000, "nucleotide", 100, "gb", None, True, "hola@quetal.com"),
		(["Anax imperator"], True, "json", 5000, "nucleotide", 100, "gb", "[Organism]", False, "hola@quetal.com"),
		(["Anax imperator"], False, "fasta", 5000, "nucleotide", 100, "fasta", "[Organism]", False, "hola@quetal.com"),
	],
)
def test_download(query, summary, output_format, max_bp, db, step, rettype, query_type, by_id, mail):
	with redirect_stdout(trap):
		data = ncbi_query(
			query=query,
			summary=summary,
			output_format=output_format,
			max_bp=max_bp,
			db=db,
			step=step,
			rettype=rettype,
			query_type=query_type,
			by_id=by_id,
			mail=mail,
		)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	if output_format != "fasta" and summary is False:
		data = data[0]
		assert "_seq" in data, "seq is not in data"
		assert "id" in data, "id is not in data"
		assert "name" in data, "name is not in data"
		assert "description" in data, "description is not in data"
		assert "annotations" in data, "annotations is not in data"
		assert "features" in data, "features is not in data"

	if summary and output_format != "fasta":
		data = data[0]
		assert "Id" in data, "Id is not in data"
		assert "Caption" in data, "Caption is not in data"
		assert "Title" in data, "Title is not in data"
		assert "Length" in data, "Length is not in data"
		assert "query" in data, "query is not in data"

	if summary is False and output_format == "fasta":
		# Check if the fasta file starts with >
		assert data.startswith(">")
