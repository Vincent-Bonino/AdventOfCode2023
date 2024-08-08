from dataclasses import dataclass
from enum import Enum
from typing import *

from tqdm import tqdm


class Action(Enum):
    ACCEPT = "A"
    REJECT = "R"

def always_true(_mp: 'MachinePart') -> bool:
    return True

@dataclass
class MachinePart:
    a: int
    m: int
    s: int
    x: int

    @classmethod
    def parse_machine_part(cls, line: str) -> 'MachinePart':
        line = line[1:-1]  # Remove { } and the start and end of the line

        kwargs: Dict[str, int] = {}
        for val_str in line.split(","):
            field, _sep, value = val_str.partition("=")
            kwargs[field] = int(value)
        
        return MachinePart(**kwargs)


class Rule:
    condition: Callable[[MachinePart], bool]
    destination: str

    type: str  # lower or higher
    field: str
    value: int

    __repr: str

    def __init__(self, line: str) -> None:
        if not ":" in line:
            # At the end of a workflow
            self.condition = always_true
            self.destination = line
            self.__repr = "True"
        else:
            # Normal condition
            cond, _sep, dest = line.partition(":")
            self.destination = dest
            self.__repr = cond

            if "<" in cond:
                field, _sep, val = cond.partition("<")
                self.condition = lambda mp: getattr(mp, field) < int(val)
                self.type = "lower_than"
                self.field = field
                self.value = int(val)
            elif ">" in cond:
                field, _sep, val = cond.partition(">")
                self.condition = lambda mp: getattr(mp, field) > int(val)
                self.type = "higher_than"
                self.field = field
                self.value = int(val)
            else:
                raise ValueError(f"Unknown rule format: {line}")

    def __repr__(self) -> str:
        return self.__repr

    def test(self, item: MachinePart) -> Optional[str]:
        """Test a MachinePart against this rule.
        
        Returns
        -------
        Optional[str]
            Destination if the condition is True on the item. Destination can be a workflow name / R / A

        """
        return self.destination if self.condition(item) is True else None

    def opposite(self) -> 'Rule':
        """Must only be called on non-trivial rules."""
        new_rule: Rule = Rule(self.destination)
        new_rule.field = self.field
        if self.type == "lower_than":
            new_rule.type = "higher_than"
            new_rule.value = self.value - 1
            new_rule.__repr = self.__repr.replace("<", ">=")
        elif self.type == "higher_than":
            new_rule.type = "lower_than"
            new_rule.value = self.value + 1
            new_rule.__repr = self.__repr.replace(">", "<=")
        return new_rule

class Workflow:
    name: str
    rules: List[Rule]

    def __init__(self, name: str, line: str) -> None:
        self.rules = []
        self.name = name

        # Build rules
        for rule_str in line.split(","):
            self.rules.append(Rule(rule_str))

    def test(self, item: MachinePart) -> str:
        destination: Optional[str] = None
        for rule in self.rules:
            destination = rule.test(item)
            if destination is not None:
                return destination

        # Failed to find a matching rule
        raise ValueError(f"[WF{self.name}] Unable to find a matching rule for item {item}")


class System:
    action_values: List[str] = [x.value for x in Action]

    workflows: Dict[str, Workflow]
    accepted_pieces: List[MachinePart]

    def __init__(self) -> None:
        self.workflows = {}
        self.accepted_pieces = []

    def register_workflow(self, line: str) -> None:
        name, _sep, rest = line.partition("{")
        rules_str: str = rest[:-1]  # Remove the trailing }

        self.workflows[name] = Workflow(name, rules_str)

    def process_machine_part(self, item: MachinePart) -> None:
        next_action: str = "in"  # Name of the next workflow to apply or action
        while next_action not in self.action_values:
            next_workflow: Workflow = self.workflows[next_action]
            next_action = next_workflow.test(item)

        # We now know what to do with this piece
        action: Action = Action(next_action)
        if action is Action.ACCEPT:
            self.accepted_pieces.append(item)

    def compute_total_raiting(self) -> int:
        return sum(mp.a + mp.m + mp.s + mp.x for mp in self.accepted_pieces)


