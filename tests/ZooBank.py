import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import ZooBank

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()


def zoobank_query(query, info, dataset_size):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([ZooBank(bulk=True, dataset_size=dataset_size, info=info)])
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


def test_zoobank_initialization():
	# Test default initialization
	zoobank = ZooBank()

	# Objective: Verify that when a ZOOBANK object is created without passing any arguments, it initializes with the
	# correct default values.
	assert zoobank.dataset_size == "small"
	assert zoobank.info == False
	assert zoobank.output_format == "json"

	# Objective: Verify that the class correctly raises a ValueError when an invalid value is provided for the
	# dataset_size parameter.
	with pytest.raises(ValueError, match="Invalid dataset_size. Expected 'small' or 'large'."):
		ZooBank(dataset_size="invalid")

	# Objective: Verify that the class raises a ValueError when an invalid value is provided for the
	# output_format parameter.
	with pytest.raises(ValueError, match="Invalid output_format. Expected 'json'."):
		ZooBank(output_format="xml")


@pytest.mark.parametrize(
	"query, info, dataset_size",
	[
		(["Bufotes viridis"], False, "small"),
		(["Bufotes viridis"], False, "large"),
		(["Bufotes viridis"], True, "small"),
		(["Bufotes viridis"], True, "large")
	],
)
def test_download_syn(query, info, dataset_size):
	with redirect_stdout(trap):
		data = zoobank_query(query=query, info=info, dataset_size=dataset_size)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	data = data[0]

	if info:
		assert 'Identifier' in data[0], "Identifier not in data"
		assert 'IdentifierDomain' in data[0], "IdentifierDomain not in data"
		assert 'Abbreviation' in data[0], "Abbreviation not in data"
		assert 'IdentifierURL' in data[0], "IdentifierURL not in data"
		assert 'RegisteringAgentGivenName' in data[0], "RegisteringAgentGivenName not in data"
		assert 'RegisteringAgentFamilyName' in data[0], "RegisteringAgentFamilyName not in data"
		assert 'RegisteringAgentOrganizationName' in data[0], "RegisteringAgentOrganizationName not in data"
		assert 'IdentifierUUID' in data[0], "IdentifierUUID not in data"
		assert 'DomainLogoURL' in data[0], "DomainLogoURL not in data"
		assert 'ResolutionNote' in data[0], "ResolutionNote not in data"

	else:
		assert 'referenceuuid' in data, "referenceuuid is not in data"
		assert data['referenceuuid'] == '083a67c2-d89b-4631-bfec-d610d396e68f', "referenceuuid is not 083a67c2-d89b-4631-bfec-d610d396e68f"
		assert 'label' in data, "label is not in data"
		assert 'value' in data, "value is not in data"
		assert 'authorlist' in data, "authorlist is not in data"
		assert 'year' in data, "year is not in data"
		assert data['year'] == '2019', "year is not 2019"
		assert 'title' in data, "title is not in data"
		assert 'citationdetails' in data, "citationdetails is not in data"
		assert 'volume' in data, "volume is not in data"
		assert 'number' in data, "number is not in data"
		assert 'edition' in data, "edition is not in data"
		assert 'publisher' in data, "publisher is not in data"
		assert 'placepublished' in data, "placepublished is not in data"
		assert 'pagination' in data, "pagination is not in data"
		assert 'startpage' in data, "startpage is not in data"
		assert 'endpage' in data, "endpage is not in data"
		assert 'language' in data, "language is not in data"
		assert 'languageid' in data, "languageid is not in data"
		assert 'referencetype' in data, "referencetype is not in data"
		assert data['referencetype'] == 'Journal Article', "referencetype is not Journal Article"
		assert 'lsid' in data, "lsid is not in data"
		assert 'parentreferenceid' in data, "parentreferenceid is not in data"
		assert 'parentreference' in data, "parentreference is not in data"
		assert 'authors' in data, "authors is not in data"
