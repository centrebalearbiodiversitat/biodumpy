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


def worms_query(query, distribution, marine_only):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([WORMS(bulk=True, distribution=distribution, marine_only=marine_only)])
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


def test_worms_initialization():
	# Test default initialization
	worms = WORMS()

	assert worms.output_format == "json"

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
	assert data["AphiaID"] == 140780, "AphiaID is 140780 - Correct for Pinna nobilis"
	assert "valid_AphiaID" in data, "valid_AphiaID is not in data"
	assert data["valid_AphiaID"] == 140780, "valid_AphiaID is 140780 - Correct for Pinna nobilis"

	assert "scientificname" in data, "scientificname is not in data"
	assert data["scientificname"] == "Pinna nobilis", "scientificname is Pinna nobilis - Correct for Pinna nobilis"
	assert "valid_name" in data, "valid_name is not in data"
	assert data["valid_name"] == "Pinna nobilis", "valid_name is Pinna nobilis - Correct for Pinna nobilis"

	assert "authority" in data, "authority is not in data"
	assert data["authority"] == "Linnaeus, 1758", "authority is Linnaeus, 1758 - Correct for Pinna nobilis"
	assert "valid_authority" in data, "valid_authority is not in data"
	assert data["valid_authority"] == "Linnaeus, 1758", "valid_authority is Linnaeus, 1758 - Correct for Pinna nobilis"

	assert "rank" in data, "rank is not in data"
	assert data["rank"] == "Species", "authority is Species - Correct for Pinna nobilis"

	assert "kingdom" in data, "kingdom is not in data"
	assert data["kingdom"] == "Animalia", "kingdom is Animalia - Correct for Pinna nobilis"
	assert "phylum" in data, "phylum is not in data"
	assert data["phylum"] == "Mollusca", "phylum is Mollusca - Correct for Pinna nobilis"
	assert "class" in data, "class is not in data"
	assert data["class"] == "Bivalvia", "class is Bivalvia - Correct for Pinna nobilis"
	assert "order" in data, "order is not in data"
	assert data["order"] == "Ostreida", "class is Ostreida - Correct for Pinna nobilis"
	assert "family" in data, "family is not in data"
	assert data["family"] == "Pinnidae", "family is Pinnidae - Correct for Pinna nobilis"
	assert "genus" in data, "genus is not in data"
	assert data["genus"] == "Pinna", "genus is Pinna - Correct for Pinna nobilis"

	if distribution:
		assert "distribution" in data, "distribution is not in data"

		assert len(data["distribution"]) == 31, "length of distribution is not 31"

		dist = data["distribution"][0]

		assert "locality" in dist, "locality is not in data"
		assert dist["locality"] == "European waters (ERMS scope)", "locality is European waters (ERMS scope) - The first distribution"
		assert "locationID" in dist, "locationID is not in data"
		assert dist["locationID"] == "http://marineregions.org/mrgid/7130", "locationID is http://marineregions.org/mrgid/7130 - The first distribution"
		assert "higherGeography" in dist, "higherGeography is not in data"
		assert dist["higherGeography"] == "North Atlantic Ocean", "higherGeography is North Atlantic Ocean - The first distribution"
		assert "recordStatus" in dist, "recordStatus is not in data"
		assert dist["recordStatus"] == "valid", "recordStatus is valid - The first distribution"
		assert "decimalLatitude" in dist, "decimalLatitude is not in data"
		assert dist["decimalLatitude"] is None, "decimalLatitude is None - The first distribution"
		assert "decimalLongitude" in dist, "decimalLongitude is not in data"
		assert dist["decimalLongitude"] is None, "decimalLongitude is None - The first distribution"
