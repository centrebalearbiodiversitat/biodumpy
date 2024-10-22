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


def ncbi_query(query, summary, output_format, max_bp, db, step_id, step_seq, rettype, query_type, by_id, taxonomy, taxonomy_only, mail):
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
				step_id=step_id,
				step_seq=step_seq,
				rettype=rettype,
				query_type=query_type,
				by_id=by_id,
				taxonomy=taxonomy,
				taxonomy_only=taxonomy_only,
				mail=mail,
			)
		]
	)
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


def test_ncbi_initialization():
	# Test default initialization
	ncbi = NCBI()

	# Verify default parameters
	assert ncbi.db == "nucleotide"
	assert ncbi.rettype == "gb"
	assert ncbi.query_type == "[Organism]"
	assert ncbi.step_id == 100
	assert ncbi.step_seq == 100
	assert ncbi.max_bp is None
	assert ncbi.summary == False
	assert ncbi.by_id == False
	assert ncbi.taxonomy == False
	assert ncbi.taxonomy_only == False
	assert ncbi.bulk == False
	assert ncbi.output_format == "json"

	with pytest.raises(ValueError, match="Invalid output_format. Expected fasta."):
		NCBI(output_format="fasta", rettype="gb")  # Should raise the error

	with pytest.raises(ValueError, match="Invalid parameters: 'by_id' is True, so 'query_type' must be None."):
		NCBI(by_id=True, query_type="[Organism]")  # Should raise the error

	with pytest.raises(ValueError, match="Invalid parameters: 'summary' is True, so 'output_format' cannot be 'fasta'."):
		NCBI(summary=True, output_format="fasta", rettype="fasta")  # Should raise the error

	with pytest.raises(ValueError, match="Invalid parameters: 'taxonomy' is True, so 'output_format' cannot be 'fasta'."):
		NCBI(taxonomy=True, output_format="fasta", rettype="fasta")  # Should raise the error

	with pytest.raises(ValueError, match="Invalid parameters: 'taxonomy_only' is True, so 'output_format' cannot be 'fasta'."):
		NCBI(taxonomy_only=True, output_format="fasta", rettype="fasta")  # Should raise the error

	with pytest.raises(ValueError, match='Invalid output_format. Expected "json" or "fasta".'):
		NCBI(output_format="xml")  # Should raise the error


@pytest.mark.parametrize(
	"query, summary, output_format, max_bp, db, step_id, step_seq, rettype, query_type, by_id, taxonomy, taxonomy_only, mail",
	[
		(["Alytes muletensis"], False, "json", 2000, "nucleotide", 100, 100, "gb", "[Organism]", False, False, False, "ok"),
		(["Alytes muletensis"], False, "json", 2000, "nucleotide", 100, 100, "gb", "[Organism] AND COX1[Gene]", False, False, False, "ok"),
		(["AY166960"], False, "json", 2000, "nucleotide", 100, 100, "gb", None, True, False, False, "ok"),
		(["Alytes muletensis"], True, "json", 2000, "nucleotide", 100, 100, "gb", "[Organism]", False, False, False, "ok"),
		(["Alytes muletensis"], False, "fasta", 2000, "nucleotide", 100, 100, "fasta", "[Organism]", False, False, False, "ok")
	],
)
def test_download(query, summary, output_format, max_bp, db, step_id, step_seq, rettype, query_type, by_id, taxonomy, taxonomy_only, mail):
	with redirect_stdout(trap):
		data = ncbi_query(
			query=query,
			summary=summary,
			output_format=output_format,
			max_bp=max_bp,
			db=db,
			step_id=step_id,
			step_seq=step_seq,
			rettype=rettype,
			query_type=query_type,
			by_id=by_id,
			taxonomy=taxonomy,
			taxonomy_only=taxonomy_only,
			mail=mail
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
		elem_annotations = [
			"molecule_type",
			"topology",
			"data_file_division",
			"date",
			"accessions",
			"sequence_version",
			"keywords",
			"source",
			"organism",
			"taxonomy",
			"references"
		]
		found_words = []
		for word in elem_annotations:
			if word in data["annotations"]:
				found_words.append(word)
		assert len(found_words) == 11, "Check the annotation list"

		assert "features" in data, "features is not in data"

	if summary and output_format != "fasta":
		data = data[0]
		assert "Id" in data, "Id is not in data"
		assert "Caption" in data, "Caption is not in data"
		assert "Title" in data, "Title is not in data"
		assert "Length" in data, "Length is not in data"
		assert "query" in data, "query is not in data"

		# Check if the length is lover than 2000
		assert data["Length"] < 2000, "Length is not in correct, is higher than 2000 bp"

	if summary is False and output_format == "fasta":
		# Check if the fasta file starts with >
		assert data.startswith(">")


@pytest.mark.parametrize(
	"query, summary, output_format, max_bp, db, step_id, step_seq, rettype, query_type, by_id, taxonomy, taxonomy_only, mail",
	[
		(["Alytes muletensis"], False, "json", 2000, "nucleotide", 100, 100, "gb", "[Organism]", False, True, False, "hola@quetal.com"),
		(["Alytes muletensis"], False, "json", 2000, "nucleotide", 100, 100, "gb", "[Organism]", False, False, True, "hola@quetal.com")
	],
)
def test_download_taxonomy(query, summary, output_format, max_bp, db, step_id, step_seq, rettype, query_type, by_id, taxonomy, taxonomy_only, mail):
	with redirect_stdout(trap):
		data = ncbi_query(
			query=query,
			summary=summary,
			output_format=output_format,
			max_bp=max_bp,
			db=db,
			step_id=step_id,
			step_seq=step_seq,
			rettype=rettype,
			query_type=query_type,
			by_id=by_id,
			taxonomy=taxonomy,
			taxonomy_only=taxonomy_only,
			mail=mail,
		)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	data = data[0]

	if taxonomy:
		assert "taxonomy" in data, "taxonomy is not in data"
		assert len(data["taxonomy"]) == 23, "The length of taxonomy is not 23"

		data = data["taxonomy"][0]
		assert "TaxId" in data, "TaxId is not in data"
		assert data["TaxId"] == "131567", "TaxId is not 131567"
		assert "ScientificName" in data, "ScientificName is not in data"
		assert data["ScientificName"] == 'cellular organisms', "ScientificName is not cellular organisms"
		assert "Rank" in data, "Rank is not in data"
		assert data["Rank"] == 'no rank', "Rank is not no rank"

	if taxonomy is False and taxonomy_only:

		assert len(data) == 23, "The length of taxonomy is not 23"

		data = data[0]
		assert len(data) == 3, "The length of taxonomy is not 3"

		assert "TaxId" in data, "TaxId is not in data"
		assert data["TaxId"] == "131567", "TaxId is not 131567"
		assert "ScientificName" in data, "ScientificName is not in data"
		assert data["ScientificName"] == 'cellular organisms', "ScientificName is not cellular organisms"
		assert "Rank" in data, "Rank is not in data"
		assert data["Rank"] == 'no rank', "Rank is not no rank"
