import copy
import numpy as np
import itertools as it
import classes


def get_system_objects(system_file):
    """Return numpy array with uint16 that represent Rule Based System and dictionary to encode true values."""
    system_file.seek(0)  # return to beginning of file
    objects = []
    unique_values = {}
    for line in system_file:
        if line.strip() != '':  # true if line isn't empty
            objects.append(get_object(line, unique_values))  # append Decision Object to list of objects
    return np.array(objects, dtype=np.uint16), dict(zip(unique_values.values(), unique_values.keys()))


def get_object(line, unique_values):
    """Transform string values to uint16s and return array with uint16 values"""
    decision_object = []
    line = line.rstrip().split(' ')  # remove from end all white chars and split row by ' '
    for value in line:
        if value not in unique_values:
            unique_values[value] = get_object.counter
            get_object.counter += 1
        decision_object.append(unique_values.get(value))
    decision_object.append(0)
    return decision_object

get_object.counter = 0


def covering(decision_system):
    number_of_attributes = len(decision_system[0]) - 2  # number of attributes
    attributes_ids = [att for att in range(number_of_attributes)]  # list of attributes ids
    rules = []
    for scale in range(number_of_attributes):
        scale += 1
        combination_of_attributes = list(it.combinations(attributes_ids, scale))
        for decision_object in iterate(decision_system):
            for combination in combination_of_attributes:
                descriptors = get_descriptors(decision_object, combination)
                decision = decision_object[-2]
                if is_rule_inconsistent(descriptors, decision, decision_system):
                    rule = classes.Rule(descriptors, decision, scale)
                    calculate_support_and_eliminate(rule, decision_system)
                    rules.append(rule)
                    break
            is_this_the_end(decision_system)
    return rules


def iterate(decision_system):
    for decision_object in decision_system:
        if decision_object[-1] == 1:
            continue
        else:
            yield decision_object


def get_descriptors(decision_object, attributes):
    descriptors = []
    for attribute in attributes:
        descriptors.append([attribute, decision_object[attribute]])
    return descriptors


def has_object_fulfill_rule(descriptors, decision_object):
    """Return true if fulfill; return false if not"""
    for descriptor in descriptors:
        if descriptor[1] != decision_object[descriptor[0]]:
            return False
    else:
        return True


def is_rule_inconsistent(descriptors, decision, objects):
    for decision_object in objects:
        if decision != decision_object[-2] and has_object_fulfill_rule(descriptors, decision_object):
            return False
    else:
        return True

def has_object_fulfill_rule_old(descriptors, decision_object):
    """Return true if fulfill; return false if not"""
    matrix = np.fromiter((fulfill_condition(descriptor, decision_object) for descriptor in descriptors),
                         dtype=np.bool)

    if np.any(matrix == False):
        return False
    else:
        return True


def fulfill_condition(descriptor, decision_object):
    if descriptor[1] == decision_object[descriptor[0]]:
        return True
    else:
        return False


def is_rule_inconsistent_old(descriptors, decision, objects):
    """Return true if inconsistent; return false if not"""
    matrix = np.fromiter((inconsistent_condition(decision_object, descriptors, decision)
                          for decision_object in objects), dtype=np.bool)

    if np.any(matrix == False):
        return False
    else:
        return True


def inconsistent_condition(decision_object, descriptors, decision):
    if decision != decision_object[-1] and has_object_fulfill_rule(descriptors, decision_object):
        return False
    else:
        return True


def calculate_support_and_eliminate(rule, objects):
    """Calculate support of rule and eliminate supporting objects"""
    support = 0
    for decision_object in objects:
        if rule.decision == decision_object[-2] and has_object_fulfill_rule(rule.descriptors, decision_object):
            decision_object[-1] = 1
            support += 1
    rule.support = support


def is_this_the_end(objects):
    if 0 in objects[:, -1]:
        return False
    else:
        return True
