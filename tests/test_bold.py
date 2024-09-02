import pytest
import tempfile
import os
import json

import io
from contextlib import redirect_stdout

from biodumpy import Biodumpy
from biodumpy.inputs import BOLD

# set a trap and redirect stdout. Remove the print of the function. In this wat the test output is cleanest.
trap = io.StringIO()


def bold_query(query, summary, fasta, output_format):
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Construct the dynamic path using formatted strings
        dynamic_path = os.path.join(temp_dir)

    # Start biodumpy function
    bdp = Biodumpy([BOLD(bulk=True, summary=summary, fasta=fasta, output_format=output_format)])
    bdp.start(elements=query, output_path=f'{dynamic_path}/downloads/{{date}}/{{module}}/{{name}}')

    # Retrieve a file path
    dir_date = os.listdir(f'{dynamic_path}/downloads/')[0]
    dir_module = os.listdir(f'{dynamic_path}/downloads/{dir_date}')[0]
    file_list = os.listdir(f'{dynamic_path}/downloads/{dir_date}/{dir_module}')[0]

    file = os.path.join(f'{dynamic_path}/downloads/{dir_date}/{dir_module}/{file_list}')
    if output_format == 'json':
        with open(file, 'r') as f:
            data = json.load(f)
    elif output_format == 'fasta':
        with open(file, 'r') as file:
            data = file.read()


    return data


def test_bold_initialization():
    # Test default initialization
    bold = BOLD()

    # Verify default parameters
    assert bold.summary == False
    assert bold.fasta == False
    assert bold.bulk == False
    assert bold.output_format == 'json'

    # Objective: Verify that the class raises a ValueError when an invalid value is provided for the
    # output_format parameter. If fasta parameter is True, output_format has to be 'fasta'.
    with pytest.raises(ValueError, match='Invalid output_format. Expected fasta.'):
        BOLD(output_format='json', fasta=True)

    # Objective: Verify that the class raises a ValueError when an invalid value is provided for the
    # output_format parameter.
    with pytest.raises(ValueError, match='Invalid output_format. Expected "json" or "fasta".'):
        BOLD(output_format='xml')


@pytest.mark.parametrize('query, summary, fasta, output_format', [
    (['Alytes muletensis'], True, False, 'json'),  # Test the output file of summary=True.
    (['Alytes muletensis'], False, False, 'json'),  # Test the output file of summary=True.
    (['Alytes muletensis'], False, True, 'fasta')  # Test the output of fasta file.
])
def test_download(query, summary, fasta, output_format):
    with redirect_stdout(trap):
        data = bold_query(query=query, summary=summary, fasta=fasta, output_format=output_format)

    # Check if data is not empty
    assert len(data) > 0, 'data length is 0'


    if summary is False and fasta is False:
        # Check the main info in a BOLD JSON file
        data = data[0]
        key = list(data.keys())
        assert 'bin_uri' in data[key[0]], 'bin_uri is not in data'
        assert 'specimen_identifiers' in data[key[0]], 'specimen_identifiers is not in data'
        assert 'taxonomy' in data[key[0]], 'taxonomy is not in data'

    if summary and fasta is False:
        # Check the summary structure
        assert 'record_id' in data[0], 'record_id is not in data'
        assert 'processid' in data[0], 'processid is not in data'
        assert 'bin_uri' in data[0], 'bin_uri is not in data'
        assert 'taxon' in data[0], 'taxon is not in data'
        assert 'country' in data[0], 'country is not in data'
        assert 'province_state' in data[0], 'province_state is not in data'
        assert 'region' in data[0], 'region is not in data'
        assert 'lat' in data[0], 'lat is not in data'
        assert 'lon' in data[0], 'lon is not in data'
        assert 'markercode' in data[0], 'markercode is not in data'
        assert 'genbank_accession' in data[0], 'genbank_accession is not in data'

    if summary is False and fasta is True:
        # Check if the fasta file starts with >
        assert data.startswith('>')

#     # Check the main info in a BOLD JSON file
#     if occ is False:
#         assert 'key' in data[0], 'key is not in data'
#         assert 'scientificName' in data[0], 'scientificName is not in data'
#     else:
#         assert 'key' in data[0], 'key is not in data'
#         assert 'scientificName' in data[0], 'scientificName is not in data'
#         assert 'gadm' in data[0], 'gadm is not in data'
#         assert 'year' in data[0], 'year is not in data'
#         assert 'month' in data[0], 'month is not in data'
#         assert 'day' in data[0], 'day is not in data'
