import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import GBIF

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()

gbif_backbone = "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"


def gbif_query(query, accepted_only, occ, geometry):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy(
		[
			GBIF(
				output_format="json",
				dataset_key=gbif_backbone,
				limit=20,
				bulk=False,
				accepted_only=accepted_only,
				occ=occ,
				geometry=geometry,
			)
		]
	)
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


def test_gbif_initialization():
	# Test default initialization
	gbif = GBIF()

	# Verify default parameters
	assert gbif.dataset_key == "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
	assert gbif.limit == 20
	assert gbif.accepted == True
	assert gbif.occ == False
	assert gbif.geometry is None
	assert gbif.bulk == False
	assert gbif.output_format == "json"

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# accepted_only parameter.
	with pytest.raises(ValueError, match="Invalid accepted_only. Expected True."):
		GBIF(occ=True, accepted_only=False)

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match='Invalid output_format. Expected "json".'):
		GBIF(output_format="xml")


@pytest.mark.parametrize(
	"query, accepted_only, occ, geometry",
	[
		(["Alytes muletensis (Sanchíz & Adrover, 1979)"], True, False, None),
		(
			["Alytes muletensis (Sanchíz & Adrover, 1979)"],
			True,
			True,
			"POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))",
		),
	],
)
def test_download(query, accepted_only, occ, geometry):
	with redirect_stdout(trap):
		data = gbif_query(query=query, accepted_only=accepted_only, occ=occ, geometry=geometry)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check the main info in a GBIF JSON file
	if occ is False:
		assert "key" in data[0], "key is not in data"
		assert "scientificName" in data[0], "scientificName is not in data"
	else:
		assert "key" in data[0], "key is not in data"
		assert "scientificName" in data[0], "scientificName is not in data"
		assert "gadm" in data[0], "gadm is not in data"
		assert "year" in data[0], "year is not in data"
		assert "month" in data[0], "month is not in data"
		assert "day" in data[0], "day is not in data"
