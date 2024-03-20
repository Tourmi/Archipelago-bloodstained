import json
from pathlib import Path
from typing import Dict, List, NamedTuple

from worlds.generic.Rules import add_rule
from BaseClasses import Item, ItemClassification, Location, MultiWorld, Region
from .Rules import BloodstainedRules
from .Items import BAEL_DEFEATED_EVENT, BloodstainedItems

class LocationData(NamedTuple):
    name : str
    id : int

class BloodstainedLocations:
    _locations : List[LocationData] = []
    _locations_dict : Dict[str, LocationData] = {}

    def get_location_name_to_id_dict(self) -> Dict[str, int]:
        return {key: value.id for key, value in self._get_locations_dict().items()}

    def create_main_region(self, player: int, world: MultiWorld, rules: BloodstainedRules) -> Region:
        menu_region = Region("Menu", player, world)

        for locationData in self._get_locations():
            location = Location(player, locationData.name, locationData.id or None, menu_region)
            if location.name == BAEL_DEFEATED_EVENT:
                completion_event = location
            rules.set_rules_for_location(location, player)
            menu_region.locations.append(location)

        completion_item = Item(BAEL_DEFEATED_EVENT, ItemClassification.progression, None, player)
        completion_event.place_locked_item(completion_item)

        return menu_region
    
    def _get_locations(self) -> List[LocationData]:
        if not self._locations:
            self._initialize_locations()

        return self._locations
    
    def _get_locations_dict(self) -> Dict[str, LocationData]:
        if not self._locations_dict:
            self._initialize_locations()

        return self._locations_dict
    
    def _initialize_locations(self) -> None:
        base_path = Path(__file__).parent
        file_path = (base_path / "data/locations.json").resolve()
        with open(file_path) as file:
            locations : Dict = json.load(file)
            self._locations = [LocationData(name, value["id"]) for name, value in locations.items()]
        self._locations_dict = {location.name: location for location in self._locations}