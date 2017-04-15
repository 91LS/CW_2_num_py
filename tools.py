import itertools as it
import classes
import collections


# Functions for read rule based system and transform symbols to integers. <---------------------------------------------
def get_system_objects(system_file):
    """Return numpy array with integers that represent Rule Based System and dictionary to encode true values."""
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


# Base function for all algorithms. <-----------------------------------------------------------------------------------
def find_rules(algorithm, decision_system):
    """Return rules calculeted by function from argument."""
    rules = []  # all rules from current algorithm
    number_of_attributes = len(decision_system[0]) - 1  # number of attributes
    attributes = [attribute_index for attribute_index in range(number_of_attributes)]  # list of attributes ids

    algorithm(decision_system, rules, attributes)
    return rules


# Covering base function and support functions. <-----------------------------------------------------------------------
def covering(decision_system, rules, attributes):
    """Calculate rules by sequential covering."""
    number_of_attributes = attributes.__len__() # number of attributes
    number_of_objects = decision_system.__len__()  # number of decision objects in decision system
    eliminated = set()  # indexes of object that don't need to calculate

    for scale in range(number_of_attributes):
        scale += 1
        combination_of_attributes = list(it.combinations(attributes, scale))
        for index, decision_object in enumerate(decision_system):
            if index not in eliminated:
                for combination in combination_of_attributes:
                    rule = classes.Rule(combination, decision_object, scale)
                    if is_rule_inconsistent(rule, decision_system):
                        set_rule_support_and_eliminate(rule, decision_system, eliminated)
                        rules.append(rule)
                        break
                if end(eliminated.__len__(), number_of_objects):
                    return
    return


def set_rule_support_and_eliminate(rule, objects, eliminated):
    """Calculate support of rule and eliminate supporting objects"""
    for index, decision_object in enumerate(objects):
        if has_object_fulfill_rule(rule, decision_object) and rule.decision == decision_object[-1]:
            eliminated.add(index)
            rule.support += 1


def end(number_of_eliminated, number_of_objects):
    """Return: True if all objects was used; False if find not covered object."""
    return number_of_eliminated == number_of_objects


# Exhaustive base function and support functions. <---------------------------------------------------------------------
def exhaustive(decision_system, rules, attributes):
    """Calculate rules by exhaustive algorithm (with indistinguishable matrix)."""
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
    """Return indistinguishable matrix."""
    matrix = []
    for current_object in decision_system:
        matrix.append(get_row(current_object, decision_system))
    return matrix


def get_row(current_object, decision_system):
    """Return row of indistinguishable matrix."""
    row = []
    for decision_object in decision_system:
        row.append(get_cell(current_object, decision_object))
    return row


def get_cell(current_object, decision_object):
    """Return cell of indistinguishable matrix."""
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
    """Return: True if combination of attributes is in cell of indistinguishable matrix; False if not."""
    for attribute in combination:
        if attribute not in cell:
            return False
    return True


def is_combination_in_row(row, combination):
    """Return: True if combination is in object; False if not."""
    for cell in row:
        if is_combination_in_cell(cell, combination):
            return True
    return False


def has_rule_contains_rule(first, second):
    """Return: True if all descriptors from second rule is in first rule; False if at lest one descriptor is not in."""
    for key, value in second.descriptors.items():
        if key not in first.descriptors or first.descriptors[key] != value:
            return False
    return True


def is_rule_in_rules(rule, rules):
    """Return: True if at least one rule from rules contains rule from argument; False if rule not contains."""
    for added_rule in rules:
        if has_rule_contains_rule(rule, added_rule):
            return True
    return False


def set_rule_support(rule, objects):
    """Calculate support of rule (in exhaustive algorithm)."""
    for decision_object in objects:
        if has_object_fulfill_rule(rule, decision_object) and rule.decision == decision_object[-1]:
            rule.support += 1


# LEM2 base function and support functions. <---------------------------------------------------------------------------
def lem2(decision_system, rules, attributes):
    """Calculate rules by LEM2 algorithm (Learn from Examples by Modules)."""
    unique_decisions = get_unique(decision[-1] for decision in decision_system)
    for decision in unique_decisions:
        concept_objects = get_concept_objects(decision_system, decision)
        while concept_objects:
            descriptors = {}
            tmp_attributes = attributes[:]
            find_lem_rules(concept_objects, descriptors, concept_objects, tmp_attributes, decision_system, rules)


