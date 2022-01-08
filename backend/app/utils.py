""" Collection of small Python functions and classes which make common patterns shorter and easier"""
from typing import List, Any, Dict, Optional, Type

def remove_space(s: str):
    """ """
    shorter_string = s
    for space in " \n\t\r":
        shorter_string = shorter_string.replace(space, "")
    return shorter_string

def parse_list(class_type: Type, default: List[Any] = [], separator: str = ",", raise_error: bool = True):
    """Create a tailored parser to build a list from a string.

    Args:
        class_type (Type): [description]
        default (List[Any], optional): [description]. Defaults to [].
        separator (str, optional): [description]. Defaults to ",".
        raise_error (bool, optional): [description]. Defaults to True.
    """
    def parser(inputs: str = None) -> Optional[List[class_type]]:
        if not isinstance(inputs, str):
            if raise_error:
                raise Exception(f"Could not parse inputs of type {type(inputs)}")
            else:
                print(f"Could not parse inputs of type {type(inputs)}.\nDefault value is passed")
                return default
        # Split the string
        elements = inputs.split(separator)
        # Remove space
        elements = [ e.strip() for e in elements if not e.isspace() ]#[ remove_space(e) for e in elements if not e.isspace() ]
        # Check the typing
        errors = {}
        results = []
        for idx, el in enumerate(elements):
            try:
                results.append(class_type(el))
            except ValueError as e:
                errors[idx] = repr(e)
        if errors:
            if raise_error:
                raise Exception(f"Could not parse elements: {errors}")
            else:
                print(f"Could not parse elements: {errors}.\nDefault value is passed")
                return default
        else:
            return results
    return parser

def parse_dict(key_type: Type, value_type: Type, default: Dict[Any, Any] = {}, item_separator: str = ",", key_value_separator: str = ",", raise_error: bool = True):
    """Create a tailored parser to build a dict from a string.

    Args:
        key_type (Type): [description]
        value_type (Type): [description]
        default (Dict[Any, Any], optional): [description]. Defaults to {}.
        item_separator (str, optional): [description]. Defaults to ",".
        key_value_separator (str, optional): [description]. Defaults to ",".
        raise_error (bool, optional): [description]. Defaults to True.
    """
    def parser(inputs: str = None) -> Optional[Dict[key_type, value_type]]:
        if not isinstance(inputs, str):
            if raise_error:
                raise Exception(f"Could not parse inputs of type {type(inputs)}")
            else:
                print(f"Could not parse inputs of type {type(inputs)}.\nDefault value is passed")
                return default
        # Split the string
        elements = inputs.split(item_separator)
        # Remove space
        elements = [ e.split() for e in elements if not e.isspace() ]
        # Check the typing
        errors = {}
        results = []
        for idx, el in enumerate(elements):
            try:
                key, value = el.split(key_value_separator)
                results.append( (key_type(key), value_type(value)) )
            except ValueError as e:
                errors[idx] = repr(e)
        if errors:
            if raise_error:
                raise Exception(f"Could not parse elements: {errors}")
            else:
                print(f"Could not parse elements: {errors}.\nDefault value is passed")
                return default
        else:
            results = dict(results)
            return results
    return parser


