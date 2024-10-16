import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import INaturalist

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()


def inat_query(query, output_format):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([INaturalist(bulk=True, output_format=output_format)])
	bdp.start(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
	dir_module = os.listdir(f"{dynamic_path}/downloads/{dir_date}")[0]
	file_list = os.listdir(f"{dynamic_path}/downloads/{dir_date}/{dir_module}")[0]

	file = os.path.join(f"{dynamic_path}/downloads/{dir_date}/{dir_module}/{file_list}")
	with open(file, "r") as f:
		data = json.load(f)

	return data


def test_inat_initialization():
	# Test default initialization
	bold = INaturalist()

	# Verify default parameters
	assert bold.bulk == False
	assert bold.output_format == "json"

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match='Invalid output_format. Expected "json".'):
		INaturalist(output_format="xml")


@pytest.mark.parametrize(
	"query, output_format",
	[
		(["Alytes muletensis"], "json"),
	]
)
def test_download(query, output_format):
	with redirect_stdout(trap):
		data = inat_query(query=query, output_format=output_format)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	assert "taxon" in data[0], "taxon is not in data"
	assert "image_id" in data[0], "image_id is not in data"
	assert "license_code" in data[0], "license_code is not in data"
	assert "attribution" in data[0], "attribution is not in data"
