from abc import ABC, abstractmethod
import random

def define_all_rules(graph, n, num_repeaters, repeater_min_steps, repeater_max_steps):
    """
    Define all rule vertices while ensuring each vertex is assigned at most one rule.
    """
    rule_vertices = set()

    # Define ascenders
    ascenders = define_ascenders(graph, n, rule_vertices)
    rule_vertices.update(ascenders)

    # Define descenders
    descenders = define_descenders(graph, n, rule_vertices)
    rule_vertices.update(descenders)

    # Define evens and odds
    evens, odds = define_evens_odds(graph, n, rule_vertices)
    rule_vertices.update(evens)
    rule_vertices.update(odds)

    # Define repeaters
    repeaters = define_repeaters(graph, num_repeaters, repeater_min_steps, repeater_max_steps, rule_vertices)

    return ascenders, descenders, evens, odds, repeaters

def define_ascenders(graph, n, existing_rule_vertices):
    """
    Define ascender vertices while ensuring they are not already assigned to another rule.
    """
    available_vertices = set(graph.nodes()) - existing_rule_vertices
    mid = n // 2
    range_start = int(mid * 0.9)
    range_end = int(mid * 1.1)
    candidates = [v for v in available_vertices if range_start <= v <= range_end]
    return set(random.sample(candidates, k=min(len(candidates)//5, len(candidates))))

def define_descenders(graph, n, existing_rule_vertices):
    """
    Define descender vertices while ensuring they are not already assigned to another rule.
    """
    available_vertices = set(graph.nodes()) - existing_rule_vertices
    mid = n // 2
    range_start = int(mid * 0.9)
    range_end = int(mid * 1.1)
    candidates = [v for v in available_vertices if range_start <= v <= range_end]
    return set(random.sample(candidates, k=min(len(candidates)//5, len(candidates))))

def define_evens_odds(graph, n, existing_rule_vertices):
    """
    Randomly select even and odd vertices that are not already assigned to another rule.
    """
    available_vertices = set(graph.nodes()) - existing_rule_vertices
    evens = set(random.sample([v for v in available_vertices if v % 2 == 0], k=min(n//10, len(available_vertices))))
    odds = set(random.sample([v for v in available_vertices if v % 2 != 0], k=min(n//10, len(available_vertices))))
    return evens, odds

def define_repeaters(graph, num_repeaters, min_steps, max_steps, existing_rule_vertices):
    """
    Randomly select vertices and their corresponding number of steps for the repeater rule.
    Add k-1 edges to form a loop starting and stopping at the repeater vertex.
    """
    repeaters = {}
    available_vertices = set(graph.nodes()) - existing_rule_vertices
    
    for _ in range(num_repeaters):
        vertex = random.choice(list(available_vertices))
        steps = random.randint(min_steps, max_steps)
        
        # Add k-1 edges to form a loop starting and stopping at the repeater vertex
        loop_vertices = random.sample(list(available_vertices), steps - 1)
        loop_vertices.insert(0, vertex)
        loop_vertices.append(vertex)
        
        for i in range(len(loop_vertices) - 1):
            graph.add_edge(loop_vertices[i], loop_vertices[i + 1])
        
        repeaters[vertex] = steps
    
    return repeaters

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
        walk = [int(item) for item in walk]
        for i, v in enumerate(walk):
            if v in self.ascenders:
                if any(walk[j] < v for j in range(i+1, len(walk))):
                    return False
        return True
    
    def get_violation_position(self, graph, walk):
        for i in range(len(walk) - 1):
            if walk[i] in self.ascenders and walk[i+1] <= walk[i]:
                return i+1
        return None

class DescenderRule(Rule):
    def __init__(self, descenders):
        self.descenders = descenders
    
    def apply(self, graph, walk):
        walk = [int(item) for item in walk]
        for i, v in enumerate(walk):
            if v in self.descenders:
                if any(walk[j] > v for j in range(i+1, len(walk))):
                    return False
        return True
    
    def get_violation_position(self, graph, walk):
        for i in range(len(walk) - 1):
            if walk[i] in self.descenders and walk[i+1] >= walk[i]:
                return i+1
        return None

class EvenRule(Rule):
    def __init__(self, evens):
        self.evens = evens
    
    def apply(self, graph, walk):
        walk = [int(item) for item in walk]
        for i, v in enumerate(walk):
            if v in self.evens:
                if any(walk[j] % 2 != 0 for j in range(i+1, len(walk))):
                    return False
        return True
    
    def get_violation_position(self, graph, walk):
        for i in range(len(walk) - 1):
            if walk[i] in self.evens and walk[i+1] % 2 != 0:
                return i+1
        return None

class OddRule(Rule):
    def __init__(self, odds):
        self.odds = odds
    
    def apply(self, graph, walk):
        walk = [int(item) for item in walk]
        for i, v in enumerate(walk):
            if v in self.odds:
                if any(walk[j] % 2 == 0 for j in range(i+1, len(walk))):
                    return False
        return True
    
    def get_violation_position(self, graph, walk):
        for i in range(len(walk) - 1):
            if walk[i] in self.odds and walk[i+1] % 2 == 0:
                return i+1
        return None

class EdgeExistenceRule(Rule):
    def apply(self, walk, graph):
        for i in range(len(walk) - 1):
            if not graph.has_edge(walk[i], walk[i+1]):
                return False
        return True

class RepeaterRule(Rule):
    def __init__(self, repeaters):
        self.repeaters = repeaters
    
    def apply(self, graph, walk):
        walk = [int(item) for item in walk]
        for v, k in self.repeaters.items():
            if v in walk:
                indices = [i for i, x in enumerate(walk) if x == v]
                for i in range(len(indices) - 1):
                    if indices[i+1] - indices[i] != k:
                        return False
        return True
    
    def get_violation_position(self, graph, walk):
        for v, k in self.repeaters.items():
            if v in walk:
                indices = [i for i, x in enumerate(walk) if x == v]
                for i in range(len(indices) - 1):
                    if indices[i+1] - indices[i] != k:
                        return indices[i+1]
        return None

