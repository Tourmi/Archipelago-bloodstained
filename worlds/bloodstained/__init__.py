import settings
import typing

from typing import Dict
from BaseClasses import Item, Location, MultiWorld, Tutorial, ItemClassification
from .Rules import BloodstainedRules
from .Options import BloodstainedOptions
from .Locations import BloodstainedLocations
from .Items import BAEL_DEFEATED_EVENT, BloodstainedItems

from ..AutoWorld import World, WebWorld

class BloodstainedSettings(settings.Group):
    pass

class BloodstainedWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up a Bloodstained Archipelago multiworld.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Tourmi"])]

class BloodstainedWorld(World):
    """
    Bloostained: Ritual of the Night
    """
    game = "Bloodstained Ritual of the Night"
    topology_present = False
    settings:typing.ClassVar[BloodstainedSettings]
    settings_key = "bloodstained_options"
    options_dataclass = BloodstainedOptions
    options: BloodstainedOptions

    bloodstained_items = BloodstainedItems()
    bloodstained_locations = BloodstainedLocations()
    bloodstained_rules = BloodstainedRules()
    item_name_groups = {}
    item_name_to_id = bloodstained_items.get_item_name_to_id_dict()
    location_name_to_id = bloodstained_locations.get_location_name_to_id_dict()

    web = BloodstainedWeb()

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        # TODO: Validate YAMLs
        pass

    def create_regions(self) -> None:
        self.multiworld.regions += [self.bloodstained_locations.create_main_region(self.player, self.multiworld, self.bloodstained_rules)]

    def create_item(self, name: str) -> Item:
        return self.bloodstained_items.generate_item(name, self.player)
    
    def create_items(self) -> None:
        self.multiworld.itempool += [self.create_item(name) for name in self.bloodstained_items.get_item_name_to_id_dict().keys() if name != BAEL_DEFEATED_EVENT]

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has(BAEL_DEFEATED_EVENT, self.player)

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        return slot_data
    
    def get_filler_item_name(self) -> str:
        return "item5"