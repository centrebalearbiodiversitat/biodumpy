import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import AVONET

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()

def avonet_query(query, output_format, dir_module="AVONET"):
	# Create temporary directory
	with tempfile.TemporaryDirectory() as temp_dir:
		# Construct the dynamic path using formatted strings
		dynamic_path = os.path.join(temp_dir)

	# Start biodumpy function
	bdp = Biodumpy([AVONET(bulk=True, output_format=output_format)])
	bdp.start(elements=query, output_path=f"{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}")

	# Retrieve a file path
	dir_date = os.listdir(f"{dynamic_path}/downloads/")[0]
	# dir_module = os.listdir(f"{dynamic_path}/downloads/{dir_date}")[0]
	file_list = os.listdir(f"{dynamic_path}/downloads/{dir_date}/{dir_module}")[0]

	file = os.path.join(f"{dynamic_path}/downloads/{dir_date}/{dir_module}/{file_list}")
	if output_format == "json":
		with open(file, "r") as f:
			data = json.load(f)

	return data

@pytest.mark.parametrize(
	"query, output_format",
	[(["Accipiter albogularis"], "json")],
)
def test_download(query, output_format):
	with redirect_stdout(trap):
		data = avonet_query(query=query, output_format=output_format)

	# Check if data is not empty
	assert len(data) > 0, "data length is 0"

    # Check the main info in a BOLD JSON file
	data = data[0]

    # Check if data is not empty
	assert len(data) > 0, "data length is 0"

	assert "Sequence" in data, "Sequence is not in data"
	assert "Avibase.ID1" in data, "Avibase.ID1 is not in data"
	assert "Male" in data, "Male is not in data"
	assert "Wing.Length" in data, "Wing.Length is not in data"