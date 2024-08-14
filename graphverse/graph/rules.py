from abc import ABC, abstractmethod
import random

def define_ascenders(graph, n):
    """Define ascender vertices near n/2."""
    mid = n // 2
    range_start = int(mid * 0.9)
    range_end = int(mid * 1.1)
    candidates = [v for v in graph.nodes() if range_start <= v <= range_end]
    return set(random.sample(candidates, k=len(candidates)//5))

def define_descenders(graph, n):
    """Define descender vertices near n/2."""
    mid = n // 2
    range_start = int(mid * 0.9)
    range_end = int(mid * 1.1)
    candidates = [v for v in graph.nodes() if range_start <= v <= range_end]
    return set(random.sample(candidates, k=len(candidates)//5))

def define_evens_odds(graph, n):
    """Randomly select even and odd vertices."""
    evens = set(random.sample([v for v in graph.nodes() if v % 2 == 0], k=n//10))
    odds = set(random.sample([v for v in graph.nodes() if v % 2 != 0], k=n//10))
    return evens, odds

def check_rule_compliance(walk, ascenders, descenders, evens, odds):
    """Check if a given walk complies with all rules."""
    for i, v in enumerate(walk):
        if v in ascenders:
            if any(walk[j] <= v for j in range(i+1, len(walk))):
                return False
        if v in descenders:
            if any(walk[j] >= v for j in range(i+1, len(walk))):
                return False
        if v in evens:
            if any(walk[j] % 2 != 0 for j in range(i+1, len(walk))):
                return False
        if v in odds:
            if any(walk[j] % 2 == 0 for j in range(i+1, len(walk))):
                return False
    return True

class Rule(ABC):
    @abstractmethod
    def apply(self, walk, graph):
        """
        Check if the rule is satisfied for the given walk.
        
        :param walk: List of vertices representing the walk
        :param graph: The graph on which the walk is performed
        :return: True if the rule is satisfied, False otherwise
        """
        pass

class AscenderRule(Rule):
    def __init__(self, ascenders):
        self.ascenders = ascenders

    def apply(self, graph, walk):
        for i, v in enumerate(walk):
            if v in self.ascenders:
                if any(walk[j] <= v for j in range(i+1, len(walk))):
                    return False
        return True

class DescenderRule(Rule):
    def __init__(self, descenders):
        self.descenders = descenders

    def apply(self, graph, walk):
        for i, v in enumerate(walk):
            if v in self.descenders:
                if any(walk[j] >= v for j in range(i+1, len(walk))):
                    return False
        return True

class EvenRule(Rule):
    def __init__(self, evens):
        self.evens = evens

    def apply(self, graph, walk):
        for i, v in enumerate(walk):
            if v in self.evens:
                if any(walk[j] % 2 != 0 for j in range(i+1, len(walk))):
                    return False
        return True

class OddRule(Rule):
    def __init__(self, odds):
        self.odds = odds

    def applyapply(self, graph, walk):
        for i, v in enumerate(walk):
            if v in self.odds:
                if any(walk[j] % 2 == 0 for j in range(i+1, len(walk))):
                    return False
        return True

class EdgeExistenceRule(Rule):
    def apply(self, walk, graph):
        for i in range(len(walk) - 1):
            if not graph.has_edge(walk[i], walk[i+1]):
                return False
        return True