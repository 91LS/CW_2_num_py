import numpy as np


def get_system_objects(system_file):
    """get info about system, return list of Decision Objects and unique decisions"""
    system_file.seek(0)  # return to beginning of file
    objects = []
    unique_values = {}
    for line in system_file:
        if line.strip() != '':  # true if line isn't empty
            objects.append(get_object(line, unique_values))  # append Decision Object to list of objects
    return np.array(objects, dtype=np.uint16)


def get_object(line, unique_values):
    """Private method. Return Decision Object with list of descriptors and decision"""
    decision_object = []
    line = line.rstrip().split(' ')  # remove from end all white chars and split row by ' '
    for value in line:
        if value not in unique_values:
            unique_values[value] = get_object.counter
            get_object.counter += 1
        decision_object.append(unique_values.get(value))
    return decision_object

get_object.counter = 0


