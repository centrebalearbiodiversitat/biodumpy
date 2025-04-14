import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import IUCN

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()

# TO DO: Remove IUCN KEY
API_KEY = ""

IUCN_SCOPE = [
	"Global",
	"Europe",
	"Mediterranean",
	"Western Africa",
	"S. Africa FW",
	"Pan-Africa",
	"Central Africa",
	"Northeastern Africa",
	"Eastern Africa",
	"Northern Africa",
	"Gulf of Mexico",
	"Caribbean",
	"Persian Gulf",
	"Arabian Sea"
]

def iucn_query(query, authorization, assess_details, latest, scope, output_format):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy(
		[
			IUCN(
				authorization = authorization,
				assess_details = assess_details,
				latest = latest,
				scope = scope,
				output_format = output_format,
				bulk = True
			)
		]
	)

	bdp.start(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
	dir_module = os.listdir(f"{dynamic_path}/downloads/{dir_date}")[0]
	file_list = os.listdir(f"{dynamic_path}/downloads/{dir_date}/{dir_module}")[0]

	file = os.path.join(f"{dynamic_path}/downloads/{dir_date}/{dir_module}/{file_list}")
	if output_format == "json":
		with open(file, "r") as f:
			data = json.load(f)

	return data


def test_iucn_initialization():
	# Test default initialization
	iucn = IUCN(authorization=API_KEY)

	# Verify default parameters
	assert iucn.latest == False
	assert iucn.assess_details == False
	assert iucn.output_format == "json"

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match="Invalid output_format. Expected 'json'."):
		IUCN(output_format="csv", authorization=API_KEY)


def test_validate_regions_valid():
	# Ensures that valid regions don't raise an error.
	regions = ["Europe", "Global"]
	try:
		for region in regions:
			if region not in IUCN_SCOPE:
				raise ValueError(f"Choose an IUCN scope from the following options: {IUCN_SCOPE}.")
	except ValueError:
		pytest.fail("ValueError raised with valid regions")


def test_validate_regions_invalid():
	# Ensures that invalid regions raise a ValueError with the correct message.
	regions = ["europe", "atlantis"]  # 'atlantis' is not in IUCN_REGIONS

	with pytest.raises(ValueError) as exc_info:
		for region in regions:
			if region not in IUCN_SCOPE:
				raise ValueError(f"Choose an IUCN scope from the following options: {IUCN_SCOPE}.")

	assert "Choose an IUCN scope from the following options" in str(exc_info.value)


@pytest.mark.parametrize(
	"query, assess_details, latest, scope, output_format",
	[
		(["Alytes muletensis"], False, False, ["Global"], "json"),
		(["Alytes muletensis"], True, False, ["Global"], "json"),
		(["Alytes muletensis"], False, True, ["Global"], "json"),
		(["Bufotes viridis"], False, False, ["Global"], "json")

	],
)
def test_download(query, assess_details, latest, scope, output_format):
	with redirect_stdout(trap):
		data = iucn_query(
			query=query,
			authorization=API_KEY,
			assess_details=assess_details,
			latest=latest,
			scope=scope,
			output_format=output_format
		)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# General checks ----
	# Check some fields
	data = data[0]
	assert "taxon" in data, "taxon is not in data"
	assert "assessment" in data, "assessment is not in data"

	taxon_info = data["taxon"]
	assert "sis_id" in taxon_info, "sis_id is not in taxon_info"
	assert "species" in taxon_info, "species is not in taxon_info"

	taxon_assessment = data["assessment"][0]
	assert 'year_published' in taxon_assessment, "year_published is not in taxon_assessment"
	assert 'latest' in taxon_assessment, "latest is not in taxon_assessment"
	assert 'possibly_extinct' in taxon_assessment, "possibly_extinct is not in taxon_assessment"
	assert 'possibly_extinct_in_the_wild' in taxon_assessment, "possibly_extinct_in_the_wild is not in taxon_assessment"
	assert 'sis_taxon_id' in taxon_assessment, "sis_taxon_id is not in taxon_assessment"
	assert 'url' in taxon_assessment, "url is not in taxon_assessment"
	assert 'assessment_id' in taxon_assessment, "uassessment_id is not in taxon_assessment"
	assert 'scopes' in taxon_assessment, "scopes is not in taxon_assessment"

	# assess_details ----
	if assess_details and query == "Alytes muletensis":
		assert "criteria" in taxon_assessment, "criteria is not in taxon_assessment"
		assert "citation" in taxon_assessment, "citation is not in taxon_assessment"
		assert "population_trend" in taxon_assessment, "population_trend is not in taxon_assessment"
		assert "red_list_category" in taxon_assessment, "red_list_category is not in taxon_assessment"
		assert "supplementary_info" in taxon_assessment, "supplementary_info is not in taxon_assessment"
		assert "documentation" in taxon_assessment, "documentation is not in taxon_assessment"
		assert "biogeographical_realms" in taxon_assessment, "biogeographical_realms is not in taxon_assessment"
		assert "conservation_actions" in taxon_assessment, "conservation_actions is not in taxon_assessment"
		assert "faos" in taxon_assessment, "faos is not in taxon_assessment"
		assert "habitats" in taxon_assessment, "habitats is not in taxon_assessment"
		assert "locations" in taxon_assessment, "locations is not in taxon_assessment"
		assert "researches" in taxon_assessment, "researches is not in taxon_assessment"
		assert "use_and_trade" in taxon_assessment, "use_and_trade is not in taxon_assessment"
		assert "threats" in taxon_assessment, "threats is not in taxon_assessment"
		assert "credits" in taxon_assessment, "credits is not in taxon_assessment"
		assert "errata" in taxon_assessment, "errata is not in taxon_assessment"
		assert "references" in taxon_assessment, "references is not in taxon_assessment"
		assert "growth_forms" in taxon_assessment, "growth_forms is not in taxon_assessment"
		assert "lmes" in taxon_assessment, "lmes is not in taxon_assessment"
		assert "scopes" in taxon_assessment, "scopes is not in taxon_assessment"
		assert "stresses" in taxon_assessment, "stresses is not in taxon_assessment"
		assert "systems" in taxon_assessment, "systems is not in taxon_assessment"
		assert len(taxon_assessment) == 1, "The length of the taxon_assessment is not 1"
		assert taxon_assessment.get('year_published') == 2024, "The year_published is not 2024"

	if scope == ["Global"] and query == "Alytes muletensis":
		assert taxon_assessment.get('scope') == "Global;Europe;Mediterranean", "The scope is not Global;Europe;Mediterranean"

	if scope == ["Global"] and query == "Bufotes viridis":
		assert taxon_assessment.get('scope') == "Global", "The scope is not Global"
