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


def crossref_query(query, summary, dir_module="Crossref"):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([Crossref(bulk=True, summary=summary)])
	bdp.start(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
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
	assert crossref.sleep == 3

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


	if summary:
		assert "publisher" in data, "publisher is not in data"
		assert "DOI" in data, "DOI is not in data"
		assert "type" in data, "type is not in data"
		assert "title" in data, "title is not in data"