class TreeNode:
    accepted_nodes: List['TreeNode'] = []  # Class atrribute

    workflow_name: str  # Name of the child workflow (self)
    rule: Optional[Rule]  # Condition to go from parent to this node

    parent: Optional['TreeNode']
    children: List['TreeNode']

    def __init__(self, system: System, workflow_name: str, rule: Optional[Rule] = None, parent: Optional['TreeNode'] = None) -> None:
        self.workflow_name = workflow_name
        self.rule = rule
        self.parent = parent
        self.children = []

        if self.workflow_name == Action.ACCEPT.value:
            # A
            TreeNode.accepted_nodes.append(self)
        elif self.workflow_name == Action.REJECT.value:
            # R
            return
        else:
            # WF name
            for rule in system.workflows[self.workflow_name].rules:
                self.children.append(TreeNode(system, rule.destination, rule, parent=self))

    @property
    def brothers(self) -> List['TreeNode']:
        if self.parent is None:
            return []
        return [x for x in self.parent.children if x is not self]

    @property
    def previous_brothers(self) -> List['TreeNode']:
        if self.parent is None:
            return []
        result: List['TreeNode'] = []
        for bro in self.parent.children:
            if bro is self:
                break
            result.append(bro)
        return result

    def build_combined_rule(self) -> List[Rule]:
        result: List[Rule] = []
        if self.parent is not None and self.rule is not None:
            if self.rule.condition is always_true:
                # End node, if any other brother matched
                for b_rule in [bro.rule for bro in self.brothers if bro.rule is not None]:
                    result.append(b_rule.opposite())
            else:
                # Take previous brothers into account: their rule does not match
                for b_rule in [bro.rule for bro in self.previous_brothers if bro.rule is not None]:
                    result.append(b_rule.opposite())
                result.append(self.rule)

        return result

    def __repr__(self) -> str:
        return f"Node(wf={self.workflow_name}, rule={self.rule})"


def part_one() -> int:
    system: System = System()

    registering_workflows: bool = True
    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            line = line.strip()

            # Change from Workflows to MachineParts
            if not line:
                registering_workflows = False
                continue

            # Register Workflow
            if registering_workflows:
                system.register_workflow(line)
                continue

            # Test machine parts
            part: MachinePart = MachinePart.parse_machine_part(line)
            system.process_machine_part(part)
    
    # All done, now compute the result
    return system.compute_total_raiting()


def compute_possibility_range_from_rules(rules: List[Rule]) -> int:
    min_field_value: int = 0
    max_field_value: int = 4000 + 1

    extrema: Dict[str, Dict[str, int]] = {
    "x": {"lower_than": max_field_value, "higher_than": min_field_value},
    "m": {"lower_than": max_field_value, "higher_than": min_field_value},
    "a": {"lower_than": max_field_value, "higher_than": min_field_value},
    "s": {"lower_than": max_field_value, "higher_than": min_field_value},
    }

    for rule in rules:
        rule_type: str = rule.type
        if rule_type == "lower_than":
            extrema[rule.field][rule_type] = min(extrema[rule.field][rule_type], rule.value)
        elif rule_type == "higher_than":
            extrema[rule.field][rule_type] = max(extrema[rule.field][rule_type], rule.value)

    # All done, now compute the result
    field_ranges: List[int] = [(val["lower_than"] - val["higher_than"] - 1) for _key, val in extrema.items()]
    total: int = 1
    for rnge in field_ranges:
        total *= rnge
    return total

def part_two() -> int:
    system: System = System()

    with open("input.txt", mode='r') as f_input:
        for line in f_input.readlines():
            line = line.strip()

            # Change from Workflows to MachineParts
            if not line:
                break

            # Register Workflow
            system.register_workflow(line)

    # Build a tree of workflows
    root_node: TreeNode = TreeNode(system, "in")  # Builds the tree

    sub_totals: List[int] = []  # Possibility number for each end node
    for end_node in TreeNode.accepted_nodes:

        end_node_rules: List[Rule] = []
        current_node: Optional[TreeNode] = end_node
        while current_node is not None:
            end_node_rules.extend(current_node.build_combined_rule())
            current_node = current_node.parent
        
        sub_totals.append(compute_possibility_range_from_rules(end_node_rules))

    return sum(sub_totals)

print("Part one:", part_one())
print("Part two:", part_two())
