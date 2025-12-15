import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import WORMS

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()


def worms_query(query, distribution, marine_only, dir_module="WORMS"):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([WORMS(bulk=True, distribution=distribution, marine_only=marine_only)])
	bdp.start(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
	file_list = os.listdir(f"{dynamic_path}/downloads/{dir_date}/{dir_module}")[0]

	# Open file
	file = os.path.join(f"{dynamic_path}/downloads/{dir_date}/{dir_module}/{file_list}")
	with open(file, "r") as f:
		data = json.load(f)

	return data


def test_worms_initialization():
	# Test default initialization
	worms = WORMS()

	assert worms.output_format == "json"
	assert worms.sleep == 3

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match="Invalid output_format. Expected 'json'."):
		WORMS(output_format="xml")


# Add query in pytest.mark.parametrize. We can create a different query for accepted and synonym taxa.
@pytest.mark.parametrize("query, distribution, marine_only", [(["Pinna nobilis"], False, False), (["Pinna nobilis"], True, True)])
def test_download_syn(query, distribution, marine_only):
	with redirect_stdout(trap):
		data = worms_query(query=query, marine_only=marine_only, distribution=distribution)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check nomenclature information
	data = data[0]

	assert "AphiaID" in data, "AphiaID is not in data"
	assert "url" in data, "url is not in data"
	assert "scientificname" in data, "scientificname is not in data"
	assert "authority" in data, "authority is not in data"
	assert "status" in data, "status is not in data"
	assert "taxonRankID" in data, "taxonRankID is not in data"

	if distribution:
		assert "distribution" in data, "distribution is not in data"

		dist = data["distribution"][0]
		assert "locality" in dist, "locality is not in dist"
		assert "locationID" in dist, "locationID is not in dist"
		assert "decimalLatitude" in dist, "decimalLatitude is not in dist"
		assert "decimalLongitude" in dist, "decimalLongitude is not in dist"
