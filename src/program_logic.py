from dsl import AutomatonDSL
from automata import Automata
import graphviz
import os

class ProgramLogic:
    def __init__(self):
        self.current_automata = None
        self.valid_automata = False
        self.valid_input_string = False

    def compile_automata(self, automaton_def: str):
        """compiles an automata from description written in automaton dsl. 
        Delegates compilation to the automaton dsl compiler."""
        automaton = AutomatonDSL.parse_automaton(automaton_def)
        if automaton:
            self.current_automata = automaton
            self.valid_automata = True
            self.valid_input_string = False # reset on new automaton
        else:
            self.current_automata = "Automata definition: \n\nSYNTAX ERROR:\n\n" + automaton_def
            self.valid_automata = False

    def set_input_string(self, input_string: str):
        if self.current_automata.char_in_alphabet(input_string):
            self.valid_input_string = True
            self.input_string = input_string
        else:
            self.valid_input_string = False
            self.input_string = "SYNTAX ERROR:" + "\n\n" + input_string

    @staticmethod
    # creates a visualization of the current state of the automata using graphviz
    def visualizeAutomata(automata):

        automata_data = automata.get_automata_data()
        states = automata_data["states"]
        transition_func = automata_data["transition_func"]
        accept_states = automata_data["accept_states"]
        current_state = automata.get_state()
        
        visualized_DFA = graphviz.Digraph(engine='dot')

        visualized_DFA.attr(overlap="false", nodesep="0.5", ranksep="0.8", splines="true")

        """

        dot_file = 'graph_layout.dot'
        node_positions = parse_dotfile(dot_file, states)

        """

        # iterate through list of states, creating nodes for each
        for state in states:
            
            # if the state is the current state and an accept state, draw double circle and fill in green
            if state == current_state and state in accept_states:
                visualized_DFA.node(state, style='filled', fillcolor='green', shape='doublecircle')
                continue
            
            # if state is an accept state, double circle
            if state in accept_states:
                visualized_DFA.node(state, shape='doublecircle')
                continue
            
            # if the state is the current state, fill in green
            if state == current_state:
                visualized_DFA.node(state, style='filled', fillcolor='green', shape='circle')
                continue
            
            # otherwise just draw a circle
            visualized_DFA.node(state, shape='circle')
        
        # iterate through transition function, creating edges between states
        for key in transition_func:
            visualized_DFA.edge(key[0], transition_func[key], label = key[1])
        
        visualized_DFA.render('automata_visualization', format='png', view=False, cleanup=True)

        dot_file = 'graph_layout'
        visualized_DFA.render(dot_file, format='dot')   # generates dot file


    """
    function for parsing the dot file generated by the rendering engine
    intuition was to allow rendering engine to generate automata the first time, then create a dictionary of nodes -> positions, and set position manually
    however dot rendering engine does not allow manual position setting and other rendering engines do not do a good job of rendering

    issue to figure out later
    """
    def parse_dotfile(filename, states):

        positions = {}
        for state in states:
            positions[state] = None

        if os.path.exists(filename):

            file = open(filename, 'r')
            lines = file.readlines()
            found = False
            current_key = None

            for line in lines:
                line = line.strip()
                words = line.split()

                if ( '->' not in line and words[0] in positions.keys()):
                    found = True
                    current_key = words[0]
                    continue

                if found and 'pos' in line:
                    pos = line[5:-2]
                    formatted = pos + '!'
                    positions[current_key] = formatted
                    found = False
                    current_key = None
                else: continue

            file.close()
            return positions


