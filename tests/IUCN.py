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

# TO DO: remove api key
API_KEY = ""

IUCN_REGIONS = [
	"northern_africa",
	"global",
	"pan-africa",
	"central_africa",
	"eastern_africa",
	"northeastern_africa",
	"western_africa",
	"southern_africa",
	"mediterranean",
	"europe"
]


def iucn_query(query, api_key, habitat, regions, historical, threats, weblink, output_format):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy(
		[
			IUCN(
				bulk=True,
				api_key=api_key,
				habitat=habitat,
				regions=regions,
				historical=historical,
				threats=threats,
				weblink=weblink,
				output_format=output_format
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
	iucn = IUCN(api_key=API_KEY)

	# Verify default parameters
	assert iucn.habitat == False
	assert iucn.historical == False
	assert iucn.threats == False
	assert iucn.weblink == False
	assert iucn.output_format == "json"

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match="Invalid output_format. Expected 'json'."):
		IUCN(output_format="csv", api_key=API_KEY)


def test_validate_regions_valid():
	# Ensures that valid regions don't raise an error.
	regions = ["europe", "global"]
	try:
		for region in regions:
			if region not in IUCN_REGIONS:
				raise ValueError(f"Choose an IUCN region from the following options: {IUCN_REGIONS}.")
	except ValueError:
		pytest.fail("ValueError raised with valid regions")


def test_validate_regions_invalid():
	# Ensures that invalid regions raise a ValueError with the correct message.
	regions = ["europe", "atlantis"]  # 'atlantis' is not in IUCN_REGIONS

	with pytest.raises(ValueError) as exc_info:
		for region in regions:
			if region not in IUCN_REGIONS:
				raise ValueError(f"Choose an IUCN region from the following options: {IUCN_REGIONS}.")

	assert "Choose an IUCN region from the following options" in str(exc_info.value)


@pytest.mark.parametrize(
	"query, regions, habitat, historical, threats, weblink, output_format",
	[
		(["Alytes muletensis"], ["global"], False, False, False, False, "json"),
		(["Alytes muletensis"], ["global"], True, False, False, False, "json"),
		(["Alytes muletensis"], ["global"], False, True, False, False, "json"),
		(["Alytes muletensis"], ["global"], False, False, True, False, "json"),
		(["Alytes muletensis"], ["global"], False, False, False, True, "json")
	],
)
def test_download(query, regions, habitat, historical, threats, weblink, output_format):
	with redirect_stdout(trap):
		data = iucn_query(
			query=query,
			regions=regions,
			habitat=habitat,
			historical=historical,
			threats=threats,
			output_format=output_format,
			weblink=weblink,
			api_key=API_KEY
		)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check some fields
	data = data[0]
	assert "taxonid" in data, "taxonid is not in data"
	assert data["taxonid"] == 977, "the taxonid is not 977"

	assert "scientific_name" in data, "scientific_name is not in data"
	assert data["scientific_name"] == "Alytes muletensis", "the scientific_name is not Alytes muletensis"

	assert "category" in data, "category is not in data"
	assert data["category"] == "EN", "the category is not EN"

	assert "assessment_date" in data, "assessment_date is not in data"
	assert data["assessment_date"] == "2020-04-23", "the assessment_date is not 2020-04-23"

	assert "region" in data, "region is not in data"
	assert data["region"] == "global", "the region is not global"

	if habitat:
		assert "habitat" in data, "habitat is not in data"

		habitat = data["habitat"]

		assert len(habitat) == 4, "the number of habitat is 4"

		assert "code" in habitat[0], "code is not in habitat[0]"
		assert habitat[0]["code"] == "14.2", "the code is not 14.2"

		assert "habitat" in habitat[0], "habitat is not in habitat[0]"
		assert habitat[0]["habitat"] == "Artificial/Terrestrial - Pastureland", "the habitat is not Artificial/Terrestrial - Pastureland"

		assert "suitability" in habitat[0], "suitability is not in habitat[0]"
		assert habitat[0]["suitability"] == "Suitable", "the suitability is not Suitable"

		assert "season" in habitat[0], "season is not in habitat[0]"
		assert habitat[0]["season"] == "Resident", "the season is not Resident"

		assert "majorimportance" in habitat[0], "majorimportance is not in habitat[0]"
		assert habitat[0]["majorimportance"] is None, "the majorimportance is not None"

	if historical:
		assert "historical" in data, "historical is not in data"

		historical = data["historical"]

		assert len(historical) == 7, "the number of historical records is 7"

		assert "year" in historical[0], "code is not in historical[0]"
		assert historical[0]["year"] == "2020", "the year is not 2020"

		assert "assess_year" in historical[0], "assess_year is not in historical[0]"
		assert historical[0]["assess_year"] == "2020", "the year is not 2020"

		assert "code" in historical[0], "code is not in historical[0]"
		assert historical[0]["code"] == "EN", "the code is not EN"

		assert "category" in historical[0], "category is not in historical[0]"
		assert historical[0]["category"] == "Endangered", "the category is not Endangered"

		assert "region" in historical[0], "region is not in historical[0]"
		assert historical[0]["region"] == "global", "the region is not global"

	if threats:
		assert "threats" in data, "threats is not in data"

		threats = data["threats"]

		assert len(threats) == 12, "the number of threats records is 12"

		assert "code" in threats[0], "code is not in threats[0]"
		assert threats[0]["code"] == "1.1", "the code is not 1.1"

		assert "title" in threats[0], "title is not in threats[0]"
		assert threats[0]["title"] == "Housing & urban areas", "the title is not Housing & urban areas"

		assert "timing" in threats[0], "timing is not in threats[0]"
		assert threats[0]["timing"] == "Ongoing", "the timing is not Ongoing"

		assert "scope" in threats[0], "scope is not in threats[0]"
		assert threats[0]["scope"] is None, "the scope is not None"

		assert "severity" in threats[0], "severity is not in threats[0]"
		assert threats[0]["severity"] is None, "the severity is not None"

		assert "score" in threats[0], "score is not in threats[0]"
		assert threats[0]["score"] == "Low Impact: 3", "the score is not Low Impact: 3"

		assert "invasive" in threats[0], "invasive is not in threats[0]"
		assert threats[0]["invasive"] is None, "the invasive is not None"

	if weblink:
		assert "weblink" in data, "weblink is not in data"
		assert data["weblink"] == "https://apiv3.iucnredlist.org/api/v3/taxonredirect/977/global", "The weblink is not correct"
