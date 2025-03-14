import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import OBIS

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()


def obis_query(query, occurrences, geometry, areaid):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([OBIS(output_format="json", bulk=False, occurrences=occurrences, geometry=geometry, areaid=areaid)])
	bdp.download_data(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
	dir_module = os.listdir(f"{dynamic_path}/downloads/{dir_date}")[0]
	file_list = os.listdir(f"{dynamic_path}/downloads/{dir_date}/{dir_module}")[0]

	# Open file
	file = os.path.join(f"{dynamic_path}/downloads/{dir_date}/{dir_module}/{file_list}")
	with open(file, "r") as f:
		data = json.load(f)

	return data


def test_obis_initialization():
	# Test default initialization
	obis = OBIS()

	# Verify default parameters
	assert obis.occurrences == False
	assert obis.geometry is None
	assert obis.areaid is None
	assert obis.bulk == False
	assert obis.output_format == "json"

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match='Invalid output_format. Expected "json".'):
		OBIS(output_format="xml")

	with pytest.raises(ValueError, match='"If "occurrences" is False, "areaid" and "geometry" cannot be set."'):
		OBIS(occurrences=False, areaid=33322, geometry="abc")


@pytest.mark.parametrize(
	"query, occurrences, geometry, areaid",
	[
		(["Pinna nobilis"], False, None, None),
		(["Pinna nobilis"], True, "POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))", None),
		(["Pinna nobilis"], True, None, 33322),
		(["Pinna nobilis"], True, "POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))", 33322),
	],
)
def test_download(query, occurrences, geometry, areaid):
	with redirect_stdout(trap):
		data = obis_query(query=query, occurrences=occurrences, geometry=geometry, areaid=areaid)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check the main info in an OBIS JSON file
	if occurrences is False:
		assert "taxonID" in data[0], "taxonID is not in data"
		assert "scientificName" in data[0], "scientificName is not in data"
	else:
		assert "id" in data[0], "id is not in data"
		assert "scientificName" in data[0], "scientificName is not in data"
		assert "year" in data[0], "year is not in data"
		assert "month" in data[0], "month is not in data"
		assert "day" in data[0], "day is not in data"
