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

API_KEY = "YOUR_API_KEY"

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
	"europe",
]


def iucn_query(query, api_key, habitat, regions, historical_threats, threats, output_format):
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
				historical_threats=historical_threats,
				threats=threats,
				output_format=output_format,
			)
		]
	)
	bdp.download_data(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

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
	assert iucn.historical_threats == False
	assert iucn.threats == False
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
	"query, regions, habitat, historical_threats, threats, output_format",
	[
		(["Alytes muletensis"], ["global"], False, False, False, "json"),
		(["Alytes muletensis"], ["global"], True, False, False, "json"),
		(["Alytes muletensis"], ["global"], False, True, False, "json"),
		(["Alytes muletensis"], ["global"], False, False, True, "json"),
	],
)
def test_download(query, regions, habitat, historical_threats, threats, output_format):
	with redirect_stdout(trap):
		data = iucn_query(
			query=query,
			regions=regions,
			habitat=habitat,
			historical_threats=historical_threats,
			threats=threats,
			output_format=output_format,
			api_key=API_KEY,
		)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	# Check some fields
	data = data[0]
	assert "taxonid" in data, "taxonid is not in data"
	assert "scientific_name" in data, "scientific_name is not in data"
	assert "category" in data, "category is not in data"
	assert "assessment_date" in data, "assessment_date is not in data"
	assert "region" in data, "region is not in data"
	assert data["region"] == "global", "assessment_date is not in data"

	if habitat:
		assert "habitat" in data, "habitat is not in data"
		assert "code" in data["habitat"], "code is not in data['habitat']"
		assert "habitat" in data["habitat"], "habitat is not in data['habitat']"
		assert "suitability" in data["habitat"], "suitability is not in data['habitat']"
		assert "season" in data["habitat"], "season is not in data['habitat']"

	if historical_threats:
		assert "historical_threats" in data, "historical_threats is not in data"
		assert "year" in data["historical_threats"], "code is not in data['historical_threats']"
		assert "assess_year" in data["historical_threats"], "assess_year is not in data['historical_threats']"
		assert "code" in data["historical_threats"], "code is not in data['historical_threats']"
		assert "category" in data["historical_threats"], "category is not in data['historical_threats']"
		assert "region" in data["historical_threats"], "region is not in data['historical_threats']"

	if threats:
		assert "threats" in data, "threats is not in data"
		assert "title" in data["threats"], "title is not in data['threats']"
		assert "timing" in data["threats"], "timing is not in data['threats']"
		assert "code" in data["threats"], "code is not in data['threats']"
		assert "scope" in data["threats"], "scope is not in data['threats']"
		assert "score" in data["threats"], "score is not in data['threats']"
