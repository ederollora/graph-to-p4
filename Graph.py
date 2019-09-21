from collections import OrderedDict

class Graph:
    def __init__(self):
        self.headers = {}
        self.states = {}
        self.transitions = {}
        self.longest_hname = 0
