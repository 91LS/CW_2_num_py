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
    return decision_object

get_object.counter = 0


def get_descriptors(decision_object, attributes):
    descriptors = {}
    for attribute in attributes:
        descriptors[attribute] = decision_object[attribute]
    return descriptors


def has_object_fulfill_rule(rule, decision_object):
    """Return true if fulfill; return false if not"""
    for key, value in rule.descriptors.items():
        if value != decision_object[key]:
            return False
    else:
        return True


def is_rule_inconsistent(rule, objects):
    """Return true if inconsistent; return false if not"""
    for decision_object in objects:
        if has_object_fulfill_rule(rule, decision_object) and rule.decision != decision_object[-1]:
            return False
    else:
        return True


def calculate_support(rule, objects, eliminated):
    """Calculate support of rule and eliminate supporting objects"""
    support = 0
    for object_index, decision_object in enumerate(objects):
        if has_object_fulfill_rule(rule, decision_object) and rule.decision == decision_object[-1]:
            eliminated.add(object_index)
            support += 1
    rule.support = support


def covering(decision_system):
    rules = []
    number_of_attributes = len(decision_system[0]) - 1  # number of attributes
    attributes_ids = [att for att in range(number_of_attributes)]  # list of attributes ids
    eliminated = set()  # set
    for scale in range(number_of_attributes):
        scale += 1
        for object_index, decision_object in enumerate(decision_system):
            if object_index in eliminated:
                continue
            combination_of_attributes = list(it.combinations(attributes_ids, scale))
            for combination in combination_of_attributes:
                descriptors = get_descriptors(decision_object, combination)
                decision = decision_object[-1]
                rule = classes.Rule(descriptors, decision, scale)
                if is_rule_inconsistent(rule, decision_system):
                    calculate_support(rule, decision_system, eliminated)
                    rules.append(rule)
                    break
            if len(eliminated) == decision_system.shape[0]:
                break
    return rules


def rename_rules(rules, names):
    for rule in rules:
        real_values = {}
        for key, value in rule.descriptors.items():
            real_values[key] = names[value]
        rule.descriptors = real_values
        rule.decision = names.get(rule.decision)
