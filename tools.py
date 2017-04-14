import itertools as it
import classes
from joblib import Parallel, delayed
import multiprocessing



def get_system_objects(system_file):
    """Return numpy array with uint16 that represent Rule Based System and dictionary to encode true values."""
    system_file.seek(0)  # return to beginning of file
    objects = []
    unique_values = {}
    for line in system_file:
        if line.strip() != '':  # true if line isn't empty
            objects.append(get_object(line, unique_values))  # append Decision Object to list of objects
    return objects, dict(zip(unique_values.values(), unique_values.keys()))


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


def is_rule_inconsistent(rule, objects):
    for decision_object in objects:
        if rule.decision != decision_object[-1] and has_object_fulfill_rule(rule, decision_object):
            return False
    else:
        return True


def has_object_fulfill_rule(rule, decision_object):
    for key, value in rule.descriptors.items():
        if value != decision_object[key]:
            return False
    else:
        return True


def set_rule_support_and_eliminate(rule, objects, eliminated):
    """Calculate support of rule and eliminate supporting objects"""
    for index, decision_object in enumerate(objects):
        if has_object_fulfill_rule(rule, decision_object) and rule.decision == decision_object[-1]:
            eliminated.add(index)
            rule.support += 1


def end(number_of_eliminated, number_of_objects):
    return number_of_eliminated == number_of_objects


def covering(decision_system):
    rules = []

    number_of_attributes = len(decision_system[0]) - 1  # number of attributes
    attributes = [attribute_index for attribute_index in range(number_of_attributes)]  # list of attributes ids
    number_of_objects = decision_system.__len__()  # number of decision objects in decision system

    eliminated = set()  # indexes of object that don't need to calculate

    for scale in range(number_of_attributes):
        scale += 1
        combination_of_attributes = list(it.combinations(attributes, scale))
        for index, decision_object in enumerate(decision_system):
            if index in eliminated:
                continue
            for combination in combination_of_attributes:
                rule = classes.Rule(combination, decision_object, scale)
                if is_rule_inconsistent(rule, decision_system):
                    set_rule_support_and_eliminate(rule, decision_system, eliminated)
                    rules.append(rule)
                    break
            if end(eliminated.__len__(), number_of_objects):
                return rules

    return rules

num_cores = multiprocessing.cpu_count()
#----------------------------------------------------------------------------#
def exhaustive(decision_system):

    rules = []
    number_of_attributes = len(decision_system[0]) - 1  # number of attributes
    attributes = [att for att in range(number_of_attributes)]  # list of attributes ids

    matrix = get_matrix(decision_system)

    for index, matrix_object in enumerate(matrix):
        for combination in all_combinations(attributes):
            if not is_combination_in_row(matrix_object, combination):
                rule = classes.Rule(combination, decision_system[index], combination.__len__())
                if not is_rule_in_rules(rule, rules):
                    set_rule_support(rule, decision_system)
                    rules.append(rule)
    return rules


def get_matrix(decision_system):
    matrix = []
    for current_object in decision_system:
        matrix.append(get_row(current_object, decision_system))
    return matrix


def get_row(current_object, decision_system):
    row = []
    for decision_object in decision_system:
        row.append(get_cell(current_object, decision_object))
    return row


def get_cell(current_object, decision_object):
    cell = []
    if current_object[-1] == decision_object[-1]:
        return cell
    for index, attribute in enumerate(current_object):
        if attribute == decision_object[index]:
            cell.append(index)
    return cell


def all_combinations(attributes):
    """Generator for all picks combinations."""
    for scale in range(len(attributes)):
        for combination in it.combinations(attributes, scale + 1):
            yield combination


def is_combination_in_cell(cell, combination):
    for attribute in combination:
        if attribute not in cell:
            return False
    return True


def is_combination_in_row(row, combination):
    for cell in row:
        if is_combination_in_cell(cell, combination):
            return True
    return False


def has_rule_contains_rule(first, second):
    for key, value in second.descriptors.items():
        if key not in first.descriptors or first.descriptors[key] != value:
            return False
    return True


def is_rule_in_rules(rule, rules):
    for added_rule in rules:
        if has_rule_contains_rule(rule, added_rule):
            return True
    return False


def set_rule_support(rule, objects):
    """Calculate support of rule."""
    for decision_object in objects:
        if has_object_fulfill_rule(rule, decision_object) and rule.decision == decision_object[-1]:
            rule.support += 1




















# ----------------------------------------------------------------------------#
def rename_rules(rules, names):
    for rule in rules:
        real_values = {}
        for key, value in rule.descriptors.items():
            real_values[key] = names[value]
        rule.descriptors = real_values
        rule.decision = names.get(rule.decision)

def print_rules(rules):
    for rule in rules:
        rule.print_rule()
#----------------------------------------------------------------------------#
