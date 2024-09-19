import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import COL

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()


def col_query(syn):
	# Use a real search query. Replace this with a valid taxon name.
	query = ["Bufo roseus"]

	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([COL(bulk=True, check_syn=syn)])
	bdp.start(query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
	dir_module = os.listdir(f"{dynamic_path}/downloads/{dir_date}")[0]
	file_list = os.listdir(f"{dynamic_path}/downloads/{dir_date}/{dir_module}")[0]

	# Open file
	file = os.path.join(f"{dynamic_path}/downloads/{dir_date}/{dir_module}/{file_list}")
	with open(file, "r") as f:
		data = json.load(f)

	return data


def test_col_initialization():
	# Test default initialization
	col = COL()

	assert col.output_format == "json"

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match="Invalid output_format. Expected 'json'."):
		COL(output_format="xml")


# Add query in pytest.mark.parametrize. We can create a different query for accepted and synonym taxa.
@pytest.mark.parametrize(
	"syn, expected_id",
	[
		(True, False),  # True: syn=True, Expected: 'NPDX' not in id.
		(False, True),  # False: syn=False, Expected: 'NPDX' in id.
	],
)
def test_download_syn(syn, expected_id):
	with redirect_stdout(trap):
		data = col_query(syn=syn)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check the main structure of the JSON file
	assert "origin_taxon" in data[0], "origin_taxon is not in data"
	assert "taxon_id" in data[0], "taxon_id is not in data"
	assert "status" in data[0], "status is not in data"
	assert "usage" in data[0], "usage is not in data"
	assert "classification" in data[0], "classification is not in data"

	classification = data[0].get("classification")
	id = [item["id"] for item in classification]

	if expected_id:
		assert "NPDX" in id, "NPDX is not in id"
	else:
		assert "NPDX" not in id, "NPDX is in id"
