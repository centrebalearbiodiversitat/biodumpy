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
				dataset_key=gbif_backbone,
				limit=20,
				accepted_only=accepted_only,
				occ=occ,
				geometry=geometry,
				bulk=True,
				output_format="json"
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
		(["Alytes muletensis (Sanchíz & Adrover, 1979)"], True, True,
		 "POLYGON((0.248 37.604, 6.300 37.604, 6.300 41.472, 0.248 41.472, 0.248 37.604))"),
	],
)
def test_download(query, accepted_only, occ, geometry):
	with redirect_stdout(trap):
		data = gbif_query(query=query, accepted_only=accepted_only, occ=occ, geometry=geometry)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check the main info in a GBIF JSON file
	data = data[0]
	if occ is False:
		assert "key" in data, "key is not in data"
		assert data["key"] == 2426609, "key is not 2426609"
		assert "nameKey" in data, "nameKey is not in data"
		assert data["nameKey"] == 497717, "nameKey is not 497717"
		assert "datasetKey" in data, "datasetKey is not in data"
		assert data[
			       "datasetKey"] == 'd7dddbf4-2cf0-4f39-9b2a-bb099caae36c', "datasetKey is not d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
		assert "constituentKey" in data, "constituentKey is not in data"
		assert data[
			       "constituentKey"] == '7ddf754f-d193-4cc9-b351-99906754a03b', "datasetKey is not 7ddf754f-d193-4cc9-b351-99906754a03b"
		assert "nubKey" in data, "nubKey is not in data"
		assert data["nubKey"] == 2426609, "nubKey is not 2426609"
		assert "parentKey" in data, "parentKey is not in data"
		assert data["parentKey"] == 2426608, "parentKey is not 2426608"
		assert "parent" in data, "parent is not in data"
		assert data["parent"] == "Alytes", "parent is not Alytes"
		assert "basionymKey" in data, "basionymKey is not in data"
		assert data["basionymKey"] == 4409471, "basionymKey is not 4409471"
		assert "basionym" in data, "basionym is not in data"
		assert data[
			       "basionym"] == 'Baleaphryne muletensis Sanchíz & Adrover, 1979', "basionym is not Baleaphryne muletensis Sanchíz & Adrover, 1979"
		assert "kingdom" in data, "kingdom is not in data"
		assert data["kingdom"] == 'Animalia', "kingdom is not Animalia"
		assert "phylum" in data, "phylum is not in data"
		assert data["phylum"] == 'Chordata', "phylum is not Chordata"
		assert "phylum" in data, "phylum is not in data"
		assert data["phylum"] == 'Chordata', "phylum is not Chordata"
		assert "class" in data, "class is not in data"
		assert data["class"] == 'Amphibia', "class is not Chordata"
		assert "order" in data, "order is not in data"
		assert data["order"] == 'Anura', "order is not Anura"
		assert "family" in data, "family is not in data"
		assert data["family"] == 'Alytidae', "family is not Alytidae"
		assert "genus" in data, "genus is not in data"
		assert data["genus"] == 'Alytes', "genus is not Alytes"
		assert "species" in data, "species is not in data"
		assert data["species"] == 'Alytes muletensis', "species is not Alytes muletensis"
		assert "kingdomKey" in data, "kingdomKey is not in data"
		assert data["kingdomKey"] == 1, "kingdomKey is not 1"
		assert "phylumKey" in data, "phylumKey is not in data"
		assert data["phylumKey"] == 44, "phylumKey is not 44"
		assert "classKey" in data, "classKey is not in data"
		assert data["classKey"] == 131, "classKey is not 131"
		assert "orderKey" in data, "orderKey is not in data"
		assert data["orderKey"] == 952, "orderKey is not 952"
		assert "familyKey" in data, "familyKey is not in data"
		assert data["familyKey"] == 6726, "familyKey is not 6726"
		assert "genusKey" in data, "genusKey is not in data"
		assert data["genusKey"] == 2426608, "genusKey is not 2426608"
		assert "speciesKey" in data, "speciesKey is not in data"
		assert data["speciesKey"] == 2426609, "speciesKey is not 2426609"
		assert "scientificName" in data, "scientificName is not in data"
		assert data[
			       "scientificName"] == 'Alytes muletensis (Sanchíz & Adrover, 1979)', "scientificName is not Alytes muletensis (Sanchíz & Adrover, 1979)"
		assert "canonicalName" in data, "canonicalName is not in data"
		assert data["canonicalName"] == "Alytes muletensis", "canonicalName is not Alytes muletensis"
		assert "authorship" in data, "authorship is not in data"
		assert data["authorship"] == '(Sanchíz & Adrover, 1979) ', "authorship is not (Sanchíz & Adrover, 1979)"
		assert "nameType" in data, "nameType is not in data"
		assert data["nameType"] == 'SCIENTIFIC', "nameType is not SCIENTIFIC"
		assert "taxonomicStatus" in data, "taxonomicStatus is not in data"
		assert data["taxonomicStatus"] == 'ACCEPTED', "taxonomicStatus is not ACCEPTED"
		assert "rank" in data, "rank is not in data"
		assert data["rank"] == 'SPECIES', "rank is not SPECIES"
		assert "origin" in data, "origin is not in data"
		assert data["origin"] == 'SOURCE', "origin is not SOURCE"
		assert "numDescendants" in data, "numDescendants is not in data"
		assert data["numDescendants"] == 1, "numDescendants is not 1"
		assert "numOccurrences" in data, "numOccurrences is not in data"
		assert data["numOccurrences"] == 0, "numOccurrences is not 0"
		assert "extinct" in data, "extinct is not in data"
		assert "habitats" in data, "habitats is not in data"
		assert 'nomenclaturalStatus' in data, "nomenclaturalStatus is not in data"
		assert 'threatStatuses' in data, "threatStatuses is not in data"
		assert 'descriptions' in data, "descriptions is not in data"
		assert 'vernacularNames' in data, "vernacularNames is not in data"
		assert 'higherClassificationMap' in data, "higherClassificationMap is not in data"
		assert 'synonym' in data, "synonym is not in data"
	else:
		assert "key" in data, "key is not in data"
		assert "datasetKey" in data, "datasetKey is not in data"
		assert "publishingOrgKey" in data, "publishingOrgKey is not in data"
		assert "installationKey" in data, "installationKey is not in data"
		assert "hostingOrganizationKey" in data, "hostingOrganizationKey is not in data"
		assert "publishingCountry" in data, "publishingCountry is not in data"
		assert "protocol" in data, "protocol is not in data"
		assert "lastCrawled" in data, "lastCrawled is not in data"
		assert "lastParsed" in data, "lastParsed is not in data"
		assert "crawlId" in data, "crawlId is not in data"
		assert "extensions" in data, "extensions is not in data"
		assert "basisOfRecord" in data, "basisOfRecord is not in data"
		assert "individualCount" in data, "individualCount is not in data"
		assert "occurrenceStatus" in data, "occurrenceStatus is not in data"
		assert "lifeStage" in data, "lifeStage is not in data"
		assert "taxonKey" in data, "taxonKey is not in data"
		assert "kingdomKey" in data, "kingdomKey is not in data"
		assert "phylumKey" in data, "phylumKey is not in data"
		assert "classKey" in data, "classKey is not in data"
		assert "orderKey" in data, "orderKey is not in data"
		assert "familyKey" in data, "familyKey is not in data"
		assert "genusKey" in data, "genusKey is not in data"
		assert "speciesKey" in data, "speciesKey is not in data"
		assert "acceptedTaxonKey" in data, "acceptedTaxonKey is not in data"
		assert "scientificName" in data, "scientificName is not in data"
		assert "acceptedScientificName" in data, "acceptedScientificName is not in data"
		assert "kingdom" in data, "kingdom is not in data"
		assert "phylum" in data, "phylum is not in data"
		assert "order" in data, "order is not in data"
		assert "family" in data, "family is not in data"
		assert "genus" in data, "genus is not in data"
		assert "species" in data, "species is not in data"
		assert "genericName" in data, "genericName is not in data"
		assert "specificEpithet" in data, "specificEpithet is not in data"
		assert "taxonRank" in data, "taxonRank is not in data"
		assert "taxonomicStatus" in data, "taxonomicStatus is not in data"
		assert "iucnRedListCategory" in data, "iucnRedListCategory is not in data"
		assert "decimalLatitude" in data, "decimalLatitude is not in data"
		assert "decimalLongitude" in data, "decimalLongitude is not in data"
		assert "coordinateUncertaintyInMeters" in data, "coordinateUncertaintyInMeters is not in data"
		assert "continent" in data, "continent is not in data"
		assert "stateProvince" in data, "stateProvince is not in data"
		assert "gadm" in data, "gadm is not in data"
		assert "year" in data, "year is not in data"
		assert "month" in data, "month is not in data"
		assert "day" in data, "day is not in data"
		assert "eventDate" in data, "eventDate is not in data"
		assert "startDayOfYear" in data, "startDayOfYear is not in data"
		assert "endDayOfYear" in data, "endDayOfYear is not in data"
		assert "issues" in data, "issues is not in data"
		assert "modified" in data, "modified is not in data"
		assert "lastInterpreted" in data, "lastInterpreted is not in data"
		assert "license" in data, "license is not in data"
		assert "isSequenced" in data, "isSequenced is not in data"
		assert "identifiers" in data, "identifiers is not in data"
		assert "media" in data, "media is not in data"
		assert "facts" in data, "facts is not in data"
		assert "relations" in data, "relations is not in data"
		assert "isInCluster" in data, "isInCluster is not in data"
		assert "recordedBy" in data, "recordedBy is not in data"
		assert "samplingProtocol" in data, "samplingProtocol is not in data"
		assert "geodeticDatum" in data, "geodeticDatum is not in data"
		assert "class" in data, "class is not in data"
		assert "countryCode" in data, "countryCode is not in data"
		assert "recordedByIDs" in data, "recordedByIDs is not in data"
		assert "identifiedByIDs" in data, "identifiedByIDs is not in data"
		assert "country" in data, "country is not in data"
		assert "gbifRegion" in data, "gbifRegion is not in data"
		assert "publishedByGbifRegion" in data, "publishedByGbifRegion is not in data"
		assert "rightsHolder" in data, "rightsHolder is not in data"
		assert "identifier" in data, "identifier is not in data"
		assert "vernacularName" in data, "vernacularName is not in data"
		assert "habitat" in data, "habitat is not in data"
		assert "dataGeneralizations" in data, "dataGeneralizations is not in data"
		assert "eventTime" in data, "eventTime is not in data"
		assert "locality" in data, "locality is not in data"
		assert "identificationVerificationStatus" in data, "identificationVerificationStatus is not in data"
		assert "gbifID" in data, "gbifID is not in data"
		assert "eventType" in data, "eventType is not in data"
		assert "occurrenceID" in data, "occurrenceID is not in data"
