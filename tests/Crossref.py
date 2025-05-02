import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import Crossref

# set a trap and redirect stdout. Remove print of function. In this wat test output is cleanest.
trap = io.StringIO()


def crossref_query(query, summary):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([Crossref(bulk=True, summary=summary)])
	bdp.start(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
	dir_module = os.listdir(f"{dynamic_path}/downloads/{dir_date}")[0]
	file_list = os.listdir(f"{dynamic_path}/downloads/{dir_date}/{dir_module}")[0]

	# Open file
	file = os.path.join(f"{dynamic_path}/downloads/{dir_date}/{dir_module}/{file_list}")
	with open(file, "r") as f:
		data = json.load(f)

	return data


def test_crossref_initialization():
	# Test default initialization
	crossref = Crossref()

	# Objective: Verify that when a Crossref object is created without passing any arguments, it initializes with the
	# correct default values.
	assert crossref.summary == False
	assert crossref.output_format == "json"

	# Objective: Verify that class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match="Invalid output_format. Expected 'json'."):
		Crossref(output_format="xml")


@pytest.mark.parametrize("query, summary", [(["10.1038/s44185-022-00001-3"], False), (["10.1038/s44185-022-00001-3"], True)])
def test_download(query, summary):
	with redirect_stdout(trap):
		data = crossref_query(query=query, summary=summary)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check the main structure of the JSON file
	data = data[0]

	print(data)

	if summary:
		assert "publisher" in data, "publisher is not in data"
		assert data["publisher"] == "Springer Science and Business Media LLC", "publisher is not Springer Science and Business Media LLC"
		assert "container-title" in data, "container-title is not in data"
		assert data["container-title"] == "npj Biodiversity", "container-title is not npj Biodiversity"
		assert "DOI" in data, "DOI is not in data"
		assert data["DOI"] == "10.1038/s44185-022-00001-3", "DOI is not 10.1038/s44185-022-00001-3"
		assert "type" in data, "type is not in data"
		assert data["type"] == "journal-article", "type is not journal-article"
		assert "language" in data, "language is not in data"
		assert data["language"] == "en", "language is not en"
		assert "URL" in data, "URL is not in data"
		# assert data["URL"] == "http://dx.doi.org/10.1038/s44185-022-00001-3", "URL is not http://dx.doi.org/10.1038/s44185-022-00001-3"
		assert "published" in data, "published is not in data"
		assert "title" in data, "title is not in data"
		assert data["title"] == "Climate change will redefine taxonomic, functional, and phylogenetic diversity of Odonata in space and time", (
			"title is not Climate change will redefine taxonomic, functional, and phylogenetic diversity of Odonata in space and time"
		)
		assert "title" in data, "title is not in data"
		assert "author" in data, "author is not in data"
		assert "abstract" in data, "abstract is not in data"
	else:
		assert "indexed" in data, "indexed is not in data"
		assert "reference-count" in data, "reference-count is not in data"
		assert data["reference-count"] == 132, "reference-count is not 132"
		assert "publisher" in data, "publisher is not in data"
		# assert data["publisher"] == "Springer Science and Business Media LLC", "publisher is not Springer Science and Business Media LLC"
		assert "issue" in data, "issue is not in data"
		assert "license" in data, "license is not in data"
		assert "content-domain" in data, "content-domain is not in data"
		assert "short-container-title" in data, "short-container-title is not in data"
		# assert data["short-container-title"][0] == "npj biodivers", "short-container-title is not npj biodivers"
		assert "abstract" in data, "abstract is not in data"
		assert "DOI" in data, "DOI is not in data"
		assert data["DOI"] == "10.1038/s44185-022-00001-3", "DOI is not 10.1038/s44185-022-00001-3"
		assert "type" in data, "type is not in data"
		assert data["type"] == "journal-article", "type is not journal-article"
		assert "created" in data, "created is not in data"
		assert "update-policy" in data, "update-policy is not in data"
		assert "source" in data, "source is not in data"
		assert "is-referenced-by-count" in data, "is-referenced-by-count is not in data"
		assert "title" in data, "title is not in data"
		assert data["title"][0] == "Climate change will redefine taxonomic, functional, and phylogenetic diversity of Odonata in space and time", (
			"title is not Climate change will redefine taxonomic, functional, and phylogenetic diversity of Odonata in space and time"
		)
		assert "prefix" in data, "prefix is not in data"
		# assert data["prefix"] == "10.1038", "prefix is not 10.1038"
		assert "volume" in data, "volume is not in data"
		assert data["volume"] == "1", "volume is not 1"
		assert "author" in data, "author is not in data"
		assert "member" in data, "member is not in data"
		assert "published-online" in data, "published-online is not in data"
		assert "reference" in data, "reference is not in data"
		assert "container-title" in data, "container-title is not in data"
		assert "original-title" in data, "original-title is not in data"
		assert "language" in data, "language is not in data"
		assert data["language"] == "en", "language is not en"
		assert "link" in data, "link is not in data"
		assert "deposited" in data, "deposited is not in data"
		assert "score" in data, "score is not in data"
		assert "resource" in data, "resource is not in data"
		assert "subtitle" in data, "subtitle is not in data"
		assert "short-title" in data, "short-title is not in data"
		assert "issued" in data, "issued is not in data"
		assert "references-count" in data, "references-count is not in data"
		assert "journal-issue" in data, "journal-issue is not in data"
		assert "alternative-id" in data, "alternative-id is not in data"
		assert "URL" in data, "URL is not in data"
		# assert data["URL"] == "http://dx.doi.org/10.1038/s44185-022-00001-3", "URL is not http://dx.doi.org/10.1038/s44185-022-00001-3"
		assert "relation" in data, "relation is not in data"
		assert "ISSN" in data, "ISSN is not in data"
		assert "issn-type" in data, "issn-type is not in data"
		assert "subject" in data, "subject is not in data"
		assert "published" in data, "published is not in data"
		assert "assertion" in data, "assertion is not in data"
		assert "article-number" in data, "article-number is not in data"
