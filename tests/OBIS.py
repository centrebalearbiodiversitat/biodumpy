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


def obis_query(query, occ, geometry, areaid):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([OBIS(output_format="json", bulk=True, occ=occ, geometry=geometry, areaid=areaid)])
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


def test_obis_initialization():
	# Test default initialization
	obis = OBIS()

	# Verify default parameters
	assert obis.occ == False
	assert obis.geometry is None
	assert obis.areaid is None
	assert obis.bulk == False
	assert obis.output_format == "json"

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
		assert data["scientificName"] == "Pinna nobilis", "scientificName is not Pinna nobilis"
		assert "scientificNameAuthorship" in data, "scientificNameAuthorship is not in data"
		assert data["scientificNameAuthorship"] == "Linnaeus, 1758", "scientificNameAuthorship is not Linnaeus, 1758"
		assert "taxonID" in data, "taxonID is not in data"
		assert data["taxonID"] == 140780, "taxonID is not 140780"
		assert "bold_id" in data, "bold_id is not in data"
		assert data["bold_id"] == 79749, "bold_id is not 79749"
		assert "ncbi_id" in data, "ncbi_id is not in data"
		assert data["ncbi_id"] == 111169, "ncbi_id is not 111169"
		assert "taxonRank" in data, "taxonRank is not in data"
		assert data["taxonRank"] == "Species", "taxonRank is not Species"
		assert "taxonomicStatus" in data, "taxonomicStatus is not in data"
		assert data["taxonomicStatus"] == "accepted", "taxonomicStatus is not accepted"
		assert "acceptedNameUsage" in data, "acceptedNameUsage is not in data"
		assert data["acceptedNameUsage"] == "Pinna nobilis", "acceptedNameUsage is not Pinna nobilis"
		assert "acceptedNameUsageID" in data, "acceptedNameUsageID is not in data"
		assert data["acceptedNameUsageID"] == 140780, "acceptedNameUsageID is not 140780"
		assert "is_marine" in data, "is_marine is not in data"
		assert data["is_marine"] is True, "is_marine is not True"
		assert "is_brackish" in data, "is_brackish is not in data"
		assert data["is_brackish"] is False, "is_brackish is not False"
		assert "is_freshwater" in data, "is_freshwater is not in data"
		assert data["is_freshwater"] is False, "is_freshwater is not False"
		assert "is_terrestrial" in data, "is_terrestrial is not in data"
		assert data["is_terrestrial"] is False, "is_terrestrial is not False"
		assert "kingdom" in data, "kingdom is not in data"
		assert data["kingdom"] == "Animalia", "kingdom is not Animalia"
		assert "phylum" in data, "phylum is not in data"
		assert data["phylum"] == "Mollusca", "phylum is not Mollusca"
		assert "class" in data, "class is not in data"
		assert data["class"] == "Bivalvia", "class is not Bivalvia"
		assert "subclass" in data, "subclass is not in data"
		assert data["subclass"] == "Autobranchia", "subclass is not Autobranchia"
		assert "infraclass" in data, "infraclass is not in data"
		assert data["infraclass"] == "Pteriomorphia", "infraclass is not Pteriomorphia"
		assert "order" in data, "order is not in data"
		assert data["order"] == "Ostreida", "order is not Ostreida"
		assert "superfamily" in data, "superfamily is not in data"
		assert data["superfamily"] == "Pinnoidea", "superfamily is not Pinnoidea"
		assert "family" in data, "family is not in data"
		assert data["family"] == "Pinnidae", "family is not Pinnidae"
		assert "genus" in data, "genus is not in data"
		assert data["genus"] == "Pinna", "genus is not Pinna"
		assert "species" in data, "species is not in data"
		assert data["species"] == "Pinna nobilis", "species is not Pinna nobilis"
		assert "kingdomid" in data, "kingdomid is not in data"
		assert data["kingdomid"] == 2, "kingdomid is not 2"
		assert "phylumid" in data, "phylumid is not in data"
		assert data["phylumid"] == 51, "phylumid is not 51"
		assert "classid" in data, "classid is not in data"
		assert data["classid"] == 105, "classid is not 105"
		assert "subclassid" in data, "subclassid is not in data"
		assert data["subclassid"] == 1424948, "subclassid is not 1424948"
		assert "infraclassid" in data, "infraclassid is not in data"
		assert data["infraclassid"] == 206, "infraclassid is not 206"
		assert "orderid" in data, "orderid is not in data"
		assert data["orderid"] == 1774, "orderid is not 1774"
		assert "superfamilyid" in data, "superfamilyid is not in data"
		assert data["superfamilyid"] == 382250, "superfamilyid is not 382250"
		assert "familyid" in data, "familyid is not in data"
		assert data["familyid"] == 1776, "familyid is not 1776"
		assert "genusid" in data, "genusid is not in data"
		assert data["genusid"] == 138352, "genusid is not 138352"
		assert "speciesid" in data, "speciesid is not in data"
		assert data["speciesid"] == 140780, "speciesid is not 140780"
		assert "category" in data, "category is not in data"
		assert data["category"] == "CR", "category is not CR"
	else:
		assert "basisOfRecord" in data, "basisOfRecord is not in data"
		assert "catalogNumber" in data, "catalogNumber is not in data"
		assert "collectionCode" in data, "collectionCode is not in data"
		assert "country" in data, "country is not in data"
		assert "datasetID" in data, "datasetID is not in data"
		assert "datasetName" in data, "datasetName is not in data"
		assert "day" in data, "day is not in data"
		assert "decimalLatitude" in data, "decimalLatitude is not in data"
		assert "decimalLongitude" in data, "decimalLongitude is not in data"
		assert "eventDate" in data, "eventDate is not in data"
		assert "eventID" in data, "eventID is not in data"
		assert "footprintSRS" in data, "footprintSRS is not in data"
		assert "identifiedBy" in data, "identifiedBy is not in data"
		assert "language" in data, "language is not in data"
		assert "maximumDepthInMeters" in data, "maximumDepthInMeters is not in data"
		assert "minimumDepthInMeters" in data, "minimumDepthInMeters is not in data"
		assert "modified" in data, "modified is not in data"
		assert "month" in data, "month is not in data"
		assert "occurrenceID" in data, "occurrenceID is not in data"
		assert "occurrenceRemarks" in data, "occurrenceRemarks is not in data"
		assert "occurrenceStatus" in data, "occurrenceStatus is not in data"
		assert "scientificName" in data, "scientificName is not in data"
		assert "scientificNameID" in data, "scientificNameID is not in data"
		assert "stateProvince" in data, "stateProvince is not in data"
		assert "year" in data, "year is not in data"
		assert "id" in data, "id is not in data"
		assert "dataset_id" in data, "dataset_id is not in data"
		assert "node_id" in data, "node_id is not in data"
		assert "depth" in data, "depth is not in data"
		assert "date_start" in data, "date_start is not in data"
		assert "date_mid" in data, "date_mid is not in data"
		assert "date_end" in data, "date_end is not in data"
		assert "date_year" in data, "date_year is not in data"
		assert "dropped" in data, "dropped is not in data"
		assert "absence" in data, "absence is not in data"
		assert "marine" in data, "marine is not in data"
		assert "brackish" in data, "brackish is not in data"
		assert "superdomain" in data, "superdomain is not in data"
		assert "kingdom" in data, "kingdom is not in data"
		assert "phylum" in data, "phylum is not in data"
		assert "class" in data, "class is not in data"
		assert "subclass" in data, "subclass is not in data"
		assert "infraclass" in data, "infraclass is not in data"
		assert "order" in data, "order is not in data"
		assert "superfamily" in data, "superfamily is not in data"
		assert "family" in data, "family is not in data"
		assert "genus" in data, "genus is not in data"
		assert "species" in data, "species is not in data"
		assert "superdomainid" in data, "superdomainid is not in data"
		assert "kingdomid" in data, "kingdomid is not in data"
		assert "phylumid" in data, "phylumid is not in data"
		assert "classid" in data, "classid is not in data"
		assert "subclassid" in data, "subclassid is not in data"
		assert "infraclassid" in data, "infraclassid is not in data"
		assert "orderid" in data, "orderid is not in data"
		assert "superfamilyid" in data, "superfamilyid is not in data"
		assert "familyid" in data, "familyid is not in data"
		assert "genusid" in data, "genusid is not in data"
		assert "speciesid" in data, "speciesid is not in data"
		assert "aphiaID" in data, "aphiaID is not in data"
		assert "originalScientificName" in data, "originalScientificName is not in data"
		assert "category" in data, "category is not in data"
		assert "flags" in data, "flags is not in data"
		assert "bathymetry" in data, "bathymetry is not in data"
		assert "shoredistance" in data, "shoredistance is not in data"
		assert "sst" in data, "sst is not in data"
		assert "sss" in data, "sss is not in data"
