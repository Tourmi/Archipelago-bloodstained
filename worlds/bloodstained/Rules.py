import json
from pathlib import Path
from typing import Dict, List, NamedTuple
from worlds.generic.Rules import add_rule, set_rule

from BaseClasses import CollectionState, Location


class Requirement(NamedTuple):
    required_items: List[str]

class RuleData(NamedTuple):
    location_name: str
    possibilities: List[Requirement]

class BloodstainedRules:
    _rules : List[RuleData] = []
    _rules_dict : Dict[str, RuleData] = {}

    def set_rules_for_location(self, location: Location, player: int) -> None:
        if not location.name in self._get_rules_dict():
            return
        
        set_rule(location, lambda _: False)

        for requirement in self._get_rules_dict()[location.name].possibilities:
            add_rule(location, lambda state: _has_all_items(state, player, requirement), "or")

    def _get_rules(self) -> List[RuleData]:
        if not self._rules:
            self._initialize_rules()
        return self._rules

    def _get_rules_dict(self) -> Dict[str, RuleData]:
        if not self._rules_dict:
            self._initialize_rules()
        return self._rules_dict

    def _initialize_rules(self) -> None:
        base_path = Path(__file__).parent
        file_path = (base_path / "data/default_rules.json").resolve()
        with open(file_path) as file:
            rules: Dict = json.load(file)
            self._rules = [RuleData(ruleName, [Requirement(requirement["required_items"]) for requirement in requirements]) for ruleName, requirements in rules.items()]
        self._rules_dict = {rule.location_name: rule for rule in self._rules}


def _has_all_items(state : CollectionState, player: int, requirement: Requirement) -> bool:
    for required_item in requirement.required_items:
        if not state.has(required_item, player):
            return False
    
    return True