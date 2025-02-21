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


def inat_query(query):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([INaturalist(bulk=True)])
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


@pytest.mark.parametrize("query", [(["Alytes muletensis"])])
def test_download(query):
	with redirect_stdout(trap):
		data = inat_query(query=query)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	data = data[0]

	assert "taxon" in data, "taxon is not in data"
	assert data["taxon"] == "Alytes muletensis", "taxon is not Alytes muletensis"
	assert "image_id" in data, "image_id is not in data"
	assert data["image_id"] == "61080851/medium.jpeg", "image_id is not 61080851/medium.jpeg"
	assert "license_code" in data, "license_code is not in data"
	assert data["license_code"] == "cc-by-nc", "image_id is not cc-by-nc"
	assert "attribution" in data, "attribution is not in data"
	assert data["attribution"] == "(c) Gert Jan Verspui, some rights reserved (CC BY-NC), uploaded by Gert Jan Verspui", (
		"attribution is not (c) Gert Jan Verspui, some rights reserved (CC BY-NC), uploaded by Gert Jan Verspui"
	)
