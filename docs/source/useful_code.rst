Useful Code
===========

Below, we have compiled a collection of useful code snippets that can assist with daily tasks.

Save object in JSON format
--------------------------

This example uses placeholder data.

.. code-block:: python

    import json

    nested_list = [
        ["Apple", "Banana", "Cherry"],
        [10, 20, 30],
        ["Cat", "Dog", ["Parrot", "Fish"]]
        ]

    # Save JSON file
    filename = './FINE_NAME.json'
    with open(filename, 'w') as json_file:
        json.dump(nested_list, json_file, indent=4)


Save object in CSV format
-------------------------

This example uses placeholder data.

.. code-block:: python

    import pandas as pd

    nested_list = [
    ["Apple", "Banana", "Cherry"],
    [10, 20, 30],
    ["Cat", "Dog", "Parrot"]
    ]

    df = pd.DataFrame(nested_list)
    csv_filename = './FINE_NAME.csv'
    df.to_csv(csv_filename, index=False)



Main code to filter JSON files
------------------------------

Download the data using the BOLD module before performing the example.

.. code-block:: python

    # Import the Python json module
    import json

    # Load the file to filter
    file = './BOLD/bulk.json'
    with open(file, 'r') as f:
        data = json.load(f)

    # Create a empty list to store the filtered data
    filtered_data = []

    # Crete a for cycle to iterate in json file to filter.
    # Here we use a BOLD file.
    for entry in data:
        taxonomy = entry.get('taxonomy', None)
        collection = entry.get('collection_event', None)

        filtered_data.append({'record_id': entry.get('record_id', None),
                              'processid': entry.get('processid', None),
                              'phylum': taxonomy.get('phylum', {}).get('taxon', {}).get('name'),
                              'class': taxonomy.get('class', {}).get('taxon', {}).get('name'),
                              'order': taxonomy.get('order', {}).get('taxon', {}).get('name'),
                              'family': taxonomy.get('family', {}).get('taxon', {}).get('name'),
                              'genus': taxonomy.get('genus', {}).get('taxon', {}).get('name'),
                              'species': taxonomy.get('species', {}).get('taxon', {}).get('name'),
                              'collectors': collection.get('collectors', {}),
                              'country': collection.get('country', {}),
                              'lat': collection.get('coordinates', {}).get('lat', {}),
                              'lon': collection.get('coordinates', {}).get('lon', {})
                              })