def find_lem_rules(mode_objects, descriptors, concept_objects, tmp_attributes, decision_system, rules):
    """Find all rules by recursion."""
    descriptor = get_descriptor(mode_objects, tmp_attributes)
    add_descriptor(descriptors, descriptor)
    remove_attribute(tmp_attributes, descriptor)
    mode_objects = get_mode_objects(mode_objects, descriptor)
    rule = classes.Rule(descriptors.keys(), mode_objects[0], descriptors.keys().__len__())
    if not is_rule_inconsistent(rule, decision_system):
        find_lem_rules(mode_objects, descriptors, concept_objects, tmp_attributes, decision_system, rules)
    else:
        set_rule_support_lem(rule, mode_objects, concept_objects)
        rules.append(rule)


def remove_attribute(attributes, descriptor):
    """Remove attribute from list of attributes."""
    for att in descriptor:
        attributes.remove(att)


def add_descriptor(descriptors, descriptor):
    """Add descriptor to list of descriptors."""
    for key, value in descriptor.items():
        descriptors[key] = value


def set_rule_support_lem(rule, mode_objects, concept_objects):
    """Calculate support of rule."""
    for decision_object in mode_objects:
        if has_object_fulfill_rule(rule, decision_object) and rule.decision == decision_object[-1]:
            concept_objects.remove(decision_object)
            rule.support += 1


def get_mode_objects(objects, descriptors):
    """Return objects that contains descriptors."""
    mode_objects = []
    for decision_object in objects:
        for key, value in descriptors.items():
            if decision_object[key] == value:
                mode_objects.append(decision_object)
    return mode_objects


def get_concept_objects(decision_system, decision):
    """Return objects with decision from argument."""
    concept_objects = []
    for decision_object in decision_system:
        if decision_object[-1] == decision:
            concept_objects.append(decision_object)
    return concept_objects


def get_descriptor(concept_objects, attributes):
    """Return mode descriptor from concept objects."""
    mode_descriptor = {}
    most_common = 0

    for attribute in attributes:
        column = get_concept_column(concept_objects, attribute)
        mode = collections.Counter(column).most_common(1)  # out: [(value, count)]
        if mode[0][1] > most_common:
            most_common = mode[0][1]
            mode_descriptor = {attribute: mode[0][0]}
    return mode_descriptor


def get_concept_column(concept_objects, attribute):
    """Generator for decision objects with decision."""
    column = []
    for decision_object in concept_objects:
        column.append(decision_object[attribute])
    return column


# Universal tools. <----------------------------------------------------------------------------------------------------
def is_rule_inconsistent(rule, objects):
    """Return: True if rule is inconsistent; False if not."""
    for decision_object in objects:
        if rule.decision != decision_object[-1] and has_object_fulfill_rule(rule, decision_object):
            return False
    else:
        return True


def has_object_fulfill_rule(rule, decision_object):
    """Return: True if object fulfill rule; False if not."""
    for key, value in rule.descriptors.items():
        if value != decision_object[key]:
            return False
    else:
        return True


def get_unique(array):
    """Return list of unique values"""
    unique = []
    for number in array:
        if number not in unique:
            unique.append(number)
    return unique


def rename_rules(rules, names):
    """Transform rules from integers to original symbolic values."""
    for rule in rules:
        real_values = {}
        for key, value in rule.descriptors.items():
            real_values[key] = names[value]
        rule.descriptors = real_values
        rule.decision = names.get(rule.decision)


def print_rules(rules):
    """Print all rules on console."""
    for rule in rules:
        rule.print_rule()


def get_scales(rules):
    scales = []
    for rule in rules:
        if rule.scale not in scales:
            scales.append(rule.scale)
    scales.sort()
    return scales


def scale_rules(rules, scale):
    rules_scale = [rule for rule in rules if rule.scale == scale]
    for scale_rule in rules_scale:
        yield scale_rule.print_rule()


def get_rule_scale_length(rules, scale):
    rules_scale = [rule for rule in rules if rule.scale == scale]
    return rules_scale.__len__()
