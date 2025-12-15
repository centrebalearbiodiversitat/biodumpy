import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import COL

from dotenv import load_dotenv

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()
load_dotenv()

# Remember to check the latest dataset_key
def col_query(query, check_syn, dataset_key, dir_module="COL"):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([COL(bulk=True, check_syn=check_syn, dataset_key=dataset_key)])
	bdp.start(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
	file_list = os.listdir(f"{dynamic_path}/downloads/{dir_date}/{dir_module}")[0]

	# Open file
	file = os.path.join(f"{dynamic_path}/downloads/{dir_date}/{dir_module}/{file_list}")
	with open(file, "r") as f:
		data = json.load(f)

	return data


def test_col_initialization():
	# Test default initialization
	col = COL(dataset_key=os.getenv('COL_KEY'))

	assert col.output_format == "json"
	assert col.sleep == 3

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match="Invalid output_format. Expected 'json'."):
		COL(output_format="xml")

	with pytest.raises(ValueError, match="Please provide a valid dataset_key, or visit https://www.catalogueoflife.org/data/changelog to use the latest ChecklistBank."):
		COL(dataset_key=None)



# ⚠️ Remember to check the ChecklistBank fo COL
@pytest.mark.parametrize("query, check_syn, dataset_key", [(["Bufo roseus"], True, os.getenv('COL_KEY')), (["Bufo roseus"], False, os.getenv('COL_KEY'))])
def test_download(query, check_syn, dataset_key):
	with redirect_stdout(trap):
		data = col_query(query=query, check_syn=check_syn, dataset_key=dataset_key)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check the main structure of the JSON file
	data = data[0]

	assert "origin_taxon" in data, "origin_taxon is not in data"
	assert "taxon_id" in data, "taxon_id is not in data"
	assert "status" in data, "status is not in data"
	assert "usage" in data, "usage is not in data"
	assert "classification" in data, "classification is not in data"

