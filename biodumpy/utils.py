import csv
import json
import os


def dump_to_json(file_name, obj_list):
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(file_name, 'w+') as f:
        json.dump(obj_list, f, indent=4)


def dump_to_csv(file_name, obj_list):
    directory = os.path.dirname(file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    headers = []
    unroll_headers = []
    if len(obj_list) > 0:
        headers = []
        unroll_headers = []
        for obj in obj_list:
            headers = list(obj_list[0].keys())
            for k, v in obj_list[0].items():
                if isinstance(v, dict):
                    for kk, vv in v.items():
                        unroll_headers.append(kk)
                else:
                    unroll_headers.append(k)

    with open(file_name, mode='w+') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=unroll_headers)

        writer.writeheader()
        for obj in obj_list:
            row = {}
            for field in headers:
                if field in obj:
                    current = obj[field]
                    if isinstance(current, list):
                        row[field] = json.dumps(current)
                    elif isinstance(current, dict):
                        for k, v in current.items():
                            row[k] = json.dumps(v) if isinstance(v, dict) or isinstance(v, list) else v
                    else:
                        row[field] = current
                else:
                    row[field] = None

            writer.writerow(row)


def split_to_batches(input_list, batch_size: int):
    """
        Divides a list into smaller batches of a specified size.

        Parameters:
        input_list (list): The list to be divided into batches.
        batch_size (int): The size of each batch.

        Returns:
        list of lists: A list containing the smaller batches.

        Example usage:
        input_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        batch_size = 3
        batches = divide_list_into_batches_by_size(input_list, batch_size)
        print(batches)  # Output: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [input_list[i:i+batch_size] for i in range(0, len(input_list), batch_size)]
