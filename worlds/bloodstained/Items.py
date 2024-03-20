import json

from typing import Dict, List, NamedTuple
from pathlib import Path

from BaseClasses import Item, ItemClassification

BAEL_DEFEATED_EVENT : str = "Bael Defeated"

class ItemData(NamedTuple):
    name: str
    id: int
    is_shard: bool
    classification: ItemClassification

class BloodstainedItems:
    _items : List[ItemData] = []
    _items_dict: Dict[str, ItemData] = {}

    def get_item_name_to_id_dict(self) -> Dict[str, int]:
        return {key: value.id for key, value in self._get_items_dict().items()}

    def generate_item(self, name: str, player: int) -> Item:
        items = self._get_items_dict()
        return Item(name, items[name].classification, items[name].id, player)

    def _get_items(self) -> List[ItemData]:
        if not self._items:
            self._initialize_items()

        return self._items
    
    def _get_items_dict(self) -> Dict[str, ItemData]:
        if not self._items_dict:
            self._initialize_items()

        return self._items_dict

    def _initialize_items(self) -> None:
        base_path = Path(__file__).parent
        file_path = (base_path / "data/items.json").resolve()
        with open(file_path) as file:
            items : Dict = json.load(file)
            self._items = [ItemData(name, value["id"], value["is_shard"], ItemClassification[value["classification"]]) for name, value in items.items()]
        self._items_dict = {item.name: item for item in self._items}
