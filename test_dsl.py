import pytest
from dsl import AutomatonDSL

def setup_correct_automaton():
    """Correct Automata Description"""
    return """
    automaton hector {
        states = {q0, q1};
        alphabet = {0, 1};
        transition_func = {
            (q0, 0): q1,
            (q0, 1): q0,
            (q1, 0): q0,
            (q1, 1): q1
        };
        start_state = q0;
        accept_states = {q1};
    }
    """

def setup_automaton_missing_components():
    """Automata Description that is missing states component"""
    return """
    automaton hector {
        alphabet = {0, 1};
        transition_func = {
            (q0, 0): q1,
            (q0, 1): q0,
            (q1, 0): q0,
            (q1, 1): q1
        };
        start_state = q0;
        accept_states = {q1};
    }
    """

def test_parse_components():
    """Tests that components of properly formatted automaton are parsed correctly"""
    # parse correct automaton
    automaton_file = setup_correct_automaton()
    name, body = AutomatonDSL._parse_components(automaton_file)
    print(body)
    # ensure all components are presetn
    assert name == "hector"
    assert 'states={q0,q1}' in body
    assert 'alphabet={0,1}' in body
    assert 'transition_func={(q0,0):q1,(q0,1):q0,(q1,0):q0,(q1,1):q1}' in body
    assert 'start_state=q0' in body
    assert 'accept_states={q1}' in body

def test_parse_missing_component_fails():
    """Tests that components of properly formatted automaton are parsed correctly"""
    # parse correct automaton
    automaton_file = setup_automaton_missing_components()
    name, body = AutomatonDSL._parse_components(automaton_file)
    # ensure this does not compile
    assert name is None
    assert body is None

def setup_correct_states_component():
    return "states={q0,q1,q3,q4}"

def setup_states_component_with_duplicates():
    return "states={q0,q1,q3,q4,q0}"

def setup_states_missing_braces_component():
    return "states={q0 q1,q3,q4"

def test_parse_states():
    """tests that correct syntax is correctly parsed"""
    states_str = setup_correct_states_component()
    states = AutomatonDSL._parse_states(states_str)
    assert states == ['q0', 'q1', 'q3', 'q4']

def test_missing_braces():
    """tests that incorrect syntax is caught as syntax error"""
    states_str = setup_states_missing_braces_component()
    states = AutomatonDSL._parse_states(states_str)
    assert states is None

def test_duplicates():
    """tests that duplicate states are caught as syntax error"""
    states_str = setup_states_component_with_duplicates()
    states = AutomatonDSL._parse_states(states_str)
    assert states is None
