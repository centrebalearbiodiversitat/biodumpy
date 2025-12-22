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


def gbif_query(query, accepted_only, occ, geometry, dataset_key, dir_module="GBIF"):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([GBIF(dataset_key=dataset_key, limit=20, accepted_only=accepted_only, occ=occ, geometry=geometry, output_format="json", bulk=True)])
	bdp.start(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
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
	assert gbif.dataset_key == os.getenv("GBIF_DATASET_KEY")
	assert gbif.limit == 20
	assert gbif.accepted == True
	assert gbif.occ == False
	assert gbif.geometry is None
	assert gbif.bulk == False
	assert gbif.output_format == "json"
	assert gbif.sleep == 3

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match='Invalid output_format. Expected "json".'):
		GBIF(output_format="xml")


@pytest.mark.parametrize(
	"query, accepted_only, occ, geometry",
	[(["Alytes muletensis"], True, False, None), (["Alytes muletensis"], True, True, "POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))")],
)
def test_download(query, accepted_only, occ, geometry):
	with redirect_stdout(trap):
		data = gbif_query(query=query, accepted_only=accepted_only, occ=occ, geometry=geometry, dataset_key=os.getenv("GBIF_DATASET_KEY"))

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check the main info in a GBIF JSON file
	data = data[0]
	if occ is False:
		assert "key" in data, "key is not in data"
		assert "nameKey" in data, "nameKey is not in data"
		assert "datasetKey" in data, "datasetKey is not in data"
		assert "constituentKey" in data, "constituentKey is not in data"
	else:
		assert "key" in data, "key is not in data"
		assert "datasetKey" in data, "datasetKey is not in data"
		assert "publishingOrgKey" in data, "publishingOrgKey is not in data"
		assert "installationKey" in data, "installationKey is not in data"
		assert "hostingOrganizationKey" in data, "hostingOrganizationKey is not in data"
		assert "decimalLatitude" in data, "decimalLatitude is not in data"
		assert "decimalLongitude" in data, "decimalLongitude is not in data"
