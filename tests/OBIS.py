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


def obis_query(query, occ, geometry, areaid, dir_module="OBIS"):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([OBIS(output_format="json", bulk=True, occ=occ, geometry=geometry, areaid=areaid)])
	bdp.start(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
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
	assert obis.occ == False
	assert obis.geometry is None
	assert obis.areaid is None
	assert obis.bulk == False
	assert obis.output_format == "json"
	assert obis.sleep == 3

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match='Invalid output_format. Expected "json".'):
		OBIS(output_format="xml")

	with pytest.raises(ValueError, match='"If "occ" is False, "areaid" and "geometry" cannot be set."'):
		OBIS(occ=False, areaid=33322, geometry="abc")


@pytest.mark.parametrize(
	"query, occ, geometry, areaid",
	[
		(["Pinna nobilis"], False, None, None),
		(["Pinna nobilis"], True, "POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))", None),
		(["Pinna nobilis"], True, None, 33322),
		(["Pinna nobilis"], True, "POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))", 33322),
	],
)
def test_download(query, occ, geometry, areaid):
	with redirect_stdout(trap):
		data = obis_query(query=query, occ=occ, geometry=geometry, areaid=areaid)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check the main info in an OBIS JSON file

	data = data[0]
	if occ is False:
		assert "scientificName" in data, "scientificName is not in data"
		assert "scientificNameAuthorship" in data, "scientificNameAuthorship is not in data"
		assert "taxonID" in data, "taxonID is not in data"
		assert "taxonRank" in data, "taxonRank is not in data"
		assert "taxonomicStatus" in data, "taxonomicStatus is not in data"
	else:
		assert "basisOfRecord" in data, "basisOfRecord is not in data"
		assert "catalogNumber" in data, "catalogNumber is not in data"
		assert "collectionCode" in data, "collectionCode is not in data"
		assert "country" in data, "country is not in data"
		assert "datasetID" in data, "datasetID is not in data"
		assert "datasetName" in data, "datasetName is not in data"
		assert "decimalLatitude" in data, "decimalLatitude is not in data"
		assert "decimalLongitude" in data, "decimalLongitude is not in data"
