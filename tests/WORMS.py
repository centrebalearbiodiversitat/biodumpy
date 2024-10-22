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
@pytest.mark.parametrize(
	"query, distribution, marine_only",
	[
		(["Pinna nobilis"], False, False),
		(["Pinna nobilis"], True, True)
	]
)
def test_download_syn(query, distribution, marine_only):
	with redirect_stdout(trap):
		data = worms_query(query=query, marine_only=marine_only, distribution=distribution)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check nomenclature information
	data = data[0]

	assert "AphiaID" in data, "AphiaID is not in data"
	assert data["AphiaID"] == 140780, "AphiaID is not 140780"
	assert "url" in data, "url is not in data"
	assert "scientificname" in data, "scientificname is not in data"
	assert data["scientificname"] == "Pinna nobilis", "scientificname is not Pinna nobilis"
	assert "authority" in data, "authority is not in data"
	assert data["authority"] == "Linnaeus, 1758", "authority is not Linnaeus, 1758"
	assert "status" in data, "status is not in data"
	assert data["status"] == "accepted", "status is not accepted"
	assert 'unacceptreason' in data, "unacceptreason is not in data"
	assert 'taxonRankID' in data, "taxonRankID is not in data"
	assert data["taxonRankID"] == 220, "taxonRankID is not accepted"
	assert "rank" in data, "rank is not in data"
	assert data["rank"] == "Species", "authority is not Species"
	assert "valid_AphiaID" in data, "valid_AphiaID is not in data"
	assert data["valid_AphiaID"] == 140780, "valid_AphiaID is not 140780"
	assert "valid_name" in data, "valid_name is not in data"
	assert data["valid_name"] == "Pinna nobilis", "valid_name is not Pinna nobilis"
	assert "valid_authority" in data, "valid_authority is not in data"
	assert data["valid_authority"] == "Linnaeus, 1758", "valid_authority is not Linnaeus, 1758"
	assert 'parentNameUsageID' in data, "parentNameUsageID is not in data"
	assert data["parentNameUsageID"] == 138352, "parentNameUsageID is not 138352"
	assert "kingdom" in data, "kingdom is not in data"
	assert data["kingdom"] == "Animalia", "kingdom is not Animalia"
	assert "phylum" in data, "phylum is not in data"
	assert data["phylum"] == "Mollusca", "phylum is not Mollusca"
	assert "class" in data, "class is not in data"
	assert data["class"] == "Bivalvia", "class is not Bivalvia"
	assert "order" in data, "order is not in data"
	assert data["order"] == "Ostreida", "class is not Ostreida"
	assert "family" in data, "family is not in data"
	assert data["family"] == "Pinnidae", "family is not Pinnidae"
	assert "genus" in data, "genus is not in data"
	assert data["genus"] == "Pinna", "genus is not Pinna"
	assert "citation" in data, "citation is not in data"
	assert 'lsid' in data, "lsid is not in data"
	assert "isMarine" in data, "isMarine is not in data"
	assert data["isMarine"] == 1, "isMarine is not 1"
	assert "isBrackish" in data, "isBrackish is not in data"
	assert data["isBrackish"] == 0, "isBrackish is not 0"
	assert "isFreshwater" in data, "isFreshwater is not in data"
	assert data["isFreshwater"] == 0, "isFreshwater is not 0"
	assert "isTerrestrial" in data, "isTerrestrial is not in data"
	assert data["isTerrestrial"] == 0, "isTerrestrial is 0"
	assert "isExtinct" in data, "isExtinct is not in data"
	assert data["isExtinct"] is None, "isExtinct is not None"
	assert 'match_type' in data, "match_type is not in data"
	assert data["match_type"] == "exact", "match_type is not exact"
	assert 'modified' in data, "modified is not in data"

	if distribution:
		assert "distribution" in data, "distribution is not in data"

		assert len(data["distribution"]) == 31, "length of distribution is not 31"

		dist = data["distribution"][0]

		assert "locality" in dist, "locality is not in dist"
		assert dist["locality"] == "European waters (ERMS scope)", "locality is European waters (ERMS scope)"
		assert "locationID" in dist, "locationID is not in dist"
		assert (dist["locationID"] == "http://marineregions.org/mrgid/7130"), "locationID is http://marineregions.org/mrgid/7130"
		assert "higherGeography" in dist, "higherGeography is not in dist"
		assert dist["higherGeography"] == "North Atlantic Ocean", "higherGeography is not North Atlantic Ocean"
		assert "higherGeographyID" in dist, "higherGeographyID is not in dist"
		assert dist["higherGeographyID"] == "http://marineregions.org/mrgid/1912", "higherGeography is not http://marineregions.org/mrgid/1912"
		assert "recordStatus" in dist, "recordStatus is not in dist"
		assert dist["recordStatus"] == "valid", "recordStatus is not 'valid'"
		assert "typeStatus" in dist, "typeStatus is not in dist"
		assert "establishmentMeans" in dist, "establishmentMeans is not in dist"
		assert "invasiveness" in dist, "invasiveness is not in dist"
		assert "occurrence" in dist, "occurrence is not in dist"
		assert "decimalLatitude" in dist, "decimalLatitude is not in dist"
		assert dist["decimalLatitude"] is None, "decimalLatitude is not None"
		assert "decimalLongitude" in dist, "decimalLongitude is not in dist"
		assert dist["decimalLongitude"] is None, "decimalLongitude is not None"
		assert "qualityStatus" in dist, "qualityStatus is not in dist"
