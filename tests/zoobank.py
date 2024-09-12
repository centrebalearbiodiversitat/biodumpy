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
	bdp = Biodumpy([ZooBank(bulk=False, dataset_size=dataset_size, info=info)])
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
		(["Bufotes viridis"], True, "large"),
	],
)
def test_download_syn(query, info, dataset_size):
	with redirect_stdout(trap):
		data = zoobank_query(query=query, info=info, dataset_size=dataset_size)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

	if info:
		data = data[0]
		assert "Abbreviation" in data[0], "Abbreviation is not in the data"
		assert "Identifier" in data[0], "Identifier is not in the data"
		assert "IdentifierUUID" in data[0], "IdentifierUUID is not in the data"

	else:
		assert "referenceuuid" in data[0], "referenceuuid is not in the data"
		assert "label" in data[0], "label is not in the data"
		assert "year" in data[0], "year is not in the data"
		assert "title" in data[0], "title is not in the data"
