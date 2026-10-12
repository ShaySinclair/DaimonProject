#TO DO:
#1. Replace all to_dict with
#  def new_to_dict(self) -> dict:
#        return asdict(self)

#2. Delete all from_dict and use kwargs in load functions instead
# FROM
# item_template_global = [ItemTemplate.from_dict(d) for d in item_template_data]
# TO
# item_template_global = [ItemTemplate(**d) for d in item_template_data]

#3. Replace all JSON files with database connections.

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
import random
import sqlalchemy
import time
from typing import Dict, List, Optional, Union


ITEM_TEMPLATE_DATA_FILE               = Path(__file__).parent / "item_template_data.json"
ITEM_DATA_FILE                        = Path(__file__).parent / "item_data.json"                         # Needs ITEM_TEMPLATE_DATA_FILE

WEATHER_TEMPLATE_DATA_FILE            = Path(__file__).parent / "weather_template_data.json"
WEATHER_DATA_FILE                     = Path(__file__).parent / "weather_data.json"                      # Needs WEATHER_TEMPLATE_DATA_FILE
BIOME_DATA_FILE                       = Path(__file__).parent / "biome_data.json"                        # Needs WEATHER_DATA_FILE
LOCATION_DATA_FILE                    = Path(__file__).parent / "location_data.json"                     # Needs ITEM_DATA_FILE, DAIMON_TEMPLATE_DATA_FILE, WEATHER_DATA_FILE, BIOME_DATA_FILE

INTERACTIBLE_DATA_FILE                = Path(__file__).parent / "interactible_data.json"                 # Needs LOCATION_DATA_FILE

DAIMON_STATUS_TEMPLATE_DATA_FILE      = Path(__file__).parent / "daimon_status_template_data.json"
DAIMON_STATUS_DATA_FILE               = Path(__file__).parent / "daimon_status_data.json"
DAIMON_TYPE_DATA_FILE                 = Path(__file__).parent / "daimon_type_data.json"
DAIMON_ABILITY_DATA_FILE              = Path(__file__).parent / "daimon_ability_data.json"
DAIMON_MOVE_TEMPLATE_DATA_FILE        = Path(__file__).parent / "daimon_move_template_data.json"         # Needs DAIMON_TYPE_DATA_FILE
DAIMON_MOVE_DATA_FILE                 = Path(__file__).parent / "daimon_move_data.json"                  # Needs DAIMON_TYPE_DATA_FILE, DAIMON_TEMPLATE_DATA_FILE
DAIMON_TEMPLATE_DATA_FILE             = Path(__file__).parent / "daimon_template_data.json"              # Needs DAIMON_TYPE_DATA_FILE, DAIMON_ABILITY_DATA_FILE, DAIMON_MOVE_DATA_FILE, ITEM_DATA_FILE

DAIMON_UNBONDED_DATA_FILE             = Path(__file__).parent / "daimon_unbonded_data.json"
DAIMON_BONDED_DATA_FILE               = Path(__file__).parent / "daimon_bonded_data.json"

QUEST_STEP_TEMPLATE_DATA_FILE         = Path(__file__).parent / "quest_step_template_data.json"
QUEST_STEP_DATA_FILE                  = Path(__file__).parent / "quest_step_data.json"
QUEST_TYPE_DATA_FILE                  = Path(__file__).parent / "quest_type_data.json"
QUEST_SIDE_DATA_FILE                  = Path(__file__).parent / "quest_side_data.json"
QUEST_MAIN_DATA_FILE                  = Path(__file__).parent / "quest_main_data.json"

NPC_ITEM_INVENTORY_DATA_FILE          = Path(__file__).parent / "npc_item_inventory_data.json"           # Needs ITEM_TEMPLATE_DATA_FILE, ITEM_DATA_FILE
NPC_DAIMON_DEX_ENTRY_DATA_FILE        = Path(__file__).parent / "npc_daimon_dex_entry_data.json"         # Needs DAIMON_TEMPLATE_DATA_FILE, LOCATION_DATA_FILE
NPC_DAIMON_DEX_DATA_FILE              = Path(__file__).parent / "npc_daimon_dex_data.json"               # Needs NPC_DAIMON_DEX_ENTRY_DATA_FILE
NPC_DAIMON_INVENTORY_DATA_FILE        = Path(__file__).parent / "npc_daimon_inventory_data.json"         # Needs DAIMON_TYPE_DATA_FILE, DAIMON_ABILITY_DATA_FILE, DAIMON_MOVE_DATA_FILE, DAIMON_TEMPLATE_DATA_FILE
NPC_QUEST_MAIN_INVENTORY_DATA_FILE    = Path(__file__).parent / "npc_quest_main_inventory_data.json"     # Needs QUEST_STEP_TEMPLATE_DATA_FILE, QUEST_STEP_DATA_FILE, QUEST_MAIN_DATA_FILE
NPC_QUEST_SIDE_INVENTORY_DATA_FILE    = Path(__file__).parent / "npc_quest_side_inventory_data.json"     # Needs QUEST_STEP_TEMPLATE_DATA_FILE, QUEST_STEP_DATA_FILE, QUEST_SIDE_DATA_FILE
NPC_DATA_FILE                         = Path(__file__).parent / "npc_data.json"

PLAYER_ITEM_INVENTORY_DATA_FILE       = Path(__file__).parent / "player_item_inventory_data.json"        # Needs ITEM_TEMPLATE_DATA_FILE, ITEM_DATA_FILE
PLAYER_DAIMON_DEX_ENTRY_DATA_FILE     = Path(__file__).parent / "player_daimon_dex_entry_data.json"      # Needs DAIMON_TEMPLATE_DATA_FILE, LOCATION_DATA_FILE
PLAYER_DAIMON_DEX_DATA_FILE           = Path(__file__).parent / "player_daimon_dex_data.json"            # Needs PLAYER_DAIMON_DEX_ENTRY_DATA_FILE
PLAYER_DAIMON_INVENTORY_DATA_FILE     = Path(__file__).parent / "player_daimon_inventory_data.json"      # Needs DAIMON_TYPE_DATA_FILE, DAIMON_ABILITY_DATA_FILE, DAIMON_MOVE_DATA_FILE, DAIMON_TEMPLATE_DATA_FILE
PLAYER_QUEST_MAIN_INVENTORY_DATA_FILE = Path(__file__).parent / "player_quest_main_inventory_data.json"  # Needs QUEST_STEP_TEMPLATE_DATA_FILE, QUEST_STEP_DATA_FILE, QUEST_MAIN_DATA_FILE
PLAYER_QUEST_SIDE_INVENTORY_DATA_FILE = Path(__file__).parent / "player_quest_side_inventory_data.json"  # Needs QUEST_STEP_TEMPLATE_DATA_FILE, QUEST_STEP_DATA_FILE, QUEST_SIDE_DATA_FILE
PLAYER_DATA_FILE                      = Path(__file__).parent / "player_data.json"

SYSTEM_DAIMON_BATTLE_DATA_FILE        = Path(__file__).parent / "system_daimon_battle_data.json"

ITEM_CATEGORY_GENERIC = ["Battle", "Generic", "Key", "Move Manual"]
ITEM_CATEGORY_UNIQUE  = ["Accessory", "Badge", "Clothing", "Gemstone", "Willstone"]



@dataclass(kw_only=True)
class ItemTemplate:
    """Represents an ItemTemplate and its attributes."""

    item_template_id               : int
    item_template_name             : str
    item_template_description      : str
    item_template_category         : str
    item_template_actions          : List[Dict[str, Union[str, int]]]
    item_template_base_value       : int
    item_template_base_hex_code_1  : str
    item_template_base_hex_code_2  : Optional[str] = None
    item_template_base_hex_code_3  : Optional[str] = None
    item_template_base_hex_code_4  : Optional[str] = None
    item_template_base_hex_code_5  : Optional[str] = None
    item_template_base_hex_code_6  : Optional[str] = None
    item_template_base_hex_code_7  : Optional[str] = None
    item_template_base_hex_code_8  : Optional[str] = None
    item_template_base_hex_code_9  : Optional[str] = None
    item_template_base_hex_code_10 : Optional[str] = None

    # --------------------------------------------------
    # Create ItemTemplate object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "ItemTemplate":
        return cls(
            item_template_id               = d.get("item_template_id"),
            item_template_name             = d.get("item_template_name"),
            item_template_description      = d.get("item_template_description"),
            item_template_category         = d.get("item_template_category"),
            item_template_actions          = d.get("item_template_actions"),
            item_template_base_value       = d.get("item_template_base_value"),
            item_template_base_hex_code_1  = d.get("item_template_base_hex_code_1"),
            item_template_base_hex_code_2  = d.get("item_template_base_hex_code_2"),
            item_template_base_hex_code_3  = d.get("item_template_base_hex_code_3"),
            item_template_base_hex_code_4  = d.get("item_template_base_hex_code_4"),
            item_template_base_hex_code_5  = d.get("item_template_base_hex_code_5"),
            item_template_base_hex_code_6  = d.get("item_template_base_hex_code_6"),
            item_template_base_hex_code_7  = d.get("item_template_base_hex_code_7"),
            item_template_base_hex_code_8  = d.get("item_template_base_hex_code_8"),
            item_template_base_hex_code_9  = d.get("item_template_base_hex_code_9"),
            item_template_base_hex_code_10 = d.get("item_template_base_hex_code_10")
        )
    
    # --------------------------------------------------
    # Convert ItemTemplate object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "item_template_id"               : self.item_template_id,
            "item_template_name"             : self.item_template_name,
            "item_template_description"      : self.item_template_description,
            "item_template_category"         : self.item_template_category,
            "item_template_actions"          : self.item_template_actions,
            "item_template_base_value"       : self.item_template_base_value,
            "item_template_base_hex_code_1"  : self.item_template_base_hex_code_1,
            "item_template_base_hex_code_2"  : self.item_template_base_hex_code_2,
            "item_template_base_hex_code_3"  : self.item_template_base_hex_code_3,
            "item_template_base_hex_code_4"  : self.item_template_base_hex_code_4,
            "item_template_base_hex_code_5"  : self.item_template_base_hex_code_5,
            "item_template_base_hex_code_6"  : self.item_template_base_hex_code_6,
            "item_template_base_hex_code_7"  : self.item_template_base_hex_code_7,
            "item_template_base_hex_code_8"  : self.item_template_base_hex_code_8,
            "item_template_base_hex_code_9"  : self.item_template_base_hex_code_9,
            "item_template_base_hex_code_10" : self.item_template_base_hex_code_10,
        }

@dataclass(kw_only=True)
class Item:
    """Represents an Item and its attributes."""

    item_id          : int
    item_name        : str
    item_description : str
    item_category    : str
    item_actions     : List[Dict[str, Union[str, int]]]
    item_base_value  : int
    item_hex_code_1  : str
    item_hex_code_2  : str
    item_hex_code_3  : str
    item_hex_code_4  : str
    item_hex_code_5  : str
    item_hex_code_6  : str
    item_hex_code_7  : str
    item_hex_code_8  : str
    item_hex_code_9  : str
    item_hex_code_10 : str
    item_quantity    : int
    
    # --------------------------------------------------
    # Create Item object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "Item":
        return cls(
            item_id          = d.get("item_id"),
            item_name        = d.get("item_name"),
            item_description = d.get("item_description"),
            item_category    = d.get("item_category"),
            item_actions     = d.get("item_actions"),
            item_base_value  = d.get("item_base_value"),
            item_hex_code_1  = d.get("item_hex_code_1"),
            item_hex_code_2  = d.get("item_hex_code_2"),
            item_hex_code_3  = d.get("item_hex_code_3"),
            item_hex_code_4  = d.get("item_hex_code_4"),
            item_hex_code_5  = d.get("item_hex_code_5"),
            item_hex_code_6  = d.get("item_hex_code_6"),
            item_hex_code_7  = d.get("item_hex_code_7"),
            item_hex_code_8  = d.get("item_hex_code_8"),
            item_hex_code_9  = d.get("item_hex_code_9"),
            item_hex_code_10 = d.get("item_hex_code_10"),
            item_quantity    = d.get("item_quantity")
        )
    
    # --------------------------------------------------
    # Convert Item object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "item_id"          : self.item_id,
            "item_name"        : self.item_name,
            "item_description" : self.item_description,
            "item_category"    : self.item_category,
            "item_actions"     : self.item_actions,
            "item_base_value"  : self.item_base_value,
            "item_hex_code_1"  : self.item_hex_code_1,
            "item_hex_code_2"  : self.item_hex_code_2,
            "item_hex_code_3"  : self.item_hex_code_3,
            "item_hex_code_4"  : self.item_hex_code_4,
            "item_hex_code_5"  : self.item_hex_code_5,
            "item_hex_code_6"  : self.item_hex_code_6,
            "item_hex_code_7"  : self.item_hex_code_7,
            "item_hex_code_8"  : self.item_hex_code_8,
            "item_hex_code_9"  : self.item_hex_code_9,
            "item_hex_code_10" : self.item_hex_code_10,
            "item_quantity"    : self.item_quantity
        }

@dataclass(kw_only=True)
class DaimonType:
    """Represents a DaimonType and its attributes."""

    daimon_type_id            : int        # Unique ID for this type (e.g., 15)
    daimon_type_name          : str        # Human-readable name (e.g., "Metal")
    daimon_type_advantages    : List[int]  # List of daimon_type_id's this type is strong against
    daimon_type_disadvantages : List[int]  # List of daimon_type_id's this type is weak against
    daimon_type_immunities    : List[int]  # List of daimon_type_id's this type is immune against

    # --------------------------------------------------
    # Create DaimonType object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "DaimonType":
        return cls(
            daimon_type_id            = d["daimon_type_id"],
            daimon_type_name          = d["daimon_type_name"],
            daimon_type_advantages    = d["daimon_type_advantages"],
            daimon_type_disadvantages = d["daimon_type_disadvantages"],
            daimon_type_immunities    = d.get("daimon_type_immunities")
        )
    
    @staticmethod
    def resolve_daimon_type_relationships():
        for daimon_type in daimon_type_global:
            daimon_type.daimon_type_advantages    = [get_daimon_type_by_id(i) for i in daimon_type.daimon_type_advantages]
            daimon_type.daimon_type_disadvantages = [get_daimon_type_by_id(i) for i in daimon_type.daimon_type_disadvantages]
            daimon_type.daimon_type_immunities    = [get_daimon_type_by_id(i) for i in daimon_type.daimon_type_immunities]

@dataclass(kw_only=True)
class DaimonStatusTemplate:
    """Represents a DaimonStatusTemplate and its attributes."""

    daimon_status_template_id : int
    daimon_status_template_name: str
    daimon_status_template_description: str
    daimon_status_template_effect: List[Dict[str, float]]
    daimon_status_template_duration_max: int

    # --------------------------------------------------
    # Create DaimonStatusTemplate object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "DaimonStatus":
        return cls(
            daimon_status_template_id           = d["daimon_status_template_id"],
            daimon_status_template_name         = d["daimon_status_template_name"],
            daimon_status_template_description  = d["daimon_status_template_description"],
            daimon_status_template_effect       = d["daimon_status_template_effect"],
            daimon_status_template_duration_max = d["daimon_status_template_duration_max"],
        )
    
@dataclass(kw_only=True)
class DaimonStatus:
    """Represents a DaimonStatus and its attributes."""

    daimon_status_id               : int
    daimon_status_name             : str
    daimon_status_description      : str
    daimon_status_effect           : List[Dict[str, float]]
    daimon_status_duration_max     : int
    daimon_status_duration_current : int

    # --------------------------------------------------
    # Create DaimonStatus object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "DaimonStatus":
        return cls(
            daimon_status_id               = d["daimon_status_id"],
            daimon_status_name             = d["daimon_status_name"],
            daimon_status_description      = d["daimon_status_description"],
            daimon_status_effect           = d["daimon_status_effect"],
            daimon_status_duration_max     = d["daimon_status_duration_max"],
            daimon_status_duration_current = d["daimon_status_duration_current"]
        )
    
    # --------------------------------------------------
    # Convert DaimonStatus object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "daimon_status_id"               : self.daimon_status_id,
            "daimon_status_name"             : self.daimon_status_name,
            "daimon_status_description"      : self.daimon_status_description,
            "daimon_status_effect"           : self.daimon_status_effect,
            "daimon_status_duration_max"     : self.daimon_status_duration_max,
            "daimon_status_duration_current" : self.daimon_status_duration_current
        }

@dataclass(kw_only=True)
class DaimonAbility:
    """Represents a DaimonAbility and its attributes."""

    daimon_ability_id          : int                   # Unique ID for this ability (e.g., 4)
    daimon_ability_name        : str                   # Human-readable name (e.g., "Second Wind")
    daimon_ability_description : str                   # Human-readable description (e.g., "The Daimon heals to 75% of maximum health and raises Physical Attack by 1 stage after being non-fatally hit to below 50% of maximum health.")
    daimon_ability_effect      : List[Dict[int, int]]  # ADD EFFECTS HERE

    # --------------------------------------------------
    # Create DaimonAbility object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "DaimonAbility":
        return cls(
            daimon_ability_id          = d["daimon_ability_id"],
            daimon_ability_name        = d["daimon_ability_name"],
            daimon_ability_description = d["daimon_ability_description"],
            daimon_ability_effect      = d["daimon_ability_effect"]
        )

@dataclass(kw_only=True)
class DaimonMoveTemplate:
    """Represents a DaimonMoveTemplate and its attributes."""

    daimon_move_template_id                 : int  # Unique ID for this move (e.g., 15)
    daimon_move_template_name               : str  # Human-readable name (e.g., "Metal Claw")
    daimon_move_template_type               : DaimonType # Unique ID for Daimon types (e.g. 3)
    daimon_move_template_description        : str  # Human-readable description (e.g., "The target is raked with steel claws. There is a 10% chance to raise the user’s Physical Attack by 1 stage.")
    daimon_move_template_category           : str  # Human-readable category (e.g., "Physical")
    daimon_move_template_power              : int  # Base damage for this move (e.g., 50)
    daimon_move_template_accuracy           : float  # Base accuracy for this move (e.g., 0.95)
    daimon_move_template_points_base        : int  # Base uses for this move (e.g., 35)
    daimon_move_template_points_max         : int  # Maximum uses for this move (e.g., 45)
    daimon_move_template_effect_status      : List[Dict[str, Union[DaimonStatusTemplate, float, str]]]  # Additional effects for this move (e.g., [{0.1, "Physical Attack", 1}])
    daimon_move_template_effect_stat_change : List[Dict[str, Union[str, int, float]]]  # Additional effects for this move (e.g., [{0.1, "Physical Attack", 1}])

    # --------------------------------------------------
    # Create DaimonMoveTemplate object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "DaimonMoveTemplate":
        return cls(
            daimon_move_template_id                 = d["daimon_move_template_id"],
            daimon_move_template_name               = d["daimon_move_template_name"],
            daimon_move_template_type               = get_daimon_type_by_id(d["daimon_move_template_type_id"]),
            daimon_move_template_description        = d["daimon_move_template_description"],
            daimon_move_template_category           = d["daimon_move_template_category"],
            daimon_move_template_power              = d["daimon_move_template_power"],
            daimon_move_template_accuracy           = d["daimon_move_template_accuracy"],
            daimon_move_template_points_base        = d["daimon_move_template_points_base"],
            daimon_move_template_points_max         = d["daimon_move_template_points_max"],
            daimon_move_template_effect_status      = [
                {
                    "daimon_move_template_status": get_daimon_status_template_by_id(daimon_move_template_effect_status.get("daimon_status_template_id", None)),
                    "daimon_move_template_status_weight": daimon_move_template_effect_status.get("daimon_status_template_weight", None),
                    "daimon_move_template_status_target": daimon_move_template_effect_status.get("daimon_status_template_target", None)
                }
                for daimon_move_template_effect_status in d.get("daimon_move_template_effect_status", None)
            ],
            daimon_move_template_effect_stat_change = d.get("daimon_move_template_effect_stat_change", None)
        )
    
@dataclass(kw_only=True)
class DaimonMove:
    """Represents a DaimonMove and its attributes."""

    daimon_move_id                 : int  # Unique ID for this move (e.g., 15)
    daimon_move_name               : str  # Human-readable name (e.g., "Metal Claw")
    daimon_move_type               : DaimonType # Unique ID for Daimon types (e.g. 3)
    daimon_move_description        : str  # Human-readable description (e.g., "The target is raked with steel claws. There is a 10% chance to raise the user’s Physical Attack by 1 stage.")
    daimon_move_category           : str  # Human-readable category (e.g., "Physical")
    daimon_move_power              : int  # Base damage for this move (e.g., 50)
    daimon_move_accuracy           : float  # Base accuracy for this move (e.g., 0.95)
    daimon_move_points_base        : int  # Maximum uses for this move (e.g., 35)
    daimon_move_points_max         : int  # Maximum uses for this move (e.g., 35)
    daimon_move_points_current     : int  # Current uses for this move (e.g., 35)
    daimon_move_effect_status      : List[Dict[DaimonStatus, Union[float, str]]]  # Additional effects for this move (e.g., [{0.1, "Physical Attack", 1}])
    daimon_move_effect_stat_change : List[Dict[str, Union[str, int, float]]]

    # --------------------------------------------------
    # Create DaimonMove object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "DaimonMove":
        return cls(
            daimon_move_id                 = d["daimon_move_id"],
            daimon_move_name               = d["daimon_move_name"],
            daimon_move_type               = d["daimon_move_type"],
            daimon_move_description        = d["daimon_move_description"],
            daimon_move_category           = d["daimon_move_category"],
            daimon_move_power              = d["daimon_move_power"],
            daimon_move_accuracy           = d["daimon_move_accuracy"],
            daimon_move_points_base        = d["daimon_move_points_base"],
            daimon_move_points_max         = d["daimon_move_points_max"],
            daimon_move_points_current     = d["daimon_move_points_current"],
            daimon_move_effect_status      = d["daimon_move_effect_status"],
            daimon_move_effect_stat_change = d.get("daimon_move_effect_stat_change")
        )
    
    # --------------------------------------------------
    # Convert DaimonMove object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "daimon_move_id"                 : self.daimon_move_id,
            "daimon_move_name"               : self.daimon_move_name,
            "daimon_move_type"               : self.daimon_move_type,
            "daimon_move_description"        : self.daimon_move_description,
            "daimon_move_category"           : self.daimon_move_category,
            "daimon_move_power"              : self.daimon_move_power,
            "daimon_move_accuracy"           : self.daimon_move_accuracy,
            "daimon_move_points_base"        : self.daimon_move_points_base,
            "daimon_move_points_max"         : self.daimon_move_points_max,
            "daimon_move_points_current"     : self.daimon_move_points_current,
            "daimon_move_effect_status"      : self.daimon_move_effect_status,
            "daimon_move_effect_stat_change" : self.daimon_move_effect_stat_change,
        }

@dataclass(kw_only=True)
class DaimonTemplate:
    """
    Represents a DaimonTemplate and its attributes.
    """

    daimon_template_id                         : int                                # Unique Daimon Template ID                     # Example: 1
    daimon_template_species                    : str                                # Unique Daimon Template Species                # Example: "Palanine"
    daimon_template_evolution_1                : List[Dict[str, Union[int, Item]]]  # Unique Daimon Template Evolution Progression  # Example: [{"daimon_template_evolution_level": 1, "daimon_template_evolution_requirement": Item", "daimon_template_evolution_id": Item"}
    daimon_template_evolution_2                : List[Dict[str, Union[int, Item]]]  # Unique Daimon Template Evolution Progression  # Example: [{"daimon_template_evolution_level": 1, "daimon_template_evolution_requirement": Item", "daimon_template_evolution_id": Item"}
    daimon_template_evolution_3                : List[Dict[str, Union[int, Item]]]  # Unique Daimon Template Evolution Progression  # Example: [{"daimon_template_evolution_level": 1, "daimon_template_evolution_requirement": Item", "daimon_template_evolution_id": Item"}
    daimon_template_gender_distribution        : Dict[str, float]                   # Daimon Template Gender Distribution           # Example: {"Male": 0.5, "Female": 0.5},
    daimon_template_height_distribution        : Dict[str, float]                   # Daimon Template Weight Distribution           # Example: {"daimon_template_height_mean": 0.75, "daimon_template_height_range": 0.15},
    daimon_template_weight_distribution        : Dict[str, float]                   # Daimon Template Height Distribution           # Example: {"daimon_template_weight_mean": 15, "daimon_template_weight_range": 1.5},
    daimon_template_stat_base_health           : float                              # Daimon Template Stat Base Health              # Example: 1
    daimon_template_stat_base_physical_attack  : float                              # Daimon Template Stat Base Physical Attack     # Example: 1
    daimon_template_stat_base_special_attack   : float                              # Daimon Template Stat Base Special Attack      # Example: 1
    daimon_template_stat_base_physical_defense : float                              # Daimon Template Stat Base Physical Defense    # Example: 1
    daimon_template_stat_base_special_defense  : float                              # Daimon Template Stat Base Special Defense     # Example: 1
    daimon_template_stat_base_speed            : float                              # Daimon Template Stat Base Speed               # Example: 1
    daimon_template_type_1                     : DaimonType                         # Daimon Template Type ID 1                     # Example: DaimonType
    daimon_template_type_2                     : Optional[DaimonType]               # Daimon Template Type ID 2                     # Example: DaimonType
    daimon_template_ability_pool               : List[Dict[DaimonAbility, float]]   # Daimon Template Ability                       # Example: [{"daimon_ability_id": 1, "daimon_ability_weight": 0.7}]
    daimon_template_move_template_pool         : List[DaimonMoveTemplate]           # Daimon Template Move Template Pool            # Example: [{"daimon_template_move_template_level_requirement": 5, "daimon_move_template_id": 1}]
    daimon_template_item_template_pool         : List[Dict[ItemTemplate, float]]    # Daimon Template Item Template Pool            # Example: [{"item_weight": 0.1, ItemTemplate}]

    # --------------------------------------------------
    # Create DaimonTemplate object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "DaimonTemplate":
        return cls(
            daimon_template_id                         = d["daimon_template_id"],
            daimon_template_species                    = d["daimon_template_species"],
            daimon_template_evolution_1                = d["daimon_template_evolution_1"],
            daimon_template_evolution_2                = d["daimon_template_evolution_2"],
            daimon_template_evolution_3                = d["daimon_template_evolution_3"],
            daimon_template_gender_distribution        = d["daimon_template_gender_distribution"],
            daimon_template_height_distribution        = d["daimon_template_height_distribution"],
            daimon_template_weight_distribution        = d["daimon_template_weight_distribution"],
            daimon_template_stat_base_health           = d["daimon_template_stat_base_health"],
            daimon_template_stat_base_physical_attack  = d["daimon_template_stat_base_physical_attack"],
            daimon_template_stat_base_special_attack   = d["daimon_template_stat_base_special_attack"],
            daimon_template_stat_base_physical_defense = d["daimon_template_stat_base_physical_defense"],
            daimon_template_stat_base_special_defense  = d["daimon_template_stat_base_special_defense"],
            daimon_template_stat_base_speed            = d["daimon_template_stat_base_speed"],
            daimon_template_type_1                     = get_daimon_type_by_id(d.get("daimon_template_type_id_1")),
            daimon_template_type_2                     = get_daimon_type_by_id(d.get("daimon_template_type_id_2")),
            daimon_template_ability_pool               = [
                {
                    "daimon_ability_weight": daimon_template_ability.get("daimon_ability_weight"),
                    "daimon_ability": get_daimon_ability_by_id(daimon_template_ability.get("daimon_ability_id"))
                }
                for daimon_template_ability in d["daimon_template_ability_pool"]
            ],
            daimon_template_move_template_pool         = [
                {
                    "daimon_template_move_template_level_requirement": daimon_template_move_template.get("daimon_template_move_template_level_requirement"),
                    "daimon_template_move_template": get_daimon_move_template_by_id(daimon_template_move_template.get("daimon_move_template_id"))
                }
                for daimon_template_move_template in d["daimon_template_move_template_pool"]
            ],
            daimon_template_item_template_pool         = [
                {
                    "item_template_weight": item_template["item_template_weight"],
                    "item_template": get_item_template_by_id(item_template.get("item_template_id"))
                }
                for item_template in d["daimon_template_item_template_pool"]
            ]
        )

@dataclass(kw_only=True)
class DaimonUnbonded:
    """Represents a DaimonUnbonded and its attributes."""

    daimon_unbonded_id                    : int                             # Unique Daimon Unbonded ID              # Example: 1
    daimon_unbonded_daimon_template_id    : int                             # Daimon Template ID                     # Example: 1
    daimon_unbonded_species               : str                             # Unique Daimon Unbonded Species         # Example: "Palanine"
    daimon_unbonded_level                 : int                             # Daimon Unbonded Level                  # Example: 50
    daimon_unbonded_level_progress        : float                           # Daimon Unbonded Level Progress         # Example: 0.25
    daimon_unbonded_gender                : str                             # Daimon Unbonded Gender                 # Example: "Male" 
    daimon_unbonded_height                : float                           # Daimon Unbonded Height                 # Example: 0.75
    daimon_unbonded_weight                : float                           # Daimon Unbonded Weight                 # Example: 15
    daimon_unbonded_max_health            : int                             # Daimon Unbonded Maximum Health         # Example: 200
    daimon_unbonded_current_health        : int                             # Daimon Unbonded Current Health         # Example: 200
    daimon_unbonded_status                : DaimonStatus                    # Daimon Unbonded Current Status         # Example: "Sleep"
    daimon_unbonded_stat_health           : float                           # Daimon Unbonded Stat Health            # Example: 1
    daimon_unbonded_stat_physical_attack  : float                           # Daimon Unbonded Stat Physical Attack   # Example: 1
    daimon_unbonded_stat_special_attack   : float                           # Daimon Unbonded Stat Special Attack    # Example: 1
    daimon_unbonded_stat_physical_defense : float                           # Daimon Unbonded Stat Physical Defense  # Example: 1
    daimon_unbonded_stat_special_defense  : float                           # Daimon Unbonded Stat Special Defense   # Example: 1
    daimon_unbonded_stat_speed            : float                           # Daimon Unbonded Stat Speed             # Example: 1
    daimon_unbonded_type_1                : DaimonType                      # Daimon Unbonded Type 1                 # Example: DaimonType
    daimon_unbonded_type_2                : Optional[DaimonType] = None     # Daimon Unbonded Type 2                 # Example: DaimonType
    daimon_unbonded_ability               : DaimonAbility                   # Daimon Unbonded Ability                # Example: DaimonAbility
    daimon_unbonded_move_1                : Optional[DaimonMove] = None     # Daimon Unbonded Move 1                 # Example: DaimonMove
    daimon_unbonded_move_2                : Optional[DaimonMove] = None     # Daimon Unbonded Move 2                 # Example: DaimonMove
    daimon_unbonded_move_3                : Optional[DaimonMove] = None     # Daimon Unbonded Move 3                 # Example: DaimonMove
    daimon_unbonded_move_4                : Optional[DaimonMove] = None     # Daimon Unbonded Move 4                 # Example: DaimonMove
    daimon_unbonded_item                  : Optional[Item] = None           # Daimon Unbonded Item                   # Example: Item

    # --------------------------------------------------
    # Create DaimonUnbonded object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "DaimonUnbonded":

        def load_daimon_unbonded_move(key: int):
            move_block = d.get(key)
            if move_block is None:
                return None

            daimon_move_template_id = move_block.get("daimon_move_template_id")
            daimon_move_points_current = move_block.get("daimon_move_points_current")

            daimon_move_template = get_daimon_move_template_by_id(daimon_move_template_id)

            return DaimonMove(
                daimon_move_id                 = daimon_move_template.daimon_move_template_id,
                daimon_move_name               = daimon_move_template.daimon_move_template_name,
                daimon_move_type               = daimon_move_template.daimon_move_template_type,
                daimon_move_description        = daimon_move_template.daimon_move_template_description,
                daimon_move_category           = daimon_move_template.daimon_move_template_category,
                daimon_move_power              = daimon_move_template.daimon_move_template_power,
                daimon_move_accuracy           = daimon_move_template.daimon_move_template_accuracy,
                daimon_move_points_base        = daimon_move_template.daimon_move_template_points_base,
                daimon_move_points_max         = daimon_move_template.daimon_move_template_points_max,
                daimon_move_points_current     = daimon_move_points_current,
                daimon_move_effect_status      = daimon_move_template.daimon_move_template_effect_status,
                daimon_move_effect_stat_change = daimon_move_template.daimon_move_template_effect_stat_change
            )

        daimon_unbonded_move_1 = load_daimon_unbonded_move("daimon_unbonded_move_1")
        daimon_unbonded_move_2 = load_daimon_unbonded_move("daimon_unbonded_move_2")
        daimon_unbonded_move_3 = load_daimon_unbonded_move("daimon_unbonded_move_3")
        daimon_unbonded_move_4 = load_daimon_unbonded_move("daimon_unbonded_move_4")

        def load_daimon_unbonded_status(key: int):
            status_block = d.get(key)
            if status_block is None:
                return None

            daimon_status_template_id = status_block.get("daimon_status_template_id")
            daimon_status_duration_current = status_block.get("daimon_status_duration_current")

            daimon_status_template = get_daimon_status_template_by_id(daimon_status_template_id)

            return DaimonStatus(
                daimon_status_id               = daimon_status_template.daimon_status_template_id,
                daimon_status_name             = daimon_status_template.daimon_status_template_name,
                daimon_status_description      = daimon_status_template.daimon_status_template_description,
                daimon_status_effect           = daimon_status_template.daimon_status_template_effect,
                daimon_status_duration_max     = daimon_status_template.daimon_status_template_duration_max,
                daimon_status_duration_current = daimon_status_duration_current
            )
        
        daimon_unbonded_status = load_daimon_unbonded_status("daimon_unbonded_status")

        def load_daimon_unbonded_item(key: int):
            item_block = d.get(key)
            if item_block is None:
                return None

            item_template_id = item_block.get("item_template_id")
            item_hex_code_1  = item_block.get("item_hex_code_1")
            item_hex_code_2  = item_block.get("item_hex_code_2")
            item_hex_code_3  = item_block.get("item_hex_code_3")
            item_hex_code_4  = item_block.get("item_hex_code_4")
            item_hex_code_5  = item_block.get("item_hex_code_5")
            item_hex_code_6  = item_block.get("item_hex_code_6")
            item_hex_code_7  = item_block.get("item_hex_code_7")
            item_hex_code_8  = item_block.get("item_hex_code_8")
            item_hex_code_9  = item_block.get("item_hex_code_9")
            item_hex_code_10 = item_block.get("item_hex_code_10")
            item_quantity    = item_block.get("item_quantity")

            item_template = get_item_template_by_id(item_template_id)

            return Item(
                item_id          = item_template.item_template_id,
                item_name        = item_template.item_template_name,
                item_description = item_template.item_template_description,
                item_category    = item_template.item_template_category,
                item_actions     = item_template.item_template_actions,
                item_base_value  = item_template.item_template_base_value,
                item_hex_code_1  = item_hex_code_1,
                item_hex_code_2  = item_hex_code_2,
                item_hex_code_3  = item_hex_code_3,
                item_hex_code_4  = item_hex_code_4,
                item_hex_code_5  = item_hex_code_5,
                item_hex_code_6  = item_hex_code_6,
                item_hex_code_7  = item_hex_code_7,
                item_hex_code_8  = item_hex_code_8,
                item_hex_code_9  = item_hex_code_9,
                item_hex_code_10 = item_hex_code_10,
                item_quantity    = item_quantity
            )
        
        daimon_unbonded_item = load_daimon_unbonded_item("daimon_unbonded_item")

        return cls(
            daimon_unbonded_id                    = d["daimon_unbonded_id"],
            daimon_unbonded_daimon_template_id    = d["daimon_unbonded_daimon_template_id"],
            daimon_unbonded_species               = d["daimon_unbonded_species"],
            daimon_unbonded_level                 = d["daimon_unbonded_level"],
            daimon_unbonded_level_progress        = d["daimon_unbonded_level_progress"],
            daimon_unbonded_gender                = d["daimon_unbonded_gender"],
            daimon_unbonded_height                = d["daimon_unbonded_height"],
            daimon_unbonded_weight                = d["daimon_unbonded_weight"],
            daimon_unbonded_max_health            = d["daimon_unbonded_max_health"],
            daimon_unbonded_current_health        = d["daimon_unbonded_current_health"],
            daimon_unbonded_status                = daimon_unbonded_status_id,
            daimon_unbonded_stat_health           = d["daimon_unbonded_stat_health"],
            daimon_unbonded_stat_physical_attack  = d["daimon_unbonded_stat_physical_attack"],
            daimon_unbonded_stat_special_attack   = d["daimon_unbonded_stat_special_attack"],
            daimon_unbonded_stat_physical_defense = d["daimon_unbonded_stat_physical_defense"],
            daimon_unbonded_stat_special_defense  = d["daimon_unbonded_stat_special_defense"],
            daimon_unbonded_stat_speed            = d["daimon_unbonded_stat_speed"],
            daimon_unbonded_type_1                = get_daimon_type_by_id(d.get("daimon_unbonded_type_id_1")),
            daimon_unbonded_type_2                = get_daimon_type_by_id(d.get("daimon_unbonded_type_id_2")),
            daimon_unbonded_ability               = get_daimon_ability_by_id(d["daimon_unbonded_ability_id"]),
            daimon_unbonded_move_1                = daimon_unbonded_move_1,
            daimon_unbonded_move_2                = daimon_unbonded_move_2,
            daimon_unbonded_move_3                = daimon_unbonded_move_3,
            daimon_unbonded_move_4                = daimon_unbonded_move_4,
            daimon_unbonded_item                  = daimon_unbonded_item
        )
    
    # --------------------------------------------------
    # Convert DaimonUnbonded object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        print(f'HERERERERESAW {self.daimon_unbonded_status}')
        return {
            "daimon_unbonded_id"                    : self.daimon_unbonded_id,
            "daimon_unbonded_daimon_template_id"    : self.daimon_unbonded_daimon_template_id,
            "daimon_unbonded_species"               : self.daimon_unbonded_species,
            "daimon_unbonded_level"                 : self.daimon_unbonded_level,
            "daimon_unbonded_level_progress"        : self.daimon_unbonded_level_progress,
            "daimon_unbonded_gender"                : self.daimon_unbonded_gender,
            "daimon_unbonded_height"                : self.daimon_unbonded_height,
            "daimon_unbonded_weight"                : self.daimon_unbonded_weight,
            "daimon_unbonded_max_health"            : self.daimon_unbonded_max_health,
            "daimon_unbonded_current_health"        : self.daimon_unbonded_current_health,
            "daimon_unbonded_status_id"             : self.daimon_unbonded_status.daimon_status_id,
            "daimon_unbonded_stat_health"           : self.daimon_unbonded_stat_health,
            "daimon_unbonded_stat_physical_attack"  : self.daimon_unbonded_stat_physical_attack,
            "daimon_unbonded_stat_special_attack"   : self.daimon_unbonded_stat_special_attack,
            "daimon_unbonded_stat_physical_defense" : self.daimon_unbonded_stat_physical_defense,
            "daimon_unbonded_stat_special_defense"  : self.daimon_unbonded_stat_special_defense,
            "daimon_unbonded_stat_speed"            : self.daimon_unbonded_stat_speed,
            "daimon_unbonded_type_id_1"             : self.daimon_unbonded_type_1.daimon_type_id,
            "daimon_unbonded_type_id_2"             : self.daimon_unbonded_type_2.daimon_type_id if self.daimon_unbonded_type_2 else None,
            "daimon_unbonded_ability_id"            : self.daimon_unbonded_ability.daimon_ability_id,
            "daimon_unbonded_move_1"                : {"daimon_move_template_id": self.daimon_unbonded_move_1.daimon_move_id, 
                                                       "daimon_move_points_current": self.daimon_unbonded_move_1.daimon_move_points_current} if self.daimon_unbonded_move_1 else None,
            "daimon_unbonded_move_2"                : {"daimon_move_template_id": self.daimon_unbonded_move_2.daimon_move_id, 
                                                       "daimon_move_points_current": self.daimon_unbonded_move_1.daimon_move_points_current} if self.daimon_unbonded_move_2 else None,
            "daimon_unbonded_move_3"                : {"daimon_move_template_id": self.daimon_unbonded_move_3.daimon_move_id, 
                                                       "daimon_move_points_current": self.daimon_unbonded_move_1.daimon_move_points_current} if self.daimon_unbonded_move_3 else None,
            "daimon_unbonded_move_4"                : {"daimon_move_template_id": self.daimon_unbonded_move_4.daimon_move_id, 
                                                       "daimon_move_points_current": self.daimon_unbonded_move_1.daimon_move_points_current} if self.daimon_unbonded_move_4 else None,
            "daimon_unbonded_item"                  : {"item_template_id": self.daimon_unbonded_item.item_id, 
                                                       "item_hex_code_1": self.daimon_unbonded_item.item_hex_code_1,
                                                       "item_hex_code_2": self.daimon_unbonded_item.item_hex_code_2,
                                                       "item_hex_code_3": self.daimon_unbonded_item.item_hex_code_3,
                                                       "item_hex_code_4": self.daimon_unbonded_item.item_hex_code_4,
                                                       "item_hex_code_5": self.daimon_unbonded_item.item_hex_code_5,
                                                       "item_hex_code_6": self.daimon_unbonded_item.item_hex_code_6,
                                                       "item_hex_code_7": self.daimon_unbonded_item.item_hex_code_7,
                                                       "item_hex_code_8": self.daimon_unbonded_item.item_hex_code_8,
                                                       "item_hex_code_9": self.daimon_unbonded_item.item_hex_code_9,
                                                       "item_hex_code_10": self.daimon_unbonded_item.item_hex_code_10,
                                                       "item_quantity": self.daimon_unbonded_item.item_quantity} if self.daimon_unbonded_item else None
        }
    
    def add_level_progress(self, progress: float):
        """
        Adds experience to the DaimonUnbonded's level progress.
        If level_progress reaches or exceeds 1, increases level by 1 and carries over remainder.
        If evolution is possible, prompts the player whether to evolve via input().
        """
        if progress < 0:
            raise ValueError("Progress must be non-negative.")

        self.daimon_unbonded_level_progress += progress

        # Handle level-up(s)
        while self.daimon_unbonded_level_progress >= 1.0:
            self.daimon_unbonded_level += 1
            self.daimon_unbonded_level_progress -= 1.0
            print(f"⬆️ {self.daimon_unbonded_species} leveled up! New level: {self.daimon_unbonded_level}")

            # Check for evolution
            can_evolve = False
            current_species = self.daimon_unbonded_species
            if self.try_evolve():  # Returns True if evolution possible
                can_evolve = True
                # Reset species for now; actual evolution runs after choice
                self.daimon_unbonded_species = current_species

            if can_evolve:
                self.try_evolve()

        print(f"Current level progress for {self.daimon_unbonded_species}: {round(self.daimon_unbonded_level_progress, 2)}")

    def try_evolve(self):
        """
        Checks if this DaimonUnbonded should evolve based on its level.
        If so, updates its species, types, stats, height, and weight.
        Abilities and moves are preserved.
        """
        # Get the current DaimonTemplate
        current_template = get_daimon_template_by_id(self.daimon_unbonded_daimon_template_id)
        if not current_template:
            print(f"❌ No template found for species {self.daimon_unbonded_species}.")
            return False

        # Flatten all evolution stages
        evolution_stages = (
            (current_template.daimon_template_evolution_1 or []) +
            (current_template.daimon_template_evolution_2 or []) +
            (current_template.daimon_template_evolution_3 or [])
        )

        if not evolution_stages:
            print(f"ℹ️ {self.daimon_unbonded_species} has no evolutions.")
            return False

        # Find eligible evolutions based on level and (optional) item
        for stage in evolution_stages:
            required_level = stage.get("daimon_template_evolution_level", 0)
            required_item = stage.get("daimon_template_evolution_requirement", None)
            if self.daimon_unbonded_level >= required_level:
                if required_item and (self.daimon_unbonded_item is None or self.daimon_unbonded_item.item_id != required_item.item_id):
                    continue  # Can't evolve without required item
                # Found a valid evolution
                evolved_template = get_daimon_template_by_id(stage["daimon_template_evolution_id"])
                if not evolved_template:
                    print(f"❌ Evolution template ID {stage['daimon_template_evolution_id']} not found.")
                    return False

                # --- Preserve abilities and moves ---
                ability = self.daimon_unbonded_ability
                moves = [
                    self.daimon_unbonded_move_1,
                    self.daimon_unbonded_move_2,
                    self.daimon_unbonded_move_3,
                    self.daimon_unbonded_move_4
                ]

                # --- Height & Weight ratio preservation ---
                old_height_min = current_template.daimon_template_height_distribution.get("daimon_template_height_mean", 1) - current_template.daimon_template_height_distribution.get("daimon_template_height_range", 0)
                old_height_max = current_template.daimon_template_height_distribution.get("daimon_template_height_mean", 1) + current_template.daimon_template_height_distribution.get("daimon_template_height_range", 0)
                old_height_range = old_height_max - old_height_min
                old_height_ratio = (self.daimon_unbonded_height - old_height_min) / old_height_range if old_height_range else 0.5

                new_height_mean = evolved_template.daimon_template_height_distribution.get("daimon_template_height_mean", 1)
                new_height_range = evolved_template.daimon_template_height_distribution.get("daimon_template_height_range", 0)
                new_height_min = new_height_mean - new_height_range
                new_height_max = new_height_mean + new_height_range
                self.daimon_unbonded_height = round(new_height_min + old_height_ratio * (new_height_max - new_height_min), 2)

                old_weight_min = current_template.daimon_template_weight_distribution.get("daimon_template_weight_mean", 1) - current_template.daimon_template_weight_distribution.get("daimon_template_weight_range", 0)
                old_weight_max = current_template.daimon_template_weight_distribution.get("daimon_template_weight_mean", 1) + current_template.daimon_template_weight_distribution.get("daimon_template_weight_range", 0)
                old_weight_range = old_weight_max - old_weight_min
                old_weight_ratio = (self.daimon_unbonded_weight - old_weight_min) / old_weight_range if old_weight_range else 0.5

                new_weight_mean = evolved_template.daimon_template_weight_distribution.get("daimon_template_weight_mean", 1)
                new_weight_range = evolved_template.daimon_template_weight_distribution.get("daimon_template_weight_range", 0)
                new_weight_min = new_weight_mean - new_weight_range
                new_weight_max = new_weight_mean + new_weight_range
                self.daimon_unbonded_weight = round(new_weight_min + old_weight_ratio * (new_weight_max - new_weight_min), 2)

                # --- Update species, types, and stats (scaled by current level) ---
                self.daimon_unbonded_species = evolved_template.daimon_template_species
                self.daimon_unbonded_type_1 = evolved_template.daimon_template_type_1
                self.daimon_unbonded_type_2 = evolved_template.daimon_template_type_2

                self.daimon_unbonded_stat_health = round(evolved_template.daimon_template_stat_base_health * self.daimon_unbonded_level, 2)
                self.daimon_unbonded_stat_physical_attack = round(evolved_template.daimon_template_stat_base_physical_attack * self.daimon_unbonded_level, 2)
                self.daimon_unbonded_stat_special_attack = round(evolved_template.daimon_template_stat_base_special_attack * self.daimon_unbonded_level, 2)
                self.daimon_unbonded_stat_physical_defense = round(evolved_template.daimon_template_stat_base_physical_defense * self.daimon_unbonded_level, 2)
                self.daimon_unbonded_stat_special_defense = round(evolved_template.daimon_template_stat_base_special_defense * self.daimon_unbonded_level, 2)
                self.daimon_unbonded_stat_speed = round(evolved_template.daimon_template_stat_base_speed * self.daimon_unbonded_level, 2)

                # --- Update max health, current health, and current status (scaled by current level) ---
                self.daimon_unbonded_max_health = self.daimon_unbonded_stat_health * 2 + self.daimon_unbonded_level
                self.daimon_unbonded_current_health = self.daimon_unbonded_max_health
                self.daimon_unbonded_status = None

                # --- Restore abilities and moves ---
                self.daimon_unbonded_ability = ability
                self.daimon_unbonded_move_1, self.daimon_unbonded_move_2, self.daimon_unbonded_move_3, self.daimon_unbonded_move_4 = moves

                print(f"🌟 {current_template.daimon_template_species} evolved into {self.daimon_unbonded_species}!")
                return True

        # No evolution triggered
        return False
    
    def take_battle_turn(self, battle: "SystemDaimonBattle"):
        """Wild Daimon turn logic using random actions."""

        opponents = battle.get_opponents_for_participant(self)
        if not opponents:
            print(f"⚠️ Wild {self.daimon_unbonded_species} has no opponents to attack.")
            return

        target = random.choice(opponents)

        # --- Get moves ----
        move_slots = [
            getattr(self, "daimon_unbonded_move_1", None),
            getattr(self, "daimon_unbonded_move_2", None),
            getattr(self, "daimon_unbonded_move_3", None),
            getattr(self, "daimon_unbonded_move_4", None),
        ]

        # Filter out None move slots and those with no current points left
        moves_with_current_points = [m for m in move_slots if m and m.daimon_move_points_current > 0]
        # Choose a move
        if not moves_with_current_points:
            # Struggle if there are no move options
            move = get_daimon_move_by_id(4)
            print(f"💢 Wild {self.daimon_unbonded_species} has no moves left! It used {move.daimon_move_name}!\n")
        else:
            # Choose randomly from available PP
            move = random.choice(moves_with_current_points)
            move.daimon_move_points_current -= 1
            print(f"🐾 Wild {self.daimon_unbonded_species} used {move.daimon_move_name}!")

        # ------------------------------
        # Execute the move
        # ------------------------------
        battle.execute_move(self, target, move)

    def update_status(self):
        """Automatically update the Daimon's status based on current health."""
        if self.daimon_unbonded_current_health == 0:
            self.daimon_unbonded_status = "Fainted"
        elif self.daimon_unbonded_status > 0:
            self.daimon_unbonded_status = None

    def add_current_health(self, amount: int):
        """Restore health safely and update fainted status."""
        if amount < 0:
            raise ValueError("Cannot add a negative health amount.")
        self.daimon_unbonded_current_health = min(
            self.daimon_unbonded_max_health,
            self.daimon_unbonded_current_health + amount
        )
        self.update_status_based_on_health()

    def subtract_current_health(self, amount: int):
        """Reduce health safely and update fainted status."""
        self.daimon_unbonded_current_health = max(0, self.daimon_unbonded_current_health - amount)
        self.update_status_based_on_health()

@dataclass(kw_only=True)
class DaimonBonded:
    """Represents a DaimonBonded and its attributes."""

    daimon_bonded_id: int                                     # Unique Daimon Bonded ID              # Example: 1
    daimon_bonded_daimon_template_id: int                     # Daimon Template ID                   # Example: 1
    daimon_bonded_species: str                                # Unique Daimon Bonded Species         # Example: "Palanine"
    daimon_bonded_level: int                                  # Daimon Bonded Level                  # Example: 50
    daimon_bonded_level_progress: int                         # Daimon Bonded Level Progress         # Example: 25
    daimon_bonded_gender: str                                 # Daimon Bonded Gender                 # Example: "Male" 
    daimon_bonded_height: float                               # Daimon Bonded Height                 # Example: 0.75
    daimon_bonded_weight: float                               # Daimon Bonded Weight                 # Example: 15
    daimon_bonded_max_health: int                             # Daimon Bonded Maximum Health         # Example: 200
    daimon_bonded_current_health: int                         # Daimon Bonded Current Health         # Example: 200
    daimon_bonded_status: DaimonStatus                        # Daimon Bonded Current Status         # Example: "Sleep"
    daimon_bonded_stat_health: float                          # Daimon Bonded Stat Health            # Example: 1
    daimon_bonded_stat_physical_attack: float                 # Daimon Bonded Stat Physical Attack   # Example: 1
    daimon_bonded_stat_special_attack: float                  # Daimon Bonded Stat Special Attack    # Example: 1
    daimon_bonded_stat_physical_defense: float                # Daimon Bonded Stat Physical Defense  # Example: 1
    daimon_bonded_stat_special_defense: float                 # Daimon Bonded Stat Special Defense   # Example: 1
    daimon_bonded_stat_speed: float                           # Daimon Bonded Stat Speed             # Example: 1
    daimon_bonded_type_1: DaimonType                          # Daimon Bonded Type 1                 # Example: DaimonType
    daimon_bonded_type_2: Optional[DaimonType] = None         # Daimon Bonded Type 2                 # Example: DaimonType
    daimon_bonded_ability: DaimonAbility                      # Daimon Bonded Ability                # Example: DaimonAbility
    daimon_bonded_move_1: Optional[DaimonMove] = None         # Daimon Bonded Move 1                 # Example: DaimonMove
    daimon_bonded_move_2: Optional[DaimonMove] = None         # Daimon Bonded Move 2                 # Example: DaimonMove
    daimon_bonded_move_3: Optional[DaimonMove] = None         # Daimon Bonded Move 3                 # Example: DaimonMove
    daimon_bonded_move_4: Optional[DaimonMove] = None         # Daimon Bonded Move 4                 # Example: DaimonMove
    daimon_bonded_item: Optional[Item] = None                 # Daimon Bonded Item                   # Example: Item
    daimon_bonded_nickname: str                               # Daimon Bonded Nickname               # Example: "Ronin"

    # --------------------------------------------------
    # Create DaimonBonded object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "DaimonBonded":

        def load_daimon_bonded_move(key: str):
            move_block = d.get(key)
            if move_block is None:
                return None

            daimon_move_template_id = move_block.get("daimon_move_template_id")
            daimon_move_points_current = move_block.get("daimon_move_points_current")

            daimon_move_template = get_daimon_move_template_by_id(daimon_move_template_id)

            daimon_move_effect_status = []

            for effect in daimon_move_template.daimon_move_template_effect_status:
                status_template = effect.get("daimon_move_template_status")
                if status_template is None:
                    continue  # skip empty slots

                status_instance = DaimonStatus.from_dict({
                    "daimon_status_id": status_template.daimon_status_template_id,
                    "daimon_status_name": status_template.daimon_status_template_name,
                    "daimon_status_description": status_template.daimon_status_template_description,
                    "daimon_status_effect": status_template.daimon_status_template_effect,
                    "daimon_status_duration_max": status_template.daimon_status_template_duration_max,
                    "daimon_status_duration_current": 0  # start fresh
                })

                daimon_move_effect_status.append({
                    "daimon_move_status": status_instance,
                    "daimon_move_status_weight": effect.get("daimon_move_template_status_weight", 1.0),
                    "daimon_effect_status_target": effect.get("daimon_move_template_status_target", "Target")
                })

            return DaimonMove(
                daimon_move_id                 = daimon_move_template.daimon_move_template_id,
                daimon_move_name               = daimon_move_template.daimon_move_template_name,
                daimon_move_type               = daimon_move_template.daimon_move_template_type,
                daimon_move_description        = daimon_move_template.daimon_move_template_description,
                daimon_move_category           = daimon_move_template.daimon_move_template_category,
                daimon_move_power              = daimon_move_template.daimon_move_template_power,
                daimon_move_accuracy           = daimon_move_template.daimon_move_template_accuracy,
                daimon_move_points_base        = daimon_move_template.daimon_move_template_points_base,
                daimon_move_points_max         = daimon_move_template.daimon_move_template_points_max,
                daimon_move_points_current     = daimon_move_points_current,
                daimon_move_effect_status      = daimon_move_effect_status,
                daimon_move_effect_stat_change = daimon_move_template.daimon_move_template_effect_stat_change
            )

        daimon_bonded_move_1 = load_daimon_bonded_move("daimon_bonded_move_1")
        daimon_bonded_move_2 = load_daimon_bonded_move("daimon_bonded_move_2")
        daimon_bonded_move_3 = load_daimon_bonded_move("daimon_bonded_move_3")
        daimon_bonded_move_4 = load_daimon_bonded_move("daimon_bonded_move_4")

        def load_daimon_bonded_item(key: str):
            item_block = d.get(key)
            if item_block is None:
                return None

            item_template_id = item_block.get("item_template_id")
            item_hex_code_1  = item_block.get("item_hex_code_1")
            item_hex_code_2  = item_block.get("item_hex_code_2")
            item_hex_code_3  = item_block.get("item_hex_code_3")
            item_hex_code_4  = item_block.get("item_hex_code_4")
            item_hex_code_5  = item_block.get("item_hex_code_5")
            item_hex_code_6  = item_block.get("item_hex_code_6")
            item_hex_code_7  = item_block.get("item_hex_code_7")
            item_hex_code_8  = item_block.get("item_hex_code_8")
            item_hex_code_9  = item_block.get("item_hex_code_9")
            item_hex_code_10 = item_block.get("item_hex_code_10")
            item_quantity    = item_block.get("item_quantity")

            item_template = get_item_template_by_id(item_template_id)

            return Item(
                item_id          = item_template.item_template_id,
                item_name        = item_template.item_template_name,
                item_description = item_template.item_template_description,
                item_category    = item_template.item_template_category,
                item_actions     = item_template.item_template_actions,
                item_base_value  = item_template.item_template_base_value,
                item_hex_code_1  = item_hex_code_1,
                item_hex_code_2  = item_hex_code_2,
                item_hex_code_3  = item_hex_code_3,
                item_hex_code_4  = item_hex_code_4,
                item_hex_code_5  = item_hex_code_5,
                item_hex_code_6  = item_hex_code_6,
                item_hex_code_7  = item_hex_code_7,
                item_hex_code_8  = item_hex_code_8,
                item_hex_code_9  = item_hex_code_9,
                item_hex_code_10 = item_hex_code_10,
                item_quantity    = item_quantity
            )
        
        daimon_bonded_item = load_daimon_bonded_item("daimon_bonded_item")

        return cls(
            daimon_bonded_id                    = d["daimon_bonded_id"],
            daimon_bonded_daimon_template_id    = d["daimon_bonded_daimon_template_id"],
            daimon_bonded_species               = d["daimon_bonded_species"],
            daimon_bonded_level                 = d["daimon_bonded_level"],
            daimon_bonded_level_progress        = d["daimon_bonded_level_progress"],
            daimon_bonded_gender                = d["daimon_bonded_gender"],
            daimon_bonded_height                = d["daimon_bonded_height"],
            daimon_bonded_weight                = d["daimon_bonded_weight"],
            daimon_bonded_max_health            = d["daimon_bonded_max_health"],
            daimon_bonded_current_health        = d["daimon_bonded_current_health"],
            daimon_bonded_status                = d.get(get_daimon_status_by_id(["daimon_bonded_status_id"])),
            daimon_bonded_stat_health           = d["daimon_bonded_stat_health"],
            daimon_bonded_stat_physical_attack  = d["daimon_bonded_stat_physical_attack"],
            daimon_bonded_stat_special_attack   = d["daimon_bonded_stat_special_attack"],
            daimon_bonded_stat_physical_defense = d["daimon_bonded_stat_physical_defense"],
            daimon_bonded_stat_special_defense  = d["daimon_bonded_stat_special_defense"],
            daimon_bonded_stat_speed            = d["daimon_bonded_stat_speed"],
            daimon_bonded_type_1                = get_daimon_type_by_id(d.get("daimon_bonded_type_id_1")),
            daimon_bonded_type_2                = get_daimon_type_by_id(d.get("daimon_bonded_type_id_2")),
            daimon_bonded_ability               = get_daimon_ability_by_id(d["daimon_bonded_ability_id"]),
            daimon_bonded_move_1                = daimon_bonded_move_1,
            daimon_bonded_move_2                = daimon_bonded_move_2,
            daimon_bonded_move_3                = daimon_bonded_move_3,
            daimon_bonded_move_4                = daimon_bonded_move_4,
            daimon_bonded_item                  = daimon_bonded_item,
            daimon_bonded_nickname              = d.get("daimon_bonded_nickname"),
        )
    
    # --------------------------------------------------
    # Convert DaimonBonded object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "daimon_bonded_id"                    : self.daimon_bonded_id,
            "daimon_bonded_daimon_template_id"    : self.daimon_bonded_daimon_template_id,
            "daimon_bonded_species"               : self.daimon_bonded_species,
            "daimon_bonded_level"                 : self.daimon_bonded_level,
            "daimon_bonded_level_progress"        : self.daimon_bonded_level_progress,
            "daimon_bonded_gender"                : self.daimon_bonded_gender,
            "daimon_bonded_height"                : self.daimon_bonded_height,
            "daimon_bonded_weight"                : self.daimon_bonded_weight,
            "daimon_bonded_max_health"            : self.daimon_bonded_max_health,
            "daimon_bonded_current_health"        : self.daimon_bonded_current_health,
            "daimon_bonded_status_id"             : self.daimon_bonded_status.daimon_status_id,
            "daimon_bonded_stat_health"           : self.daimon_bonded_stat_health,
            "daimon_bonded_stat_physical_attack"  : self.daimon_bonded_stat_physical_attack,
            "daimon_bonded_stat_special_attack"   : self.daimon_bonded_stat_special_attack,
            "daimon_bonded_stat_physical_defense" : self.daimon_bonded_stat_physical_defense,
            "daimon_bonded_stat_special_defense"  : self.daimon_bonded_stat_special_defense,
            "daimon_bonded_stat_speed"            : self.daimon_bonded_stat_speed,
            "daimon_bonded_type_id_1"             : self.daimon_bonded_type_1.daimon_type_id,
            "daimon_bonded_type_id_2"             : self.daimon_bonded_type_2.daimon_type_id if self.daimon_bonded_type_2 else None,
            "daimon_bonded_ability_id"            : self.daimon_bonded_ability.daimon_ability_id,
            "daimon_bonded_move_1"                : {"daimon_move_template_id": self.daimon_bonded_move_1.daimon_move_id, 
                                                       "daimon_move_points_current": self.daimon_bonded_move_1.daimon_move_points_current} if self.daimon_bonded_move_1 else None,
            "daimon_bonded_move_2"                : {"daimon_move_template_id": self.daimon_bonded_move_2.daimon_move_id, 
                                                       "daimon_move_points_current": self.daimon_bonded_move_1.daimon_move_points_current} if self.daimon_bonded_move_2 else None,
            "daimon_bonded_move_3"                : {"daimon_move_template_id": self.daimon_bonded_move_3.daimon_move_id, 
                                                       "daimon_move_points_current": self.daimon_bonded_move_1.daimon_move_points_current} if self.daimon_bonded_move_3 else None,
            "daimon_bonded_move_4"                : {"daimon_move_template_id": self.daimon_bonded_move_4.daimon_move_id, 
                                                       "daimon_move_points_current": self.daimon_bonded_move_1.daimon_move_points_current} if self.daimon_bonded_move_4 else None,
            "daimon_bonded_item"                  : {"item_template_id": self.daimon_bonded_item.item_id, 
                                                       "item_hex_code_1": self.daimon_bonded_item.item_hex_code_1,
                                                       "item_hex_code_2": self.daimon_bonded_item.item_hex_code_2,
                                                       "item_hex_code_3": self.daimon_bonded_item.item_hex_code_3,
                                                       "item_hex_code_4": self.daimon_bonded_item.item_hex_code_4,
                                                       "item_hex_code_5": self.daimon_bonded_item.item_hex_code_5,
                                                       "item_hex_code_6": self.daimon_bonded_item.item_hex_code_6,
                                                       "item_hex_code_7": self.daimon_bonded_item.item_hex_code_7,
                                                       "item_hex_code_8": self.daimon_bonded_item.item_hex_code_8,
                                                       "item_hex_code_9": self.daimon_bonded_item.item_hex_code_9,
                                                       "item_hex_code_10": self.daimon_bonded_item.item_hex_code_10,
                                                       "item_quantity": self.daimon_bonded_item.item_quantity} if self.daimon_bonded_item else None,
            "daimon_bonded_nickname"              : self.daimon_bonded_nickname
        }
    
    def add_level_progress(self, progress: float):
        """
        Adds experience to the DaimonBonded's level progress.
        If level_progress reaches or exceeds 1, increases level by 1 and carries over remainder.
        If evolution is possible, prompts the player whether to evolve via input().
        """
        if progress < 0:
            raise ValueError("Progress must be non-negative.")

        self.daimon_bonded_level_progress += progress

        # Handle level-up(s)
        while self.daimon_bonded_level_progress >= 1.0:
            self.daimon_bonded_level += 1
            self.daimon_bonded_level_progress -= 1.0
            print(f"⬆️ {self.daimon_bonded_species} leveled up! New level: {self.daimon_bonded_level}")

            # Check for evolution
            can_evolve = False
            current_species = self.daimon_bonded_species
            if self.try_evolve():  # Returns True if evolution possible
                can_evolve = True
                # Reset species for now; actual evolution runs after choice
                self.daimon_bonded_species = current_species

            if can_evolve:
                # Prompt player directly
                choice = input(f"{self.daimon_bonded_species} is ready to evolve! Evolve now? (y/n): ").lower()
                if choice.startswith("y"):
                    self.try_evolve()
                else:
                    print(f"⚡ Evolution of {self.daimon_bonded_species} postponed by player choice.")

        print(f"Current level progress for {self.daimon_bonded_species}: {round(self.daimon_bonded_level_progress, 2)}")

    def try_evolve(self):
        """
        Checks if this DaimonBonded should evolve based on its level.
        If so, updates its species, types, stats, height, and weight.
        Abilities and moves are preserved.
        """
        # Get the current DaimonTemplate
        current_template = get_daimon_template_by_id(self.daimon_bonded_daimon_template_id)
        if not current_template:
            print(f"❌ No template found for species {self.daimon_bonded_species}.")
            return False

        # Flatten all evolution stages
        evolution_stages = (
            (current_template.daimon_template_evolution_1 or []) +
            (current_template.daimon_template_evolution_2 or []) +
            (current_template.daimon_template_evolution_3 or [])
        )

        if not evolution_stages:
            print(f"ℹ️ {self.daimon_bonded_species} has no evolutions.")
            return False

        # Find eligible evolutions based on level and (optional) item
        for stage in evolution_stages:
            required_level = stage.get("daimon_template_evolution_level", 0)
            required_item = stage.get("daimon_template_evolution_requirement", None)
            if self.daimon_bonded_level >= required_level:
                if required_item and (self.daimon_bonded_item is None or self.daimon_bonded_item.item_id != required_item.item_id):
                    continue  # Can't evolve without required item
                # Found a valid evolution
                evolved_template = get_daimon_template_by_id(stage["daimon_template_evolution_id"])
                if not evolved_template:
                    print(f"❌ Evolution template ID {stage['daimon_template_evolution_id']} not found.")
                    return False

                # --- Preserve abilities and moves ---
                ability = self.daimon_bonded_ability
                moves = [
                    self.daimon_bonded_move_1,
                    self.daimon_bonded_move_2,
                    self.daimon_bonded_move_3,
                    self.daimon_bonded_move_4
                ]

                # --- Height & Weight ratio preservation ---
                old_height_min = current_template.daimon_template_height_distribution.get("daimon_template_height_mean", 1) - current_template.daimon_template_height_distribution.get("daimon_template_height_range", 0)
                old_height_max = current_template.daimon_template_height_distribution.get("daimon_template_height_mean", 1) + current_template.daimon_template_height_distribution.get("daimon_template_height_range", 0)
                old_height_range = old_height_max - old_height_min
                old_height_ratio = (self.daimon_bonded_height - old_height_min) / old_height_range if old_height_range else 0.5

                new_height_mean = evolved_template.daimon_template_height_distribution.get("daimon_template_height_mean", 1)
                new_height_range = evolved_template.daimon_template_height_distribution.get("daimon_template_height_range", 0)
                new_height_min = new_height_mean - new_height_range
                new_height_max = new_height_mean + new_height_range
                self.daimon_bonded_height = round(new_height_min + old_height_ratio * (new_height_max - new_height_min), 2)

                old_weight_min = current_template.daimon_template_weight_distribution.get("daimon_template_weight_mean", 1) - current_template.daimon_template_weight_distribution.get("daimon_template_weight_range", 0)
                old_weight_max = current_template.daimon_template_weight_distribution.get("daimon_template_weight_mean", 1) + current_template.daimon_template_weight_distribution.get("daimon_template_weight_range", 0)
                old_weight_range = old_weight_max - old_weight_min
                old_weight_ratio = (self.daimon_bonded_weight - old_weight_min) / old_weight_range if old_weight_range else 0.5

                new_weight_mean = evolved_template.daimon_template_weight_distribution.get("daimon_template_weight_mean", 1)
                new_weight_range = evolved_template.daimon_template_weight_distribution.get("daimon_template_weight_range", 0)
                new_weight_min = new_weight_mean - new_weight_range
                new_weight_max = new_weight_mean + new_weight_range
                self.daimon_bonded_weight = round(new_weight_min + old_weight_ratio * (new_weight_max - new_weight_min), 2)

                # --- Update species, types, and stats (scaled by current level) ---
                self.daimon_bonded_species = evolved_template.daimon_template_species
                self.daimon_bonded_type_1 = evolved_template.daimon_template_type_1
                self.daimon_bonded_type_2 = evolved_template.daimon_template_type_2

                self.daimon_bonded_stat_health = round(evolved_template.daimon_template_stat_base_health * self.daimon_bonded_level, 2)
                self.daimon_bonded_stat_physical_attack = round(evolved_template.daimon_template_stat_base_physical_attack * self.daimon_bonded_level, 2)
                self.daimon_bonded_stat_special_attack = round(evolved_template.daimon_template_stat_base_special_attack * self.daimon_bonded_level, 2)
                self.daimon_bonded_stat_physical_defense = round(evolved_template.daimon_template_stat_base_physical_defense * self.daimon_bonded_level, 2)
                self.daimon_bonded_stat_special_defense = round(evolved_template.daimon_template_stat_base_special_defense * self.daimon_bonded_level, 2)
                self.daimon_bonded_stat_speed = round(evolved_template.daimon_template_stat_base_speed * self.daimon_bonded_level, 2)

                # --- Update max health, current health, and current status (scaled by current level) ---
                self.daimon_bonded_max_health = self.daimon_bonded_stat_health * 2 + self.daimon_bonded_level
                self.daimon_bonded_current_health = self.daimon_bonded_max_health
                self.daimon_bonded_status = None

                # --- Restore abilities and moves ---
                self.daimon_bonded_ability = ability
                self.daimon_bonded_move_1, self.daimon_bonded_move_2, self.daimon_bonded_move_3, self.daimon_bonded_move_4 = moves

                print(f"🌟 {current_template.daimon_template_species} evolved into {self.daimon_bonded_species}!")
                return True

        # No evolution triggered
        return False
    
    # --------------------------------------------------
    # Item Management
    # --------------------------------------------------
    def give_item(self, item: "Item", player: "Player") -> bool:
        """
        Gives an item from the player to this DaimonBonded.
        If the Daimon already has an item, prompts a switch instead.
        """
        # Ensure player actually owns the item before removing it
        has_item = player.check_player_has_item(item)
        if not has_item:
            print(f"⚠️ {player.player_name} does not have {item.item_name} to give.")
            return False

        # If Daimon already holds an item, prompt for switch
        if self.daimon_bonded_item:
            current_item = self.daimon_bonded_item
            print(f"🔁 {self.daimon_bonded_species} already holds {current_item.item_name}.")

            # Confirm switch
            confirm = input(f"Would you like to switch {current_item.item_name} for {item.item_name}? (y/n): ").strip().lower()
            if confirm != "y":
                print("❎ Switch cancelled.")
                return False

            # Perform switch
            player.add_item_to_player_item_inventory(current_item)
            player.subtract_item_from_player_item_inventory(item, quantity=1)
            self.daimon_bonded_item = item

            print(f"✅ {self.daimon_bonded_species} now holds {item.item_name}. {current_item.item_name} was returned to {player.player_name}.")
            return True

        # Daimon has no item — simply give it
        success = player.subtract_item_from_player_item_inventory(item, quantity=1)
        if success:
            self.daimon_bonded_item = item
            print(f"🎁 {self.daimon_bonded_species} now holds {item.item_name}.")
            return True

        print(f"⚠️ Failed to give {item.item_name} to {self.daimon_bonded_species}.")
        return False


    def take_item(self, player: "Player") -> bool:
        """
        Takes the currently held item from the DaimonBonded and returns it to the player's inventory.
        Prevents taking if no item is held.
        """
        if not self.daimon_bonded_item:
            print(f"⚠️ {self.daimon_bonded_species} isn’t holding any item.")
            return False

        item = self.daimon_bonded_item
        player.add_item_to_player_item_inventory(item)
        self.daimon_bonded_item = None

        print(f"🪄 Took {item.item_name} from {self.daimon_bonded_species} and returned it to {player.player_name}'s inventory.")
        return True
    
    def update_status(self):
        """Automatically update the Daimon's status based on current health."""
        if self.daimon_bonded_current_health == 0:
            self.daimon_bonded_status = "Fainted"
        elif self.daimon_bonded_status > 0:
            self.daimon_bonded_status = None

    def add_current_health(self, amount: int):
        """Restore health safely and update fainted status."""
        if amount < 0:
            raise ValueError("Cannot add a negative health amount.")
        self.daimon_bonded_current_health = min(
            self.daimon_bonded_max_health,
            self.daimon_bonded_current_health + amount
        )
        self.update_status_based_on_health()

    def subtract_current_health(self, amount: int):
        """Reduce health safely and update fainted status."""
        self.daimon_bonded_current_health = max(0, self.daimon_bonded_current_health - amount)
        self.update_status_based_on_health()

@dataclass(kw_only=True)
class QuestStepTemplate:
    """Represents a QuestStepTemplate and its base attributes."""

    quest_step_template_id: int
    quest_step_template_name: str
    quest_step_template_description: str
    quest_step_template_start_pool: List[Union["Interactible", "Item", "Location", "NPC"]]
    quest_step_template_end_pool: List[Union["Interactible", "Item", "Location", "NPC"]]
    quest_step_template_reward_money_range: List[int]
    quest_step_template_reward_item_template_pool: Optional[List[Dict[str, Union["ItemTemplate", float]]]]
    quest_step_template_status: str

    # --------------------------------------------------
    # Create QuestStepTemplate object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "QuestStepTemplate":
        # --- START POOL ---
        start_pool_data = d.get("quest_step_template_start_pool", [])
        start_pool: List[Union["Interactible", "Item", "Location", "NPC"]] = []

        for pool in start_pool_data:
            if "start_pool_interactible_ids" in pool:
                start_pool.extend([get_interactible_by_id(i) for i in pool["start_pool_interactible_ids"]])
            if "start_pool_item_ids" in pool:
                start_pool.extend([get_item_by_id(i) for i in pool["start_pool_item_ids"]])
            if "start_pool_location_ids" in pool:
                start_pool.extend([get_location_by_id(i) for i in pool["start_pool_location_ids"]])
            if "start_pool_npc_ids" in pool:
                start_pool.extend([get_npc_by_id(i) for i in pool["start_pool_npc_ids"]])

        # --- END POOL ---
        end_pool_data = d.get("quest_step_template_end_pool", [])
        end_pool: List[Union["Interactible", "Item", "Location", "NPC"]] = []

        for pool in end_pool_data:
            if "end_pool_interactible_ids" in pool:
                end_pool.extend([get_interactible_by_id(i) for i in pool["end_pool_interactible_ids"]])
            if "end_pool_item_ids" in pool:
                end_pool.extend([get_item_by_id(i) for i in pool["end_pool_item_ids"]])
            if "end_pool_location_ids" in pool:
                end_pool.extend([get_location_by_id(i) for i in pool["end_pool_location_ids"]])
            if "end_pool_npc_ids" in pool:
                end_pool.extend([get_npc_by_id(i) for i in pool["end_pool_npc_ids"]])

        # --- ITEM POOL ---
        item_pool_data = d.get("quest_step_template_reward_item_template_pool", [])
        item_pool: List[Dict[str, Union[float, "ItemTemplate"]]] = []
        for entry in item_pool_data:
            item_template_id = entry.get("item_template_id")
            item_template_weight = entry.get("item_template_weight", 1.0)
            item_template = get_item_template_by_id(item_template_id)
            if item_template:
                item_pool.append({
                    "item_template": item_template,
                    "item_template_weight": item_template_weight
                })

        return cls(
            quest_step_template_id                        = d.get("quest_step_template_id"),
            quest_step_template_name                      = d.get("quest_step_template_name"),
            quest_step_template_description               = d.get("quest_step_template_description"),
            quest_step_template_start_pool                = start_pool,
            quest_step_template_end_pool                  = end_pool,
            quest_step_template_reward_money_range        = d.get("quest_step_template_reward_money_range", [0, 0]),
            quest_step_template_reward_item_template_pool = item_pool,
            quest_step_template_status                    = d.get("quest_step_template_status", "Not Started"),
        )

    # --------------------------------------------------
    # Convert QuestStepTemplate object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "quest_step_template_id": self.quest_step_template_id,
            "quest_step_template_name": self.quest_step_template_name,
            "quest_step_template_description": self.quest_step_template_description,
            "quest_step_template_start_pool": [
                {"start_pool_interactible_ids": [obj.interactible_id for obj in self.quest_step_template_start_pool if hasattr(obj, "interactible_id")]},
                {"start_pool_item_ids": [obj.item_id for obj in self.quest_step_template_start_pool if hasattr(obj, "item_id")]},
                {"start_pool_location_ids": [obj.location_id for obj in self.quest_step_template_start_pool if hasattr(obj, "location_id")]},
                {"start_pool_npc_ids": [obj.npc_id for obj in self.quest_step_template_start_pool if hasattr(obj, "npc_id")]}
                
            ],
            "quest_step_template_end_pool": [
                {"end_pool_interactible_ids": [obj.interactible_id for obj in self.quest_step_template_end_pool if hasattr(obj, "interactible_id")]},
                {"end_pool_item_ids": [obj.item_id for obj in self.quest_step_template_end_pool if hasattr(obj, "item_id")]},
                {"end_pool_location_ids": [obj.location_id for obj in self.quest_step_template_end_pool if hasattr(obj, "location_id")]},
                {"end_pool_npc_ids": [obj.npc_id for obj in self.quest_step_template_end_pool if hasattr(obj, "npc_id")]}
            ],
            "quest_step_template_reward_money_range": self.quest_step_template_reward_money_range,
            "quest_step_template_reward_item_template_pool": [
                {
                    "item_template_id": entry["item_template"].item_template_id,
                    "item_template_weight": entry["item_template_weight"],
                }
                for entry in self.quest_step_template_reward_item_template_pool or []
            ],
            "quest_step_template_status": self.quest_step_template_status,
        }

@dataclass(kw_only=True)
class QuestStep:
    quest_step_id           : int
    quest_step_name         : str
    quest_step_description  : str
    quest_step_start_type   : str
    quest_step_start        : Union["Interactible", "Item", "Location", "NPC"]
    quest_step_end_type     : str
    quest_step_end          : Union["Interactible", "Item", "Location", "NPC"]
    quest_step_reward_money : int
    quest_step_reward_item  : Optional["Item"]
    quest_step_status       : str

    # --------------------------------------------------
    # Create QuestStep object from dictionary
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "QuestStep":
        quest_step_start_type = d.get("quest_step_start_type")
        quest_step_start_id = d.get("quest_step_start_id")
        if quest_step_start_type == "Interactible":
            quest_step_start = get_interactible_by_id(quest_step_start_id)
        elif quest_step_start_type == "Item":
            quest_step_start = get_item_by_id(quest_step_start_id)
        elif quest_step_start_type == "Location":
            quest_step_start = get_location_by_id(quest_step_start_id)
        elif quest_step_start_type == "NPC":
            quest_step_start = get_npc_by_id(quest_step_start_id)
        
        quest_step_end_type = d.get("quest_step_end_type")
        quest_step_end_id = d.get("quest_step_end_id")
        if quest_step_end_type == "Interactible":
            quest_step_end = get_interactible_by_id(quest_step_end_id)
        elif quest_step_end_type == "Item":
            quest_step_end = get_item_by_id(quest_step_end_id)
        elif quest_step_end_type == "Location":
            quest_step_end = get_location_by_id(quest_step_end_id)
        elif quest_step_end_type == "NPC":
            quest_step_end = get_npc_by_id(quest_step_end_id)

        return cls(
            quest_step_id           = d.get("quest_step_id"),
            quest_step_name         = d.get("quest_step_name"),
            quest_step_description  = d.get("quest_step_description"),
            quest_step_start_type   = quest_step_start_type,
            quest_step_start        = quest_step_start,
            quest_step_end_type     = quest_step_end_type,
            quest_step_end          = quest_step_end,
            quest_step_reward_money = d.get("quest_step_reward_money", 0),
            quest_step_reward_item  = get_item_by_id(d.get("quest_step_reward_item")),
            quest_step_status       = d.get("quest_step_status", "Not Started"),
        )

    # --------------------------------------------------
    # Convert QuestStep object to dictionary
    # --------------------------------------------------
    def to_dict(self) -> dict:
        if self.quest_step_start_type == "Interactible":
            start_id = self.quest_step_start.interactible_id
        elif self.quest_step_start_type == "Item":
            start_id = self.quest_step_start.item_id
        elif self.quest_step_start_type == "Location":
            start_id = self.quest_step_start.location_id
        elif self.quest_step_start_type == "NPC":
            start_id = self.quest_step_start.npc_id

        if self.quest_step_end_type == "Interactible":
            end_id = self.quest_step_end.interactible_id
        elif self.quest_step_end_type == "Item":
            end_id = self.quest_step_end.item_id
        elif self.quest_step_end_type == "Location":
            end_id = self.quest_step_end.location_id
        elif self.quest_step_end_type == "NPC":
            end_id = self.quest_step_end.npc_id
            
        return {
            "quest_step_id"           : self.quest_step_id,
            "quest_step_name"         : self.quest_step_name,
            "quest_step_description"  : self.quest_step_description,
            "quest_step_start_type"   : self.quest_step_start_type,
            "quest_step_start_id"     : start_id,
            "quest_step_end_type"     : self.quest_step_end_type,
            "quest_step_end_id"       : end_id,
            "quest_step_reward_money" : self.quest_step_reward_money,
            "quest_step_reward_item"  : self.quest_step_reward_item.item_id if self.quest_step_reward_item else None,
            "quest_step_status"       : self.quest_step_status,
        }
    
@dataclass(kw_only=True)
class QuestType:
    quest_type_id                         : int
    quest_type_name                       : str
    quest_type_description                : str
    quest_type_quest_step_template_starts : List["QuestStepTemplate"]
    quest_type_quest_step_template_steps  : List["QuestStepTemplate"]
    quest_type_quest_step_template_ends   : List["QuestStepTemplate"]

    @classmethod
    def from_dict(cls, d: dict) -> "QuestType":
        # Extract IDs from nested dicts
        start_ids = d.get("quest_type_quest_step_template_starts", {}).get("quest_step_template_start_ids", [])
        step_ids  = d.get("quest_type_quest_step_template_steps", {}).get("quest_step_template_step_ids", [])
        end_ids   = d.get("quest_type_quest_step_template_ends", {}).get("quest_step_template_end_ids", [])

        # Resolve IDs into QuestStepTemplate objects
        start_templates = [get_quest_step_template_by_id(i) for i in start_ids]
        step_templates  = [get_quest_step_template_by_id(i) for i in step_ids]
        end_templates   = [get_quest_step_template_by_id(i) for i in end_ids]

        return cls(
            quest_type_id                         = d.get("quest_type_id"),
            quest_type_name                       = d.get("quest_type_name"),
            quest_type_description                = d.get("quest_type_description"),
            quest_type_quest_step_template_starts = start_templates,
            quest_type_quest_step_template_steps  = step_templates,
            quest_type_quest_step_template_ends   = end_templates,
        )

    def to_dict(self) -> dict:
        return {
            "quest_type_id"                         : self.quest_type_id,
            "quest_type_name"                       : self.quest_type_name,
            "quest_type_description"                : self.quest_type_description,
            "quest_type_quest_step_template_starts" : {
                "quest_step_template_start_ids"     : [obj.quest_step_template_id for obj in self.quest_type_quest_step_template_starts]
            },
            "quest_type_quest_step_template_steps"  : {
                "quest_step_template_step_ids"      : [obj.quest_step_template_id for obj in self.quest_type_quest_step_template_steps]
            },
            "quest_type_quest_step_template_ends"   : {
                "quest_step_template_end_ids"       : [obj.quest_step_template_id for obj in self.quest_type_quest_step_template_ends]
            },
        }

@dataclass(kw_only=True)
class QuestSide:
    """Represents a QuestSide and its attributes."""

    quest_side_id           : int
    quest_side_name         : str
    quest_side_description  : str
    quest_side_type         : str
    quest_side_steps        : List[QuestStep]
    quest_side_start_type   : str
    quest_side_start        : Union["Interactible", "Item", "Location", "NPC"] # Get the quest_step_start from the first QuestStep object in the quest_side_steps list.
    quest_side_end_type     : str
    quest_side_end          : Union["Interactible", "Item", "Location", "NPC"] # Get the quest_step_end from the last QuestStep object in the quest_side_steps list.
    quest_side_reward_money : int                                              # Combine the quest_step_reward_money amounts for each QuestStep object in the quest_side_steps list.
    quest_side_reward_item  : List[Item]                                       # Combine the quest_step_reward_item Item objects for each QuestStep object in the quest_side_steps list.
    quest_side_status       : str                                              # Set to true when the quest_step_status for each QuestStep object in the quest_side_steps list is true.

    # --------------------------------------------------
    # Create QuestSide object from dictionary
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "QuestSide":
        # --- Steps ---
        quest_steps = [QuestStep.from_dict(step) for step in d.get("quest_side_steps", [])]

        # --- Rewards ---
        total_reward_money = sum(step.quest_step_reward_money for step in quest_steps)
        reward_items = [
            get_item_by_id(item_id)
            for item_id in d.get("quest_side_reward_item", [])
            if isinstance(item_id, int)
        ]

        # --- Start Entity ---
        start_type = d.get("quest_side_start_type")
        start_id   = d.get("quest_side_start")
        if start_type == "Interactible":
            start_entity = get_interactible_by_id(start_id)
        elif start_type == "Item":
            start_entity = get_item_by_id(start_id)
        elif start_type == "Location":
            start_entity = get_location_by_id(start_id)
        elif start_type == "NPC":
            start_entity = get_npc_by_id(start_id)

        # --- End Entity ---
        end_type = d.get("quest_side_end_type")
        end_id   = d.get("quest_side_end")
        if end_type == "Interactible":
            end_entity = get_interactible_by_id(end_id)
        elif end_type == "Item":
            end_entity = get_item_by_id(end_id)
        elif end_type == "Location":
            end_entity = get_location_by_id(end_id)
        elif end_type == "NPC":
            end_entity = get_npc_by_id(end_id)

        # --- Status ---
        if all(step.quest_step_status == "Complete" for step in quest_steps):
            quest_status = "Complete"
        elif any(step.quest_step_status == "In Progress" for step in quest_steps):
            quest_status = "In Progress"
        else:
            quest_status = "Not Started"

        return cls(
            quest_side_id           = d.get("quest_side_id"),
            quest_side_name         = d.get("quest_side_name"),
            quest_side_description  = d.get("quest_side_description"),
            quest_side_type         = d.get("quest_side_type"),
            quest_side_steps        = quest_steps,
            quest_side_start_type   = start_type,
            quest_side_start        = start_entity,
            quest_side_end_type     = end_type,
            quest_side_end          = end_entity,
            quest_side_reward_money = total_reward_money,
            quest_side_reward_item  = reward_items,
            quest_side_status       = quest_status,
        )

    # --------------------------------------------------
    # Convert QuestSide object to dictionary
    # --------------------------------------------------
    def to_dict(self) -> dict:
        # Determine correct IDs depending on type
        if self.quest_side_start_type == "Interactible":
            start_id = self.quest_side_start.interactible_id
        elif self.quest_side_start_type == "Item":
            start_id = self.quest_side_start.item_id
        elif self.quest_side_start_type == "Location":
            start_id = self.quest_side_start.location_id
        elif self.quest_side_start_type == "NPC":
            start_id = self.quest_side_start.npc_id

        if self.quest_side_end_type == "Interactible":
            end_id = self.quest_side_end.interactible_id
        elif self.quest_side_end_type == "Item":
            end_id = self.quest_side_end.item_id
        elif self.quest_side_end_type == "Location":
            end_id = self.quest_side_end.location_id
        elif self.quest_side_end_type == "NPC":
            end_id = self.quest_side_end.npc_id

        return {
            "quest_side_id"           : self.quest_side_id,
            "quest_side_name"         : self.quest_side_name,
            "quest_side_description"  : self.quest_side_description,
            "quest_side_type"         : self.quest_side_type,
            "quest_side_steps"        : [step.to_dict() for step in self.quest_side_steps],
            "quest_side_start_type"   : self.quest_side_start_type,
            "quest_side_start"        : start_id,
            "quest_side_end_type"     : self.quest_side_end_type,
            "quest_side_end"          : end_id,
            "quest_side_reward_money" : self.quest_side_reward_money,
            "quest_side_reward_item"  : [item.item_id for item in self.quest_side_reward_item if item is not None],
            "quest_side_status"       : self.quest_side_status,
        }

@dataclass(kw_only=True)
class QuestMain:
    """Represents a QuestMain and its attributes."""

    quest_main_id           : int
    quest_main_name         : str
    quest_main_description  : str
    quest_main_type         : str
    quest_main_quest_steps  : List[QuestStep]
    quest_main_start        : Union["Interactible", "Item", "Location", "NPC",]  # Get the quest_step_start from the first QuestStep object in the quest_main_steps list.
    quest_main_end          : Union["Interactible", "Item", "Location", "NPC",]  # Get the quest_step_end from the last QuestStep object in the quest_main_steps list.
    quest_main_reward_money : int                                                # Combine the quest_step_reward_money amounts for each QuestStep object in the quest_main_steps list.
    quest_main_reward_item  : List[Item]                                         # Combine the quest_step_reward_item Item objects for each QuestStep object in the quest_main_steps list.
    quest_main_status       : str                                                # Set to true when the quest_step_status for each QuestStep object in the quest_main_steps list is true.

@dataclass(kw_only=True)
class WeatherTemplate:
    """Represents a WeatherTemplate object and its attributes."""

    weather_template_id: int  # Unique ID for this weather type (e.g. 15)
    weather_template_name: str  # Human-readable name (e.g. "Snow")
    weather_template_intensity_base: int  # Integer base level of weather intensity

    # --------------------------------------------------
    # Create WeatherTemplate object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "WeatherTemplate":
        return cls(
            weather_template_id             = d.get("weather_template_id"),
            weather_template_name           = d.get("weather_template_name"),
            weather_template_intensity_base = d.get("weather_template_intensity_base"),
        )

@dataclass(kw_only=True)
class Weather:
    """Represents a Weather object and its attributes."""

    weather_id: int  # Unique ID for this weather type (e.g. 15)
    weather_name: str  # Human-readable name (e.g. "Snow")
    weather_intensity: int  # Integer level of weather intensity

    # --------------------------------------------------
    # Create Weather object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "Weather":
        return cls(
            weather_id        = d.get("weather_id"),
            weather_name      = d.get("weather_name"),
            weather_intensity = d.get("weather_intensity"),
        )

@dataclass(kw_only=True)
class Biome:
    """Represents a Biome object and its attributes."""

    biome_id: int                                   # Unique ID for this biome (e.g. 15)
    biome_name: str                                 # Human-readable name (e.g. "Alpine")
    biome_weather_pool: List[Dict[float, Weather]]  # List of weather types that can occur in this biome and their chance to occur

    # --------------------------------------------------
    # Create Biome object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "Biome":
        return cls(
            biome_id           = d.get("biome_id"),
            biome_name         = d.get("biome_name"),
            biome_weather_pool = [
                {"weather_chance": w.get("weather_chance"), "weather": get_weather_by_id(w.get("weather_id"))}
                for w in d.get("biome_weather_pool")
            ]
        )

@dataclass(kw_only=True)
class Location:
    """Represents a Location object and its attributes."""

    location_id: int            # Unique ID for this location (e.g. 15)
    location_name: str          # Human-readable name (e.g. "Wellspring Village")
    location_description: str   # Human-readable description (e.g. "The player's home village.")
    location_biome: Biome       # Location Biome    # Example: Biome
    location_weather: Weather   # Location Weather  # Example: Weather
    location_daimon_base_spawn_rate: float  # Rate at which Daimon can spawn here (e.g. 1)
    location_daimon_base_spawn_pool: List[Dict[float, DaimonTemplate]] # Location Daimon Spawn List
    location_item_base_spawn_rate:   float  # Rate at which items can spawn here (e.g. 1)
    location_item_base_spawn_pool:   List[Dict[float, ItemTemplate]] # Location Item Spawn List

    # --------------------------------------------------
    # Create Location object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "Location":
        return cls(
            location_id                = d.get("location_id"),
            location_name              = d.get("location_name"),
            location_description       = d.get("location_description"),
            location_biome             = get_biome_by_id(d.get("location_biome_id")),
            location_weather           = get_weather_by_id(d.get("location_weather_id")),
            location_daimon_base_spawn_rate = d.get("location_daimon_base_spawn_rate"),
            location_daimon_base_spawn_pool=[
                {entry["spawn_weight"]: get_daimon_template_by_id(entry["daimon_template_id"])}
                for entry in d.get("location_daimon_base_spawn_pool", [])
                if "spawn_weight" in entry and "daimon_template_id" in entry
            ],
            location_item_base_spawn_rate   = d.get("location_item_base_spawn_rate"),
            location_item_base_spawn_pool   = [
                {entry["spawn_weight"]: get_item_template_by_id(entry["item_template_id"])}
                for entry in d.get("location_item_base_spawn_pool", [])
                if "spawn_weight" in entry and "item_template_id" in entry
            ]
        )
    
   # --------------------------------------------------
    # Convert Location object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "location_id"               : self.location_id,
            "location_name"             : self.location_name,
            "location_description"      : self.location_description,
            "location_biome_id"         : self.location_biome.biome_id if self.location_biome else None,
            "location_weather_id"       : self.location_weather.weather_id if self.location_weather else None,
            "location_daimon_base_spawn_rate": self.location_daimon_base_spawn_rate,
            "location_daimon_base_spawn_pool": [
                {
                    "spawn_weight"     : weight,
                    "daimon_template_id": daimon_template.daimon_template_id
                }
                for entry in self.location_daimon_base_spawn_pool
                for weight, daimon_template in entry.items()
            ],
            "location_item_base_spawn_rate"  : self.location_item_base_spawn_rate,
            "location_item_base_spawn_pool"  : [
                {
                    "spawn_weight"     : weight,
                    "item_template_id" : item_template.item_template_id
                }
                for entry in self.location_item_base_spawn_pool
                for weight, item_template in entry.items()
            ],
        }

@dataclass(kw_only=True)
class Interactible:
    """Represents an Interactible object and its attributes."""

    interactible_id: int
    interactible_name: str
    interactible_location: Location

    # --------------------------------------------------
    # Create Interactible object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "Interactible":
        return cls(
            interactible_id       = d.get("interactible_id"),
            interactible_name     = d.get("interactible_name"),
            interactible_location = get_location_by_id(d.get("interactible_location_id")),
            
        )
    
    # --------------------------------------------------
    # Convert Interactible object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "interactible_id"          : self.interactible_id,
            "interactible_name"        : self.interactible_name,
            "interactible_location_id" : self.interactible_location.location_id
        }



@dataclass(kw_only=True)
class NPCItemInventory():
    """Represents an NPCItemInventory object and its attributes."""

    npc_item_inventory_id              : int
    npc_item_inventory_storage_generic : List[Item] = field(default_factory=list)
    npc_item_inventory_storage_unique  : List[Item] = field(default_factory=list)

    # --------------------------------------------------
    # Create NPCItemInventory object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "NPCItemInventory":
        return cls(
            npc_item_inventory_id              = d.get("npc_item_inventory_id"),
            npc_item_inventory_storage_generic = [Item.from_dict(item_dict) for item_dict in d.get("npc_item_inventory_storage_generic", [])],
            npc_item_inventory_storage_unique  = [Item.from_dict(item_dict) for item_dict in d.get("npc_item_inventory_storage_unique", [])]
        )
    
    # --------------------------------------------------
    # Convert NPCItemInventory object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "npc_item_inventory_id"              : self.npc_item_inventory_id,
            "npc_item_inventory_storage_generic" : [item.to_dict() for item in self.npc_item_inventory_storage_generic],
            "npc_item_inventory_storage_unique"  : [item.to_dict() for item in self.npc_item_inventory_storage_unique]
        }

    def prepopulate_generic_items_from_templates(self, templates: List["ItemTemplate"]):
        """Initialize an empty NPCItemInventory for a new or missing NPCItemInventory."""
        self.npc_item_inventory_storage_generic = [
            Item(
                item_id          = item_template.item_template_id,
                item_name        = item_template.item_template_name,
                item_description = item_template.item_template_description,
                item_category    = item_template.item_template_category,
                item_actions     = item_template.item_template_actions,
                item_base_value  = item_template.item_template_base_value,
                item_hex_code_1  = item_template.item_template_base_hex_code_1,
                item_hex_code_2  = item_template.item_template_base_hex_code_2,
                item_hex_code_3  = item_template.item_template_base_hex_code_3,
                item_hex_code_4  = item_template.item_template_base_hex_code_4,
                item_hex_code_5  = item_template.item_template_base_hex_code_5,
                item_hex_code_6  = item_template.item_template_base_hex_code_6,
                item_hex_code_7  = item_template.item_template_base_hex_code_7,
                item_hex_code_8  = item_template.item_template_base_hex_code_8,
                item_hex_code_9  = item_template.item_template_base_hex_code_9,
                item_hex_code_10 = item_template.item_template_base_hex_code_10,
                item_quantity    = 0
            )
            for item_template in templates if item_template.item_template_category in ITEM_CATEGORY_GENERIC
        ]

    def add_item_to_npc_item_inventory(self, item: Item) -> bool:
        """
        Adds/modifies an Item object to the NPCItemInventory.
        Generic items are prepopulated — modify existing Item object.
        Unique items are not prepopulated - add new Item object.
        Only allows items that exist in item_template_global.
        """
        # ---------------------------
        # Validate Item.item_quantity within acceptable range
        # ---------------------------
        if 1 <= item.item_quantity <= 1_000_000:
            print(f"⚠️ Invalid quantity {item.item_quantity}. Must be 1–1,000,000.")
            return False

        # ---------------------------
        # Validate Item is legitimate
        # ---------------------------
        if not any(template.item_template_id == item.item_id for template in item_template_global):
            print(f"⚠️ Cannot subtract item {item.item_name} (ID: {item.item_id}) — not found in item_template_global.")
            return False
        
        # ---------------------------
        # Validate Item is legitimate
        # ---------------------------
        if not any(template.item_template_id == item.item_id for template in item_template_global):
            print(f"⚠️ Cannot add item {item.item_name} (ID: {item.item_id}) — not found in item_template_global.")
            return False

        # ---------------------------
        # Unique Item
        # ---------------------------
        if item.item_category in ITEM_CATEGORY_UNIQUE:
            self.npc_item_inventory_storage_unique.append(item)
            print(f"💎 Added unique item: {item.item_name} (Category: {item.item_category}, Hex: {getattr(item, 'item_hex_code_1', None)})")
            return True

        # ---------------------------
        # Generic Item
        # ---------------------------
        elif item.item_category in ITEM_CATEGORY_GENERIC:
            # Stackable — merge into existing stack
            for existing_item in self.npc_item_inventory_storage_generic:
                if existing_item.item_id == item.item_id:
                    max_quantity = 1_000_000
                    new_quantity = existing_item.item_quantity + item.item_quantity
                    if new_quantity > max_quantity:
                        added_quantity = max_quantity - existing_item.item_quantity
                        existing_item.item_quantity = max_quantity
                        print(f"⚠️ Too much {item.item_name}. Added {added_quantity}, capped at {max_quantity}.")
                    else:
                        existing_item.item_quantity = new_quantity
                        print(f"✅ Added {item.item_quantity}x {item.item_name}. Total: {existing_item.item_quantity}.")
                    return True
    
    def subtract_item_from_npc_item_inventory(self, item: Item, quantity: int) -> bool:
        """
        Removes/modifies an Item object to the NPCItemInventory.
        Generic items are prepopulated — modify existing Item object.
        Unique items are not prepopulated - remove existing Item object.
        Only allows items that exist in item_template_global.
        """

        # ---------------------------
        # Validate quantity within acceptable range
        # ---------------------------
        if 1 <= quantity <= 1_000_000:
            print(f"⚠️ Invalid quantity {quantity}. Must be 1–1,000,000.")
            return False

        # ---------------------------
        # Validate Item is legitimate
        # ---------------------------
        if not any(template.item_template_id == item.item_id for template in item_template_global):
            print(f"⚠️ Cannot subtract item {item.item_name} (ID: {item.item_id}) — not found in item_template_global.")
            return False

        # ---------------------------
        # Unique Item
        # ---------------------------
        if item.item_category in ITEM_CATEGORY_UNIQUE:
            if item in self.npc_item_inventory_storage_unique:
                self.npc_item_inventory_storage_unique.remove(item)
                print(f"🗑️ Removed unique item: {item.item_name} (Hex: {getattr(item, 'item_hex_code_1', None)})")
                return True
            else:
                print(f"⚠️ Unique item {item.item_name} not found in inventory.")
                return False

        # ---------------------------
        # Generic Item
        # ---------------------------
        elif item.item_category in ITEM_CATEGORY_GENERIC:
            for existing_item in self.npc_item_inventory_storage_generic:
                if existing_item.item_id == item.item_id:
                    if existing_item.item_quantity >= quantity:
                        existing_item.item_quantity -= quantity
                        print(f"✅ Subtracted {quantity}x {item.item_name}. Remaining: {existing_item.item_quantity}")
                        # Do not remove the item if quantity reaches 0
                        return True
                    else:
                        print(f"⚠️ Not enough {item.item_name} to subtract {quantity}. Only have {existing_item.item_quantity}.")
                        return False

@dataclass(kw_only=True)
class NPCDaimonDexEntry():
    """
    Represents a NPCDaimonDexEntry and its attributes.
    """

    npc_daimon_dex_entry_id: int
    npc_daimon_dex_entry_daimon_template_id                  : Union[str, int]
    npc_daimon_dex_entry_daimon_template_species             : Union[str, int] = "???"
    npc_daimon_dex_entry_daimon_template_evolution_1         : Union[str, List[Dict[str, Union[int, Item]]]] = "???"
    npc_daimon_dex_entry_daimon_template_evolution_2         : Union[str, List[Dict[str, Union[int, Item]]]] = "???"
    npc_daimon_dex_entry_daimon_template_evolution_3         : Union[str, List[Dict[str, Union[int, Item]]]] = "???"
    npc_daimon_dex_entry_daimon_template_gender_distribution : Union[str, Dict[str, float]] = "???"
    npc_daimon_dex_entry_daimon_template_height_distribution : Union[str, Dict[str, float]] = "???"
    npc_daimon_dex_entry_daimon_template_weight_distribution : Union[str, Dict[str, float]] = "???"
    npc_daimon_dex_entry_daimon_template_type_1              : Union[str, DaimonType] = "???"
    npc_daimon_dex_entry_daimon_template_type_2              : Union[str, Optional[DaimonType]] = "???"
    npc_daimon_dex_entry_daimon_template_ability_pool        : Union[str, List[Dict[DaimonAbility, float]]] = "???"            
    npc_daimon_dex_entry_daimon_template_move_template_pool  : Union[str, List[DaimonMove]] = "???"
    npc_daimon_dex_entry_daimon_template_item_template_pool  : Union[str, List[Dict[ItemTemplate, float]]] = "???"                                                                
    
    # --------------------------------------------------
    # Create NPCDaimonDexEntry from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "NPCDaimonDexEntry":
        return cls(
            npc_daimon_dex_entry_id                                  = d["npc_daimon_dex_entry_id"],
            npc_daimon_dex_entry_daimon_template_id                  = d["npc_daimon_dex_entry_daimon_template_id"],
            npc_daimon_dex_entry_daimon_template_species             = d.get("npc_daimon_dex_entry_daimon_template_species", "???"),
            npc_daimon_dex_entry_daimon_template_evolution_1         = d.get("npc_daimon_dex_entry_daimon_template_evolution_1", "???"),
            npc_daimon_dex_entry_daimon_template_evolution_2         = d.get("npc_daimon_dex_entry_daimon_template_evolution_2", "???"),
            npc_daimon_dex_entry_daimon_template_evolution_3         = d.get("npc_daimon_dex_entry_daimon_template_evolution_3", "???"),
            npc_daimon_dex_entry_daimon_template_gender_distribution = d.get("npc_daimon_dex_entry_daimon_template_gender_distribution", "???"),
            npc_daimon_dex_entry_daimon_template_height_distribution = d.get("npc_daimon_dex_entry_daimon_template_height_distribution", "???"),
            npc_daimon_dex_entry_daimon_template_weight_distribution = d.get("npc_daimon_dex_entry_daimon_template_weight_distribution", "???"),
            npc_daimon_dex_entry_daimon_template_type_1              = d.get("npc_daimon_dex_entry_daimon_template_type_1", "???"),
            npc_daimon_dex_entry_daimon_template_type_2              = d.get("npc_daimon_dex_entry_daimon_template_type_2", "???"),
            npc_daimon_dex_entry_daimon_template_ability_pool        = d.get("npc_daimon_dex_entry_daimon_template_ability_pool", "???"),
            npc_daimon_dex_entry_daimon_template_move_template_pool  = d.get("npc_daimon_dex_entry_daimon_template_move_template_pool", "???"),
            npc_daimon_dex_entry_daimon_template_item_template_pool  = d.get("npc_daimon_dex_entry_daimon_template_item_template_pool", "???")
        )
    
    # --------------------------------------------------
    # Convert NPCDaimonDexEntry object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "npc_daimon_dex_entry_id"                                  : self.npc_daimon_dex_entry_id,
            "npc_daimon_dex_entry_daimon_template_id"                  : self.npc_daimon_dex_entry_daimon_template_id,
            "npc_daimon_dex_entry_daimon_template_species"             : self.npc_daimon_dex_entry_daimon_template_species,
            "npc_daimon_dex_entry_daimon_template_evolution_1"         : self.npc_daimon_dex_entry_daimon_template_evolution_1,
            "npc_daimon_dex_entry_daimon_template_evolution_2"         : self.npc_daimon_dex_entry_daimon_template_evolution_2,
            "npc_daimon_dex_entry_daimon_template_evolution_3"         : self.npc_daimon_dex_entry_daimon_template_evolution_3,
            "npc_daimon_dex_entry_daimon_template_gender_distribution" : self.npc_daimon_dex_entry_daimon_template_gender_distribution,
            "npc_daimon_dex_entry_daimon_template_height_distribution" : self.npc_daimon_dex_entry_daimon_template_height_distribution,
            "npc_daimon_dex_entry_daimon_template_weight_distribution" : self.npc_daimon_dex_entry_daimon_template_weight_distribution,
            "npc_daimon_dex_entry_daimon_template_type_1"              : self.npc_daimon_dex_entry_daimon_template_type_1,
            "npc_daimon_dex_entry_daimon_template_type_2"              : self.npc_daimon_dex_entry_daimon_template_type_2,
            "npc_daimon_dex_entry_daimon_template_ability_pool"        : self.npc_daimon_dex_entry_daimon_template_ability_pool,
            "npc_daimon_dex_entry_daimon_template_move_template_pool"  : self.npc_daimon_dex_entry_daimon_template_move_template_pool,
            "npc_daimon_dex_entry_daimon_template_item_template_pool"  : self.npc_daimon_dex_entry_daimon_template_item_template_pool
        }
    
@dataclass(kw_only=True)
class NPCDaimonDex():
    """Represents a NPCDaimonDex and its attributes."""

    npc_daimon_dex_id: int
    npc_daimon_dex_dex: List[NPCDaimonDexEntry] = field(default_factory=list)

    # --------------------------------------------------
    # Create NPCDaimonDex object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "NPCDaimonDex":
        return cls(
            npc_daimon_dex_id  = d.get("npc_daimon_dex_id"),
            npc_daimon_dex_dex = [NPCDaimonDexEntry.from_dict(entry) for entry in d.get("npc_daimon_dex_dex", [])]
        )
    
    # --------------------------------------------------
    # Convert NPCDaimonDex object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "npc_daimon_dex_id"  : self.npc_daimon_dex_id,
            "npc_daimon_dex_dex" : [dex.to_dict() for dex in self.npc_daimon_dex_dex]
        }
    
    def prepopulate_dex_entries_from_templates(self, templates: List["DaimonTemplate"]):
        """Initialize an empty NPCDaimonDex for a new or missing NPCDaimonDex."""
        self.npc_daimon_dex_dex.clear()
        for template in templates:
            entry = NPCDaimonDexEntry(
                npc_daimon_dex_entry_id                                  = len(self.npc_daimon_dex_dex) + 1,
                npc_daimon_dex_entry_daimon_template_id                  = template.daimon_template_id,
                npc_daimon_dex_entry_daimon_template_species             = "???",
                npc_daimon_dex_entry_daimon_template_evolution_1         = "???",
                npc_daimon_dex_entry_daimon_template_evolution_2         = "???",
                npc_daimon_dex_entry_daimon_template_evolution_3         = "???",
                npc_daimon_dex_entry_daimon_template_gender_distribution = "???",
                npc_daimon_dex_entry_daimon_template_height_distribution = "???",
                npc_daimon_dex_entry_daimon_template_weight_distribution = "???",
                npc_daimon_dex_entry_daimon_template_type_1              = "???",
                npc_daimon_dex_entry_daimon_template_type_2              = "???",
                npc_daimon_dex_entry_daimon_template_ability_pool        = "???",
                npc_daimon_dex_entry_daimon_template_move_template_pool  = "???",
                npc_daimon_dex_entry_daimon_template_item_template_pool  = "???"
            )
            self.npc_daimon_dex_dex.append(entry)

@dataclass(kw_only=True)
class NPCDaimonInventory():
    """Represents a NPCDaimonInventory and its attributes."""

    npc_daimon_inventory_id       : int
    npc_daimon_inventory_follower : Optional[DaimonBonded] = None
    npc_daimon_inventory_team     : List[DaimonBonded] = field(default_factory=list)
    npc_daimon_inventory_storage  : List[DaimonBonded] = field(default_factory=list)

    # --------------------------------------------------
    # Create NPCDaimonInventory from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "NPCDaimonInventory":
        return cls(
            npc_daimon_inventory_id = d.get("npc_daimon_inventory_id"),
            npc_daimon_inventory_follower = (
                DaimonBonded.from_dict(d["npc_daimon_inventory_follower"])
                if d.get("npc_daimon_inventory_follower") else None
            ),
            npc_daimon_inventory_team = [
                DaimonBonded.from_dict(b) if isinstance(b, dict) else b
                for b in d.get("npc_daimon_inventory_team", [])
            ],
            npc_daimon_inventory_storage = [
                DaimonBonded.from_dict(b) if isinstance(b, dict) else b
                for b in d.get("npc_daimon_inventory_storage", [])
            ],
        )
    
    # --------------------------------------------------
    # Convert NPCDaimonInventory to dictionary
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "npc_daimon_inventory_id": self.npc_daimon_inventory_id,
            "npc_daimon_inventory_follower": (
                self.npc_daimon_inventory_follower.to_dict()
                if self.npc_daimon_inventory_follower
                else None
            ),
            "npc_daimon_inventory_team": [
                daimon.to_dict() for daimon in self.npc_daimon_inventory_team
            ],
            "npc_daimon_inventory_storage": [
                daimon.to_dict() for daimon in self.npc_daimon_inventory_storage
            ]
        }
    
    def prepopulate_daimon_from_templates(self, templates=None):
        """Initialize an empty NPCDaimonInventory for a new or missing NPCDaimonInventory."""
        self.npc_daimon_inventory_follower = None
        self.npc_daimon_inventory_team = []
        self.npc_daimon_inventory_storage = []
    
    # ---------- Core Management ----------
    def set_follower(self, daimon_bonded: "DaimonBonded") -> bool:
        if self.npc_daimon_inventory_follower is not None:
            print(f"⚠️ Follower already set: {self.npc_daimon_inventory_follower.daimon_bonded_nickname}. Remove first.")
            return False
        self.npc_daimon_inventory_follower = daimon_bonded
        print(f"✅ {daimon_bonded.daimon_bonded_nickname} is now following the NPC.")
        return True

    def remove_follower(self) -> bool:
        if not self.npc_daimon_inventory_follower:
            print("⚠️ No follower to remove.")
            return False
        print(f"👋 {self.npc_daimon_inventory_follower.daimon_bonded_nickname} is no longer following.")
        self.npc_daimon_inventory_follower = None
        return True

    def set_daimon_nickname(self, daimon_bonded_id: int, new_nickname: str) -> bool:
        for daimon in self.npc_daimon_inventory_team:
            if daimon.daimon_bonded_id == daimon_bonded_id:
                old_nickname = daimon.daimon_bonded_nickname
                daimon.daimon_bonded_nickname = new_nickname
                print(f"✏️ Daimon '{old_nickname}' renamed to '{new_nickname}'.")
                return True
        print(f"⚠️ Daimon ID {daimon_bonded_id} not found in team.")
        return False

    def add_daimon_to_npc_daimon_inventory(self, daimon_bonded: DaimonBonded) -> bool:
        """
        Add a Daimon to the NPC's inventory.
        - If the team has fewer than 6 Daimon, prompts the NPC to choose team or storage.
        - If the team is full, automatically sends to storage.

        Returns True if added to team, False if added to storage.
        """
        if len(self.npc_daimon_inventory_team) >= 6:
            # Team is full, automatically go to storage
            self.npc_daimon_inventory_storage.append(daimon_bonded)
            print(f"⚠️ Team full. {daimon_bonded.daimon_bonded_species} sent to storage.")
            return False

        # Team has space, prompt NPC
        while True:
            choice = input(f"Place {daimon_bonded.daimon_bonded_species} in team or storage? (team/storage): ").strip().lower()
            if choice in ["team", "storage"]:
                break
            print("⚠️ Invalid input. Please type 'team' or 'storage'.")

        if choice == "team":
            self.npc_daimon_inventory_team.append(daimon_bonded)
            print(f"✅ {daimon_bonded.daimon_bonded_species} added to team.")
            return True
        else:
            self.npc_daimon_inventory_storage.append(daimon_bonded)
            print(f"✅ {daimon_bonded.daimon_bonded_species} added to storage.")
            return False
        
    def move_daimon_to_team_from_storage(self, daimon: DaimonBonded) -> bool:
        """Move a Daimon from storage to team."""
        if len(self.npc_daimon_inventory_team) >= 6:
            print("⚠️ Team is full. Cannot move Daimon from storage.")
            return False

        if daimon in self.npc_daimon_inventory_storage:
            self.npc_daimon_inventory_storage.remove(daimon)
            self.npc_daimon_inventory_team.append(daimon)
            print(f"📤 {daimon.daimon_bonded_species} moved from storage to team.")
            return True

        print(f"⚠️ {daimon.daimon_bonded_species} not found in storage.")
        return False

    def move_daimon_to_storage_from_team(self, daimon: DaimonBonded) -> bool:
        """Move a Daimon from team to storage."""
        if daimon in self.npc_daimon_inventory_team:
            self.npc_daimon_inventory_team.remove(daimon)
            self.npc_daimon_inventory_storage.append(daimon)
            print(f"📦 {daimon.daimon_bonded_species} moved to storage.")
            return True

        print(f"⚠️ {daimon.daimon_bonded_species} not found in team.")
        return False

    def switch_daimon_in_team_and_storage(self, team_daimon: DaimonBonded, storage_daimon: DaimonBonded) -> bool:
        """
        Swap a Daimon from the team with one from storage.
        Returns True if successful, False if either Daimon is not found.
        """
        if team_daimon not in self.npc_daimon_inventory_team:
            print(f"⚠️ {team_daimon.daimon_bonded_species} not found in team.")
            return False
        if storage_daimon not in self.npc_daimon_inventory_storage:
            print(f"⚠️ {storage_daimon.daimon_bonded_species} not found in storage.")
            return False

        # Perform the swap
        self.npc_daimon_inventory_team.remove(team_daimon)
        self.npc_daimon_inventory_storage.remove(storage_daimon)

        self.npc_daimon_inventory_team.append(storage_daimon)
        self.npc_daimon_inventory_storage.append(team_daimon)

        print(f"🔄 Swapped {team_daimon.daimon_bonded_species} with {storage_daimon.daimon_bonded_species}.")
        return True

    def get_all_daimons(self) -> List["DaimonBonded"]:
        result = []
        if self.npc_daimon_inventory_follower:
            result.append(self.npc_daimon_inventory_follower)
        result.extend(self.npc_daimon_inventory_team)
        result.extend(self.npc_daimon_inventory_storage)
        return result

    def get_daimon_index_in_team(self, daimon_bonded_id: int) -> Optional[int]:
        for idx, daimon in enumerate(self.npc_daimon_inventory_team):
            if daimon.daimon_bonded_id == daimon_bonded_id:
                return idx
        return None

    def get_daimon_index_in_storage(self, daimon_bonded_id: int) -> Optional[int]:
        for idx, daimon in enumerate(self.npc_daimon_inventory_storage):
            if daimon.daimon_bonded_id == daimon_bonded_id:
                return idx
        return None
    
@dataclass(kw_only=True)
class NPCQuestMainInventory():
    """Represents a NPCQuestMainInventory and its attributes."""

    npc_quest_main_inventory_id      : int
    npc_quest_main_inventory_storage : List[QuestMain] = field(default_factory=list)

    # --------------------------------------------------
    # Create NPCQuestMainInventory from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "NPCQuestMainInventory":
        return cls(
            npc_quest_main_inventory_id = d.get("npc_quest_main_inventory_id"),
            npc_quest_main_inventory_storage = [
                QuestMain.from_dict(q) for q in d.get("npc_quest_main_inventory_storage", [])
            ],
        )
    
    # --------------------------------------------------
    # Convert NPCQuestMainInventory to dictionary
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "npc_quest_main_inventory_id": self.npc_quest_main_inventory_id,
            "npc_quest_main_inventory_storage": [
                quest_main.to_dict() for quest_main in self.npc_quest_main_inventory_storage
            ]
        }
    
    def prepopulate_quest_main_from_templates(self, templates=None):
        """Initialize an empty NPCQuestMainInventory for a new or missing NPCQuestMainInventory."""
        self.npc_quest_main_inventory_storage = []

@dataclass(kw_only=True)
class NPCQuestSideInventory():
    """Represents a NPCQuestSideInventory and its attributes."""

    npc_quest_side_inventory_id      : int
    npc_quest_side_inventory_storage : List[QuestSide] = field(default_factory=list)

    # --------------------------------------------------
    # Create NPCQuestSideInventory from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "NPCQuestSideInventory":
        return cls(
            npc_quest_side_inventory_id = d.get("npc_quest_side_inventory_id"),
            npc_quest_side_inventory_storage = [
                QuestSide.from_dict(q) if isinstance(q, dict) else q
                for q in d.get("npc_quest_side_inventory_storage", [])
            ],
        )
    
    # --------------------------------------------------
    # Convert NPCQuestSideInventory to dictionary
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "npc_quest_side_inventory_id": self.npc_quest_side_inventory_id,
            "npc_quest_side_inventory_storage": [
                quest_side.to_dict() for quest_side in self.npc_quest_side_inventory_storage
            ]
        }
    
    def prepopulate_quest_side_from_templates(self, templates=None):
        """Initialize an empty NPCQuestSideInventory for a new or missing NPCQuestSideInventory."""
        self.npc_quest_side_inventory_storage = []
        
@dataclass(kw_only=True)
class NPC(): # They need to be able to go on their own adventures, catch their own Daimon, add items to their inventory, and buy things. These actions will be determined by a chance to adventure.
    """Represents an NPC and its attributes."""

    npc_id: int                                      # Unique NPC ID             # Example: 1
    npc_name: str                                    # Unique NPC Name           # Example: "William Turner"
    npc_gender: str                                  # NPC Gender                # Example: "Male"
    npc_type: str                                    # NPC Type                  # Example: Merchant
    npc_money: int                                   # NPC Money                 # Example: 100
    npc_location: Location                           # NPC Location              # Example: Location
    npc_item_inventory: NPCItemInventory             # NPC Item Inventory        # Example: NPCItemInventory
    npc_daimon_dex: NPCDaimonDex                     # NPC Daimon Dex            # Example: NPCDaimonDex
    npc_daimon_inventory: NPCDaimonInventory         # NPC Daimon Inventory      # Example: NPCDaimonInventory
    npc_quest_main_inventory: NPCQuestMainInventory  # NPC Main Quest Inventory  # Example: [{"quest_id": 1, "quest_status": "Complete"}]
    npc_quest_side_inventory: NPCQuestMainInventory  # NPC Side Quest Inventory  # Example: [{"quest_id": 1, "quest_status": "Complete"}]
    
    # --------------------------------------------------
    # Create NPC from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict):
        npc_id                   = d.get("npc_id")
        npc_name                 = d.get("npc_name")

        # Try to load objects
        daimon_dex = get_npc_daimon_dex_by_id(d.get("npc_daimon_dex_id"))
        daimon_inventory = get_npc_daimon_inventory_by_id(d.get("npc_daimon_inventory_id"))
        item_inventory = get_npc_item_inventory_by_id(d.get("npc_item_inventory_id"))

        # --- Load linked data or prepopulate if missing ---
        item_inventory = get_npc_item_inventory_by_id(d.get("npc_item_inventory_id"))
        if item_inventory is None:
            item_inventory = NPCItemInventory(npc_item_inventory_id=npc_id)
            item_inventory.prepopulate_generic_items_from_templates(item_template_global)
            npc_item_inventory_global.append(item_inventory)
            print(f"⚙️ Created default ItemInventory for NPC {npc_name}")

        daimon_dex = get_npc_daimon_dex_by_id(d.get("npc_daimon_dex_id"))
        if daimon_dex is None:
            daimon_dex = NPCDaimonDex(npc_daimon_dex_id=npc_id)
            daimon_dex.prepopulate_dex_entries_from_templates(daimon_template_global)
            npc_daimon_dex_global.append(daimon_dex)
            print(f"⚙️ Created default DaimonDex for NPC {npc_name}")

        daimon_inventory = get_npc_daimon_inventory_by_id(d.get("npc_daimon_inventory_id"))
        if daimon_inventory is None:
            daimon_inventory = NPCDaimonInventory(npc_daimon_inventory_id=npc_id)
            daimon_inventory.prepopulate_daimon_from_templates()
            npc_daimon_inventory_global.append(daimon_inventory)
            print(f"⚙️ Created empty DaimonInventory for NPC {npc_name}") 

        quest_main_inventory = get_npc_quest_main_inventory_by_id(d.get("npc_quest_main_inventory_id"))
        if quest_main_inventory is None:
            quest_main_inventory = NPCQuestMainInventory(npc_quest_main_inventory_id=npc_id)
            quest_main_inventory.prepopulate_quest_main_from_templates()
            npc_quest_main_inventory_global.append(quest_main_inventory)
            print(f"⚙️ Created empty QuestMainInventory for NPC {npc_name}")

        quest_side_inventory = get_npc_quest_side_inventory_by_id(d.get("npc_quest_side_inventory_id"))
        if quest_side_inventory is None:
            quest_side_inventory = NPCQuestSideInventory(npc_quest_side_inventory_id=npc_id)
            quest_side_inventory.prepopulate_quest_side_from_templates()
            npc_quest_side_inventory_global.append(quest_side_inventory)
            print(f"⚙️ Created empty QuestSideInventory for NPC {npc_name}")  

        return cls(
            npc_id                   = d.get("npc_id"),
            npc_name                 = d.get("npc_name"),
            npc_gender               = d.get("npc_gender"),
            npc_type                 = d.get("npc_type"),
            npc_money                = d.get("npc_money"),
            npc_location             = get_location_by_id(d.get("npc_location_id")),
            npc_item_inventory       = item_inventory, #get_npc_item_inventory_by_id(d.get("npc_item_inventory_id")),
            npc_daimon_dex           = daimon_dex, #get_npc_daimon_dex_by_id(d.get("npc_daimon_dex_id")),
            npc_daimon_inventory     = daimon_inventory, #get_npc_daimon_inventory_by_id(d.get("npc_daimon_inventory_id")),
            npc_quest_main_inventory = quest_main_inventory,
            npc_quest_side_inventory = quest_side_inventory    
        )
    
    # --------------------------------------------------
    # Convert NPC object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "npc_id"                      : self.npc_id,
            "npc_name"                    : self.npc_name,
            "npc_gender"                  : self.npc_gender,
            "npc_type"                    : self.npc_type,
            "npc_money"                   : self.npc_money,
            "npc_location_id"             : self.npc_location.location_id,
            "npc_daimon_dex_id"           : self.npc_daimon_dex.npc_daimon_dex_id,
            "npc_daimon_inventory_id"     : self.npc_daimon_inventory.npc_daimon_inventory_id,
            "npc_item_inventory_id"       : self.npc_item_inventory.npc_item_inventory_id,
            "npc_quest_main_inventory_id" : self.npc_quest_main_inventory.npc_quest_main_inventory_id,
            "npc_quest_side_inventory_id" : self.npc_quest_side_inventory.npc_quest_side_inventory_id
        }
    
    # Class-level set to track used names
    _used_names = set()

    def __post_init__(self):
        if self.npc_name in NPC._used_names:
            raise ValueError(f"Duplicate npc name '{self.npc_name}' detected.")
        NPC._used_names.add(self.npc_name)
 
    def add_item_to_npc_item_inventory(self, item: Item) -> bool:
        """
        Adds an item (generic or unique) to the NPC's inventory.
        Automatically routed by NPCItemInventory.
        """
        return self.npc_item_inventory.add_item(item)

    def subtract_item_from_npc_item_inventory(self, item: Item, quantity: int = 1) -> bool:
        """
        Removes or subtracts an item (generic or unique) from the NPC's inventory.
        Automatically routed by NPCItemInventory.
        """
        return self.npc_item_inventory.subtract_item(item, quantity)

    def update_npc_money(self, money_amount: int) -> bool:
        """Add or subtract a NPC's money."""
        if isinstance(money_amount, int) or money_amount != 0:
            if money_amount > 0:
                print(f"{self.npc_name} added ${money_amount}. Total: {self.npc_money}")
                self.npc_money = self.npc_money + money_amount
            elif money_amount < 0 and self.npc_money + money_amount < 0:
                print(f"{self.npc_name} does not have ${money_amount} to subtract. Total: {self.npc_money}")
            elif money_amount < 0:
                print(f"{self.npc_name} subtracted ${money_amount}. Total: {self.npc_money}")
                self.npc_money = self.npc_money + money_amount
        else:
            print(f"❌ Invalid NPC money update amount: {amount}.")

    def catch_daimon_unbonded(self, daimon_unbonded: "DaimonUnbonded") -> Optional["NPC"]:
        """
        NPC catches a DaimonUnbonded.
        Converts it to a DaimonBonded and adds it to the NPC's inventory.
        Always adds to team if space is available, otherwise adds to storage.
        Returns self on success.
        """

        bonded_daimon = DaimonBonded(
            daimon_bonded_id                    = len(self.npc_daimon_inventory.npc_daimon_inventory_team)+len(self.npc_daimon_inventory.npc_daimon_inventory_storage)+1,
            daimon_bonded_daimon_template_id    = daimon_unbonded.daimon_unbonded_daimon_template_id,
            daimon_bonded_species               = daimon_unbonded.daimon_unbonded_species,
            daimon_bonded_level                 = daimon_unbonded.daimon_unbonded_level,
            daimon_bonded_level_progress        = daimon_unbonded.daimon_unbonded_level_progress,
            daimon_bonded_gender                = daimon_unbonded.daimon_unbonded_gender,
            daimon_bonded_height                = daimon_unbonded.daimon_unbonded_height,
            daimon_bonded_weight                = daimon_unbonded.daimon_unbonded_weight,
            daimon_bonded_max_health            = daimon_unbonded.daimon_unbonded_max_health,
            daimon_bonded_current_health        = daimon_unbonded.daimon_unbonded_current_health,
            daimon_bonded_status        = daimon_unbonded.daimon_unbonded_status,
            daimon_bonded_stat_health           = daimon_unbonded.daimon_unbonded_stat_health,
            daimon_bonded_stat_physical_attack  = daimon_unbonded.daimon_unbonded_stat_physical_attack,
            daimon_bonded_stat_special_attack   = daimon_unbonded.daimon_unbonded_stat_special_attack,
            daimon_bonded_stat_physical_defense = daimon_unbonded.daimon_unbonded_stat_physical_defense,
            daimon_bonded_stat_special_defense  = daimon_unbonded.daimon_unbonded_stat_special_defense,
            daimon_bonded_stat_speed            = daimon_unbonded.daimon_unbonded_stat_speed,
            daimon_bonded_type_1                = daimon_unbonded.daimon_unbonded_type_1,
            daimon_bonded_type_2                = daimon_unbonded.daimon_unbonded_type_2,
            daimon_bonded_ability               = daimon_unbonded.daimon_unbonded_ability,
            daimon_bonded_move_1                = daimon_unbonded.daimon_unbonded_move_1,
            daimon_bonded_move_2                = daimon_unbonded.daimon_unbonded_move_2,
            daimon_bonded_move_3                = daimon_unbonded.daimon_unbonded_move_3,
            daimon_bonded_move_4                = daimon_unbonded.daimon_unbonded_move_4,
            daimon_bonded_item                  = daimon_unbonded.daimon_unbonded_item,
            daimon_bonded_nickname              = daimon_unbonded.daimon_unbonded_species
        )

        # Add to NPCDaimonInventory
        self.npc_daimon_inventory.add_daimon_to_npc_daimon_inventory(bonded_daimon)

        # If this is the first Daimon caught, make it the follower
        if bonded_daimon.daimon_bonded_id == 1:
            self.npc_daimon_inventory.set_follower(bonded_daimon)

        # Remove DaimonUnbonded from daimon_unbonded_global
        if daimon_unbonded in daimon_unbonded_global:
            daimon_unbonded_global.remove(daimon_unbonded)

        print(f"🎉 {self.npc_name} caught {bonded_daimon.daimon_bonded_species}!")
        return self
    
    def assign_daimon_team(self, daimon_team: list["DaimonUnbonded"]) -> "NPC":
        """
        Assigns a full team of DaimonUnbonded to this NPC.
        Converts each to DaimonBonded using the catch_daimon_unbonded() method.
        Automatically handles follower assignment if applicable.
        """

        # Go through each DaimonUnbonded in the provided team
        for daimon_unbonded in daimon_team:
            self.catch_daimon_unbonded(daimon_unbonded)

        print(f"✅ {self.npc_name} has been assigned {len(daimon_team)} Daimon.")
        return self
    
    def add_quest_side_to_npc_quest_side_inventory(self, quest_side: "QuestSide") -> bool:
        """
        Adds a QuestSide to the NPC's side quest inventory if not already present.
        Removes the quest from the global quest_side_global list upon success.
        Returns True if successfully added, False otherwise.
        """

        # Add the quest to the NPC's side quest inventory
        quest_side.quest_side_id = len(self.npc_quest_side_inventory.npc_quest_side_inventory_storage) + 1
        self.npc_quest_side_inventory.npc_quest_side_inventory_storage.append(quest_side)
        print(f"🗺️ Added side quest '{quest_side.quest_side_name}' to {self.npc_name}'s quest inventory.")

        # Remove it from the global quest pool if it exists there
        if quest_side in quest_side_global:
            quest_side_global.remove(quest_side)
            print(f"📦 Removed '{quest_side.quest_side_name}' from global quest pool.")

        return True

    def take_battle_turn(self, battle: "SystemDaimonBattle"):
        """
        NPC takes its turn in the SystemDaimonBattle.
        Automatically selects moves, switches Daimons, or uses items as appropriate.
        """
        active_team = battle.get_active_daimons_for_participant(self)
        opponents = battle.get_opponents_for_participant(self)

        if not active_team:
            print(f"⚠️ {self.npc_name} has no active Daimons to take a turn!")
            return

        print(f"🤖 {self.npc_name}'s turn begins with {len(active_team)} Daimon(s).")

        for daimon in active_team:
            # Skip fainted Daimons
            if daimon.daimon_bonded_current_health <= 0:
                print(f"💀 {daimon.daimon_bonded_nickname} is fainted and cannot act.")
                continue

            import random
            choice = random.choice(["fight", "item", "switch"])

            # 🥊 FIGHT — use a move or fallback to Struggle
            if choice == "fight":
                if hasattr(daimon, "daimon_bonded_moves") and daimon.daimon_bonded_moves:
                    available_moves = [m for m in daimon.daimon_bonded_moves if m.daimon_move_points_current > 0]
                    if available_moves:
                        move = random.choice(available_moves)
                        move.daimon_move_points_current -= 1
                    else:
                        move = None
                else:
                    move = None

                # ⚔️ If no valid moves, use Struggle
                if move is None:
                    move = get_daimon_move_by_id(8) #Struggle
                    print(f"💢 {daimon.daimon_bonded_nickname} has no moves left! It used Struggle!")

                # Pick a target
                if opponents:
                    target = random.choice(opponents)
                    battle.execute_move(daimon, target, move)

            # 🎁 ITEM — try to use a potion
            elif choice == "item" and getattr(self, "npc_item_inventory_storage_generic", []):
                potions = [
                    i for i in self.npc_item_inventory_storage_generic
                    if "Potion" in i.item_name and i.item_quantity > 0
                ]
                if potions:
                    item = potions[0]
                    battle.execute_item(self, item, daimon)
                    item.item_quantity -= 1
                else:
                    print(f"🧾 {self.npc_name} tried to use an item, but has none available.")

            # 🔁 SWITCH — change Daimons if possible
            elif choice == "switch" and hasattr(self, "npc_daimon_inventory"):
                team = self.npc_daimon_inventory.npc_daimon_inventory_team
                available = [d for d in team if d not in active_team and d.daimon_bonded_current_health > 0]
                if available:
                    new_daimon = random.choice(available)
                    battle.switch_daimon(self, daimon, new_daimon)
                else:
                    print(f"🔁 {self.npc_name} has no Daimons available to switch to.")

@dataclass(kw_only=True)
class PlayerItemInventory():
    """Represents an PlayerItemInventory and its attributes."""

    player_item_inventory_id              : int
    player_item_inventory_storage_generic : List[Item] = field(default_factory=list)
    player_item_inventory_storage_unique  : List[Item] = field(default_factory=list)

    # --------------------------------------------------
    # Create PlayerItemInventory object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "PlayerItemInventory":
        return cls(
            player_item_inventory_id              = d.get("player_item_inventory_id"),
            player_item_inventory_storage_generic = [Item.from_dict(item_dict) for item_dict in d.get("player_item_inventory_storage_generic", [])],
            player_item_inventory_storage_unique  = [Item.from_dict(item_dict) for item_dict in d.get("player_item_inventory_storage_unique", [])]
        )
    
    # --------------------------------------------------
    # Convert PlayerItemInventory object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "player_item_inventory_id"              : self.player_item_inventory_id,
            "player_item_inventory_storage_generic" : [item.to_dict() for item in self.player_item_inventory_storage_generic],
            "player_item_inventory_storage_unique"  : [item.to_dict() for item in self.player_item_inventory_storage_unique]
        }

    def prepopulate_generic_items_from_templates(self, templates: List["ItemTemplate"]):
        """Initialize an empty PlayerItemInventory for a new or missing PlayerItemInventory."""
        self.player_item_inventory_storage_generic = [
            Item(
                item_id          = item_template.item_template_id,
                item_name        = item_template.item_template_name,
                item_description = item_template.item_template_description,
                item_category    = item_template.item_template_category,
                item_actions     = item_template.item_template_actions,
                item_base_value  = item_template.item_template_base_value,
                item_hex_code_1  = item_template.item_template_base_hex_code_1,
                item_hex_code_2  = item_template.item_template_base_hex_code_2,
                item_hex_code_3  = item_template.item_template_base_hex_code_3,
                item_hex_code_4  = item_template.item_template_base_hex_code_4,
                item_hex_code_5  = item_template.item_template_base_hex_code_5,
                item_hex_code_6  = item_template.item_template_base_hex_code_6,
                item_hex_code_7  = item_template.item_template_base_hex_code_7,
                item_hex_code_8  = item_template.item_template_base_hex_code_8,
                item_hex_code_9  = item_template.item_template_base_hex_code_9,
                item_hex_code_10 = item_template.item_template_base_hex_code_10,
                item_quantity    = 0
            )
            for item_template in templates if item_template.item_template_category in ITEM_CATEGORY_GENERIC
        ]

    def add_item_to_player_item_inventory(self, item: Item) -> bool:
        """
        Adds/modifies an Item object to the PlayerItemInventory.
        Generic items are prepopulated — modify existing Item object.
        Unique items are not prepopulated - add new Item object.
        Only allows items that exist in item_template_global.
        """
        # ---------------------------
        # Validate Item.item_quantity within acceptable range
        # ---------------------------
        if 1 <= item.item_quantity <= 1_000_000:
            print(f"⚠️ Invalid quantity {item.item_quantity}. Must be 1–1,000,000.")
            return False

        # ---------------------------
        # Validate Item is legitimate
        # ---------------------------
        if not any(template.item_template_id == item.item_id for template in item_template_global):
            print(f"⚠️ Cannot subtract item {item.item_name} (ID: {item.item_id}) — not found in item_template_global.")
            return False
        
        # ---------------------------
        # Validate Item is legitimate
        # ---------------------------
        if not any(template.item_template_id == item.item_id for template in item_template_global):
            print(f"⚠️ Cannot add item {item.item_name} (ID: {item.item_id}) — not found in item_template_global.")
            return False

        # ---------------------------
        # Unique Item
        # ---------------------------
        if item.item_category in ITEM_CATEGORY_UNIQUE:
            self.player_item_inventory_storage_unique.append(item)
            print(f"💎 Added unique item: {item.item_name} (Category: {item.item_category}, Hex: {getattr(item, 'item_hex_code_1', None)})")
            return True

        # ---------------------------
        # Generic Item
        # ---------------------------
        elif item.item_category in ITEM_CATEGORY_GENERIC:
            # Stackable — merge into existing stack
            for existing_item in self.player_item_inventory_storage_generic:
                if existing_item.item_id == item.item_id:
                    max_quantity = 1_000_000
                    new_quantity = existing_item.item_quantity + item.item_quantity
                    if new_quantity > max_quantity:
                        added_quantity = max_quantity - existing_item.item_quantity
                        existing_item.item_quantity = max_quantity
                        print(f"⚠️ Too much {item.item_name}. Added {added_quantity}, capped at {max_quantity}.")
                    else:
                        existing_item.item_quantity = new_quantity
                        print(f"✅ Added {item.item_quantity}x {item.item_name}. Total: {existing_item.item_quantity}.")
                    return True
    
    def subtract_item_from_player_item_inventory(self, item: Item, quantity: int) -> bool:
        """
        Removes/modifies an Item object to the PlayerItemInventory.
        Generic items are prepopulated — modify existing Item object.
        Unique items are not prepopulated - remove existing Item object.
        Only allows items that exist in item_template_global.
        """

        # ---------------------------
        # Validate quantity within acceptable range
        # ---------------------------
        if 1 <= quantity <= 1_000_000:
            print(f"⚠️ Invalid quantity {quantity}. Must be 1–1,000,000.")
            return False

        # ---------------------------
        # Validate Item is legitimate
        # ---------------------------
        if not any(template.item_template_id == item.item_id for template in item_template_global):
            print(f"⚠️ Cannot subtract item {item.item_name} (ID: {item.item_id}) — not found in item_template_global.")
            return False

        # ---------------------------
        # Unique Item
        # ---------------------------
        if item.item_category in ITEM_CATEGORY_UNIQUE:
            if item in self.player_item_inventory_storage_unique:
                self.player_item_inventory_storage_unique.remove(item)
                print(f"🗑️ Removed unique item: {item.item_name} (Hex: {getattr(item, 'item_hex_code_1', None)})")
                return True
            else:
                print(f"⚠️ Unique item {item.item_name} not found in inventory.")
                return False

        # ---------------------------
        # Generic Item
        # ---------------------------
        elif item.item_category in ITEM_CATEGORY_GENERIC:
            for existing_item in self.player_item_inventory_storage_generic:
                if existing_item.item_id == item.item_id:
                    if existing_item.item_quantity >= quantity:
                        existing_item.item_quantity -= quantity
                        print(f"✅ Subtracted {quantity}x {item.item_name}. Remaining: {existing_item.item_quantity}")
                        # Do not remove the item if quantity reaches 0
                        return True
                    else:
                        print(f"⚠️ Not enough {item.item_name} to subtract {quantity}. Only have {existing_item.item_quantity}.")
                        return False

@dataclass(kw_only=True)
class PlayerDaimonDexEntry():
    """Represents a PlayerDaimonDexEntry and its attributes."""

    player_daimon_dex_entry_id: int
    player_daimon_dex_entry_daimon_template_id: Union[str, int]                                                      # Unique Daimon Template ID            # Example: 1
    player_daimon_dex_entry_daimon_template_species: Union[str, int] = "???"                                         # Unique Daimon Template Species       # Example: "Palanine"
    player_daimon_dex_entry_daimon_template_evolution_1: Union[str, List[Dict[str, Union[int, Item]]]] = "???"       # Unique Daimon Template Evolution 1   # Example: "daimon_template_evolution_1": [{"daimon_template_evolution_level": 1, "daimon_template_evolution_requirement_item_id": 1, "daimon_template_evolution_id": 1}],
    player_daimon_dex_entry_daimon_template_evolution_2: Union[str, List[Dict[str, Union[int, Item]]]] = "???"       # Unique Daimon Template Evolution 2   # Example: "daimon_template_evolution_2": [{"daimon_template_evolution_level": 2, "daimon_template_evolution_requirement_item_id": 2, "daimon_template_evolution_id": 2}],
    player_daimon_dex_entry_daimon_template_evolution_3: Union[str, List[Dict[str, Union[int, Item]]]] = "???"       # Unique Daimon Template Evolution 3   # Example: "daimon_template_evolution_3": [{"daimon_template_evolution_level": 3, "daimon_template_evolution_requirement_item_id": 3, "daimon_template_evolution_id": 3}],
    player_daimon_dex_entry_daimon_template_gender_distribution: Union[str, Dict[str, float]] = "???"                # Daimon Template Gender Distribution  # Example: {"Male": 0.5, "Female": 0.5},
    player_daimon_dex_entry_daimon_template_height_distribution: Union[str, Dict[str, float]] = "???"                # Daimon Template Weight Distribution  # Example: {"daimon_template_height_mean": 0.75, "daimon_template_height_range": 0.15},
    player_daimon_dex_entry_daimon_template_weight_distribution: Union[str, Dict[str, float]] = "???"                # Daimon Template Height Distribution  # Example: {"daimon_template_weight_mean": 15, "daimon_template_weight_range": 1.5},
    player_daimon_dex_entry_daimon_template_type_1: Union[str, DaimonType] = "???"                                   # Daimon Template Type ID 1            # Example: DaimonType
    player_daimon_dex_entry_daimon_template_type_2: Union[str, Optional[DaimonType]] = "???"                         # Daimon Template Type ID 2            # Example: DaimonType
    player_daimon_dex_entry_daimon_template_ability: Union[str, DaimonAbility] = "???"                               # Daimon Template Ability ID           # Example: DaimonAbility
    player_daimon_dex_entry_daimon_template_move_template_pool: Union[str, List[DaimonMove]] = "???"                 # Daimon Template Move Pool            # Example: DaimonMove
    player_daimon_dex_entry_daimon_template_item_template_pool: Union[str, List[Dict[float, ItemTemplate]]] = "???"  # Daimon Template Item Pool            # Example: [{"item_weight": 0.1, ItemTemplate}]                                                                 
    
    # --------------------------------------------------
    # Create PlayerDaimonDexEntry from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "PlayerDaimonDexEntry":
        return cls(
            player_daimon_dex_entry_id                                  = d.get("player_daimon_dex_entry_id"),
            player_daimon_dex_entry_daimon_template_id                  = d.get("player_daimon_dex_entry_daimon_template_id"),
            player_daimon_dex_entry_daimon_template_species             = d.get("player_daimon_dex_entry_daimon_template_species", "???"),
            player_daimon_dex_entry_daimon_template_evolution_1         = d.get("player_daimon_dex_entry_daimon_template_evolution_1", "???"),
            player_daimon_dex_entry_daimon_template_evolution_2         = d.get("player_daimon_dex_entry_daimon_template_evolution_2", "???"),
            player_daimon_dex_entry_daimon_template_evolution_3         = d.get("player_daimon_dex_entry_daimon_template_evolution_3", "???"),
            player_daimon_dex_entry_daimon_template_gender_distribution = d.get("player_daimon_dex_entry_daimon_template_gender_distribution", "???"),
            player_daimon_dex_entry_daimon_template_height_distribution = d.get("player_daimon_dex_entry_daimon_template_height_distribution", "???"),
            player_daimon_dex_entry_daimon_template_weight_distribution = d.get("player_daimon_dex_entry_daimon_template_weight_distribution", "???"),
            player_daimon_dex_entry_daimon_template_type_1              = d.get("player_daimon_dex_entry_daimon_template_type_1", "???"),
            player_daimon_dex_entry_daimon_template_type_2              = d.get("player_daimon_dex_entry_daimon_template_type_2", "???"),
            player_daimon_dex_entry_daimon_template_ability             = d.get("player_daimon_dex_entry_daimon_template_ability", "???"),
            player_daimon_dex_entry_daimon_template_move_template_pool  = d.get("player_daimon_dex_entry_daimon_template_move_template_pool", "???"),
            player_daimon_dex_entry_daimon_template_item_template_pool  = d.get("player_daimon_dex_entry_daimon_template_item_template_pool", "???")
        )
    
    # --------------------------------------------------
    # Convert PlayerDaimonDexEntry object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "player_daimon_dex_entry_id"                                  : self.player_daimon_dex_entry_id,
            "player_daimon_dex_entry_daimon_template_id"                  : self.player_daimon_dex_entry_daimon_template_id,
            "player_daimon_dex_entry_daimon_template_species"             : self.player_daimon_dex_entry_daimon_template_species,
            "player_daimon_dex_entry_daimon_template_evolution_1"         : self.player_daimon_dex_entry_daimon_template_evolution_1,
            "player_daimon_dex_entry_daimon_template_evolution_2"         : self.player_daimon_dex_entry_daimon_template_evolution_2,
            "player_daimon_dex_entry_daimon_template_evolution_3"         : self.player_daimon_dex_entry_daimon_template_evolution_3,
            "player_daimon_dex_entry_daimon_template_gender_distribution" : self.player_daimon_dex_entry_daimon_template_gender_distribution,
            "player_daimon_dex_entry_daimon_template_height_distribution" : self.player_daimon_dex_entry_daimon_template_height_distribution,
            "player_daimon_dex_entry_daimon_template_weight_distribution" : self.player_daimon_dex_entry_daimon_template_weight_distribution,
            "player_daimon_dex_entry_daimon_template_type_1"              : self.player_daimon_dex_entry_daimon_template_type_1,
            "player_daimon_dex_entry_daimon_template_type_2"              : self.player_daimon_dex_entry_daimon_template_type_2,
            "player_daimon_dex_entry_daimon_template_ability"             : self.player_daimon_dex_entry_daimon_template_ability,
            "player_daimon_dex_entry_daimon_template_move_template_pool"  : self.player_daimon_dex_entry_daimon_template_move_template_pool,
            "player_daimon_dex_entry_daimon_template_item_template_pool"  : self.player_daimon_dex_entry_daimon_template_item_template_pool
        }
    
@dataclass(kw_only=True)
class PlayerDaimonDex():
    """Represents a PlayerDaimonDex and its attributes."""

    player_daimon_dex_id: int
    player_daimon_dex_dex: List[PlayerDaimonDexEntry] = field(default_factory=list)

    # --------------------------------------------------
    # Create PlayerDaimonDex object from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "PlayerDaimonDex":
        return cls(
            player_daimon_dex_id  = d.get("player_daimon_dex_id"),
            player_daimon_dex_dex = [PlayerDaimonDexEntry.from_dict(entry) for entry in d.get("player_daimon_dex_dex", [])]
        )
    
    # --------------------------------------------------
    # Convert PlayerDaimonDex object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "player_daimon_dex_id"  : self.player_daimon_dex_id,
            "player_daimon_dex_dex" : [dex.to_dict() for dex in self.player_daimon_dex_dex]
        }
    
    def prepopulate_dex_entries_from_templates(self, templates: List["DaimonTemplate"]):
        """Initialize an empty PlayerDaimonDex for a new or missing PlayerDaimonDex."""
        self.player_daimon_dex_dex.clear()
        for template in templates:
            entry = PlayerDaimonDexEntry(
                player_daimon_dex_entry_id                                  = len(self.player_daimon_dex_dex) + 1,
                player_daimon_dex_entry_daimon_template_id                  = template.daimon_template_id,
                player_daimon_dex_entry_daimon_template_species             = "???",
                player_daimon_dex_entry_daimon_template_evolution_1         = "???",
                player_daimon_dex_entry_daimon_template_evolution_2         = "???",
                player_daimon_dex_entry_daimon_template_evolution_3         = "???",
                player_daimon_dex_entry_daimon_template_gender_distribution = "???",
                player_daimon_dex_entry_daimon_template_height_distribution = "???",
                player_daimon_dex_entry_daimon_template_weight_distribution = "???",
                player_daimon_dex_entry_daimon_template_type_1              = "???",
                player_daimon_dex_entry_daimon_template_type_2              = "???",
                player_daimon_dex_entry_daimon_template_ability_pool        = "???",
                player_daimon_dex_entry_daimon_template_move_template_pool  = "???",
                player_daimon_dex_entry_daimon_template_item_template_pool  = "???"
            )
            self.player_daimon_dex_dex.append(entry)

@dataclass(kw_only=True)
class PlayerDaimonInventory():
    """Represents a PlayerDaimonInventory and its attributes. """

    player_daimon_inventory_id       : int
    player_daimon_inventory_follower : Optional[DaimonBonded] = None
    player_daimon_inventory_team     : List[DaimonBonded] = field(default_factory=list)
    player_daimon_inventory_storage  : List[DaimonBonded] = field(default_factory=list)

    # --------------------------------------------------
    # Create PlayerDaimonInventory from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "PlayerDaimonInventory":
        return cls(
            player_daimon_inventory_id = d.get("player_daimon_inventory_id"),
            player_daimon_inventory_follower = (
                DaimonBonded.from_dict(d["player_daimon_inventory_follower"])
                if d.get("player_daimon_inventory_follower") else None
            ),
            player_daimon_inventory_team = [
                DaimonBonded.from_dict(b) if isinstance(b, dict) else b
                for b in d.get("player_daimon_inventory_team", [])
            ],
            player_daimon_inventory_storage = [
                DaimonBonded.from_dict(b) if isinstance(b, dict) else b
                for b in d.get("player_daimon_inventory_storage", [])
            ],
        )
    
    # --------------------------------------------------
    # Convert PlayerDaimonInventory to dictionary
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "player_daimon_inventory_id": self.player_daimon_inventory_id,
            "player_daimon_inventory_follower": (
                self.player_daimon_inventory_follower.to_dict()
                if self.player_daimon_inventory_follower
                else None
            ),
            "player_daimon_inventory_team": [
                daimon.to_dict() for daimon in self.player_daimon_inventory_team
            ],
            "player_daimon_inventory_storage": [
                daimon.to_dict() for daimon in self.player_daimon_inventory_storage
            ]
        }
    
    def prepopulate_daimon_from_templates(self, templates=None):
        """Initialize an empty PlayerDaimonInventory for a new or missing PlayerDaimonInventory."""
        self.player_daimon_inventory_follower = None
        self.player_daimon_inventory_team = []
        self.player_daimon_inventory_storage = []
    
    # ---------- Core Management ----------
    def set_follower(self, daimon_bonded: "DaimonBonded") -> bool:
        if self.player_daimon_inventory_follower is not None:
            print(f"⚠️ Follower already set: {self.player_daimon_inventory_follower.daimon_bonded_nickname}. Remove first.")
            return False
        self.player_daimon_inventory_follower = daimon_bonded
        print(f"✅ {daimon_bonded.daimon_bonded_nickname} is now following the player.")
        return True

    def remove_follower(self) -> bool:
        if not self.player_daimon_inventory_follower:
            print("⚠️ No follower to remove.")
            return False
        print(f"👋 {self.player_daimon_inventory_follower.daimon_bonded_nickname} is no longer following.")
        self.player_daimon_inventory_follower = None
        return True

    def set_daimon_nickname(self, daimon_bonded_id: int, new_nickname: str) -> bool:
        for daimon in self.player_daimon_inventory_team:
            if daimon.daimon_bonded_id == daimon_bonded_id:
                old_nickname = daimon.daimon_bonded_nickname
                daimon.daimon_bonded_nickname = new_nickname
                print(f"✏️ Daimon '{old_nickname}' renamed to '{new_nickname}'.")
                return True
        print(f"⚠️ Daimon ID {daimon_bonded_id} not found in team.")
        return False

    def add_daimon_to_player_daimon_inventory(self, daimon_bonded: DaimonBonded) -> bool:
        """
        Add a Daimon to the player's inventory.
        - If the team has fewer than 6 Daimon, prompts the player to choose team or storage.
        - If the team is full, automatically sends to storage.

        Returns True if added to team, False if added to storage.
        """
        if len(self.player_daimon_inventory_team) >= 6:
            # Team is full, automatically go to storage
            self.player_daimon_inventory_storage.append(daimon_bonded)
            print(f"⚠️ Team full. {daimon_bonded.daimon_bonded_species} sent to storage.")
            return False

        # Team has space, prompt player
        while True:
            choice = input(f"Place {daimon_bonded.daimon_bonded_species} in team or storage? (team/storage): ").strip().lower()
            if choice in ["team", "storage"]:
                break
            print("⚠️ Invalid input. Please type 'team' or 'storage'.")

        if choice == "team":
            self.player_daimon_inventory_team.append(daimon_bonded)
            print(f"✅ {daimon_bonded.daimon_bonded_species} added to team.")
            return True
        else:
            self.player_daimon_inventory_storage.append(daimon_bonded)
            print(f"✅ {daimon_bonded.daimon_bonded_species} added to storage.")
            return False
        
    def move_daimon_to_team_from_storage(self, daimon: DaimonBonded) -> bool:
        """Move a Daimon from storage to team."""
        if len(self.player_daimon_inventory_team) >= 6:
            print("⚠️ Team is full. Cannot move Daimon from storage.")
            return False

        if daimon in self.player_daimon_inventory_storage:
            self.player_daimon_inventory_storage.remove(daimon)
            self.player_daimon_inventory_team.append(daimon)
            print(f"📤 {daimon.daimon_bonded_species} moved from storage to team.")
            return True

        print(f"⚠️ {daimon.daimon_bonded_species} not found in storage.")
        return False

    def move_daimon_to_storage_from_team(self, daimon: DaimonBonded) -> bool:
        """Move a Daimon from team to storage."""
        if daimon in self.player_daimon_inventory_team:
            self.player_daimon_inventory_team.remove(daimon)
            self.player_daimon_inventory_storage.append(daimon)
            print(f"📦 {daimon.daimon_bonded_species} moved to storage.")
            return True

        print(f"⚠️ {daimon.daimon_bonded_species} not found in team.")
        return False

    def switch_daimon_in_team_and_storage(self, team_daimon: DaimonBonded, storage_daimon: DaimonBonded) -> bool:
        """
        Swap a Daimon from the team with one from storage.
        Returns True if successful, False if either Daimon is not found.
        """
        if team_daimon not in self.player_daimon_inventory_team:
            print(f"⚠️ {team_daimon.daimon_bonded_species} not found in team.")
            return False
        if storage_daimon not in self.player_daimon_inventory_storage:
            print(f"⚠️ {storage_daimon.daimon_bonded_species} not found in storage.")
            return False

        # Perform the swap
        self.player_daimon_inventory_team.remove(team_daimon)
        self.player_daimon_inventory_storage.remove(storage_daimon)

        self.player_daimon_inventory_team.append(storage_daimon)
        self.player_daimon_inventory_storage.append(team_daimon)

        print(f"🔄 Swapped {team_daimon.daimon_bonded_species} with {storage_daimon.daimon_bonded_species}.")
        return True

    def get_all_daimons(self) -> List["DaimonBonded"]:
        result = []
        if self.player_daimon_inventory_follower:
            result.append(self.player_daimon_inventory_follower)
        result.extend(self.player_daimon_inventory_team)
        result.extend(self.player_daimon_inventory_storage)
        return result

    def get_daimon_index_in_team(self, daimon_bonded_id: int) -> Optional[int]:
        for idx, daimon in enumerate(self.player_daimon_inventory_team):
            if daimon.daimon_bonded_id == daimon_bonded_id:
                return idx
        return None

    def get_daimon_index_in_storage(self, daimon_bonded_id: int) -> Optional[int]:
        for idx, daimon in enumerate(self.player_daimon_inventory_storage):
            if daimon.daimon_bonded_id == daimon_bonded_id:
                return idx
        return None

@dataclass(kw_only=True)
class PlayerQuestMainInventory():
    """Represents a PlayerQuestMainInventory and its attributes."""

    player_quest_main_inventory_id      : int
    player_quest_main_inventory_storage : List[QuestMain] = field(default_factory=list)

    # --------------------------------------------------
    # Create PlayerQuestMainInventory from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "PlayerQuestMainInventory":
        return cls(
            player_quest_main_inventory_id = d.get("player_quest_main_inventory_id"),
            player_quest_main_inventory_storage = [
                QuestMain.from_dict(q) for q in d.get("player_quest_main_inventory_storage", [])
            ],
        )
    
    # --------------------------------------------------
    # Convert PlayerQuestMainInventory to dictionary
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "player_quest_main_inventory_id": self.player_quest_main_inventory_id,
            "player_quest_main_inventory_storage": [
                quest_main.to_dict() for quest_main in self.player_quest_main_inventory_storage
            ]
        }
    
    def prepopulate_quest_main_from_templates(self, templates=None):
        """Initialize an empty PlayerQuestMainInventory for a new or missing PlayerQuestMainInventory."""
        self.player_quest_main_inventory_storage = []

@dataclass(kw_only=True)
class PlayerQuestSideInventory():
    """Represents a PlayerQuestSideInventory and its attributes."""

    player_quest_side_inventory_id      : int
    player_quest_side_inventory_storage : List[QuestSide] = field(default_factory=list)

    # --------------------------------------------------
    # Create PlayerQuestSideInventory from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict) -> "PlayerQuestSideInventory":
        return cls(
            player_quest_side_inventory_id = d.get("player_quest_side_inventory_id"),
            player_quest_side_inventory_storage = [
                QuestSide.from_dict(q) if isinstance(q, dict) else q
                for q in d.get("player_quest_side_inventory_storage", [])
            ],
        )
    
    # --------------------------------------------------
    # Convert PlayerQuestSideInventory to dictionary
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "player_quest_side_inventory_id": self.player_quest_side_inventory_id,
            "player_quest_side_inventory_storage": [
                quest_side.to_dict() for quest_side in self.player_quest_side_inventory_storage
            ]
        }
    
    def prepopulate_quest_side_from_templates(self, templates=None):
        """Initialize an empty PlayerQuestSideInventory for a new or missing PlayerQuestSideInventory."""
        self.player_quest_side_inventory_storage = []

@dataclass(kw_only=True)
class Player():
    """Represents a Player and its attributes."""

    player_id: int                                           # Unique Player ID             # Example: 1
    player_name: str                                         # Unique Player Name           # Example: "Shay"
    player_gender: str                                       # Player Gender                # Example: "Male"
    player_money: int                                        # Player Money                 # Example: 100
    player_location: Location                                # Player Location              # Example: Location
    player_item_inventory: PlayerItemInventory               # Player Item Inventory        # Example: PlayerItemInventory
    player_daimon_dex: PlayerDaimonDex                       # Player Daimon Dex            # Example: PlayerDaimonDex
    player_daimon_inventory: PlayerDaimonInventory           # Player Daimon Inventory      # Example: PlayerDaimonInventory
    player_quest_main_inventory: PlayerQuestMainInventory    # Player Main Quest Inventory  # Example: [{"quest_id": 1, "quest_status": "Complete"}]
    player_quest_side_inventory: PlayerQuestSideInventory    # Player Side Quest Inventory  # Example: [{"quest_id": 1, "quest_status": "Complete"}]

    # --------------------------------------------------
    # Create Player from dictionary.
    # --------------------------------------------------
    @classmethod
    def from_dict(cls, d: dict):
        player_id                   = d.get("player_id")
        player_name                 = d.get("player_name")

        # Try to load objects
        daimon_dex = get_player_daimon_dex_by_id(d.get("player_daimon_dex_id"))
        daimon_inventory = get_player_daimon_inventory_by_id(d.get("player_daimon_inventory_id"))
        item_inventory = get_player_item_inventory_by_id(d.get("player_item_inventory_id"))

        # --- Load linked data or prepopulate if missing ---
        item_inventory = get_player_item_inventory_by_id(d.get("player_item_inventory_id"))
        if item_inventory is None:
            item_inventory = PlayerItemInventory(player_item_inventory_id=player_id)
            item_inventory.prepopulate_generic_items_from_templates(item_template_global)
            player_item_inventory_global.append(item_inventory)
            print(f"⚙️ Created default ItemInventory for Player {player_name}")  

        daimon_dex = get_player_daimon_dex_by_id(d.get("player_daimon_dex_id"))
        if daimon_dex is None:
            daimon_dex = PlayerDaimonDex(player_daimon_dex_id=player_id)
            daimon_dex.prepopulate_dex_entries_from_templates(daimon_template_global)
            player_daimon_dex_global.append(daimon_dex)
            print(f"⚙️ Created default DaimonDex for Player {player_name}")

        daimon_inventory = get_player_daimon_inventory_by_id(d.get("player_daimon_inventory_id"))
        if daimon_inventory is None:
            daimon_inventory = PlayerDaimonInventory(player_daimon_inventory_id=player_id)
            daimon_inventory.prepopulate_daimon_from_templates()
            player_daimon_inventory_global.append(daimon_inventory)
            print(f"⚙️ Created empty DaimonInventory for Player {player_name}") 

        quest_main_inventory = get_player_quest_main_inventory_by_id(d.get("player_quest_main_inventory_id"))
        if quest_main_inventory is None:
            quest_main_inventory = PlayerQuestMainInventory(player_quest_main_inventory_id=player_id)
            quest_main_inventory.prepopulate_quest_main_from_templates()
            player_quest_main_inventory_global.append(quest_main_inventory)
            print(f"⚙️ Created empty QuestMainInventory for Player {player_name}")

        quest_side_inventory = get_player_quest_side_inventory_by_id(d.get("player_quest_side_inventory_id"))
        if quest_side_inventory is None:
            quest_side_inventory = PlayerQuestSideInventory(player_quest_side_inventory_id=player_id)
            quest_side_inventory.prepopulate_quest_side_from_templates()
            player_quest_side_inventory_global.append(quest_side_inventory)
            print(f"⚙️ Created empty QuestSideInventory for Player {player_name}") 

        return cls(
            player_id                   = player_id, #d.get("player_id"),
            player_name                 = player_name, #d.get("player_name"),
            player_gender               = d.get("player_gender"),
            player_money                = d.get("player_money"),
            player_location             = get_location_by_id(d.get("player_location_id")),
            player_item_inventory       = item_inventory, #get_player_item_inventory_by_id(d.get("player_item_inventory_id")),
            player_daimon_dex           = daimon_dex, #get_player_daimon_dex_by_id(d.get("player_daimon_dex_id")),
            player_daimon_inventory     = daimon_inventory, #get_player_daimon_inventory_by_id(d.get("player_daimon_inventory_id")),
            player_quest_main_inventory = quest_main_inventory,
            player_quest_side_inventory = quest_side_inventory    
        )
    
    # --------------------------------------------------
    # Convert Player object to dictionary.
    # --------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "player_id"                      : self.player_id,
            "player_name"                    : self.player_name,
            "player_gender"                  : self.player_gender,
            "player_money"                   : self.player_money,
            "player_location_id"             : self.player_location.location_id,
            "player_daimon_dex_id"           : self.player_daimon_dex.player_daimon_dex_id,
            "player_daimon_inventory_id"     : self.player_daimon_inventory.player_daimon_inventory_id,
            "player_item_inventory_id"       : self.player_item_inventory.player_item_inventory_id,
            "player_quest_main_inventory_id" : self.player_quest_main_inventory.player_quest_main_inventory_id,
            "player_quest_side_inventory_id" : self.player_quest_main_inventory.player_quest_main_inventory_id
        }
    
    # Class-level set to track used names
    _used_names = set()

    def __post_init__(self):
        if self.player_name in Player._used_names:
            raise ValueError(f"Duplicate player name '{self.player_name}' detected.")
        Player._used_names.add(self.player_name)

    def add_item_to_player_item_inventory(self, item: Item) -> bool:
        """
        Adds an item (generic or unique) to the player's inventory.
        Automatically routed by PlayerItemInventory.
        """
        return self.player_item_inventory.add_item_to_player_item_inventory(item)

    def subtract_item_from_player_item_inventory(self, item: Item, quantity) -> bool:
        """
        Removes or subtracts an item (generic or unique) from the player's inventory.
        Automatically routed by PlayerItemInventory.
        """
        return self.player_item_inventory.subtract_item_from_player_item_inventory(item, quantity)

    def update_player_money(self, money_amount: int) -> bool:
        """Add or subtract a Player's money."""
        if isinstance(money_amount, int) or money_amount != 0:
            if money_amount > 0:
                print(f"{self.player_name} added ${money_amount}. Total: {self.player_money}")
                self.player_money = self.player_money + money_amount
            elif money_amount < 0 and self.player_money + money_amount < 0:
                print(f"{self.player_name} does not have ${money_amount} to subtract. Total: {self.player_money}")
            elif money_amount < 0:
                print(f"{self.player_name} subtracted ${money_amount}. Total: {self.player_money}")
                self.player_money = self.player_money + money_amount
        else:
            print(f"❌ Invalid Player money update amount: {amount}.")

    def catch_daimon_unbonded(self, daimon_unbonded: "DaimonUnbonded") -> Optional["Player"]:
        """
        Player catches a DaimonUnbonded. 
        Converts it to a DaimonBonded and adds it to the player's inventory.
        Returns self on success.
        """

        daimon_bonded = DaimonBonded(
            daimon_bonded_id                    = len(self.player_daimon_inventory.player_daimon_inventory_team)+len(self.player_daimon_inventory.player_daimon_inventory_storage)+1,
            daimon_bonded_daimon_template_id    = daimon_unbonded.daimon_unbonded_daimon_template_id,
            daimon_bonded_species               = daimon_unbonded.daimon_unbonded_species,
            daimon_bonded_level                 = daimon_unbonded.daimon_unbonded_level,
            daimon_bonded_level_progress        = daimon_unbonded.daimon_unbonded_level_progress,
            daimon_bonded_gender                = daimon_unbonded.daimon_unbonded_gender,
            daimon_bonded_height                = daimon_unbonded.daimon_unbonded_height,
            daimon_bonded_weight                = daimon_unbonded.daimon_unbonded_weight,
            daimon_bonded_max_health            = daimon_unbonded.daimon_unbonded_max_health,
            daimon_bonded_current_health        = daimon_unbonded.daimon_unbonded_current_health,
            daimon_bonded_status                = daimon_unbonded.daimon_unbonded_status,
            daimon_bonded_stat_health           = daimon_unbonded.daimon_unbonded_stat_health,
            daimon_bonded_stat_physical_attack  = daimon_unbonded.daimon_unbonded_stat_physical_attack,
            daimon_bonded_stat_special_attack   = daimon_unbonded.daimon_unbonded_stat_special_attack,
            daimon_bonded_stat_physical_defense = daimon_unbonded.daimon_unbonded_stat_physical_defense,
            daimon_bonded_stat_special_defense  = daimon_unbonded.daimon_unbonded_stat_special_defense,
            daimon_bonded_stat_speed            = daimon_unbonded.daimon_unbonded_stat_speed,
            daimon_bonded_type_1                = daimon_unbonded.daimon_unbonded_type_1,
            daimon_bonded_type_2                = daimon_unbonded.daimon_unbonded_type_2,
            daimon_bonded_ability               = daimon_unbonded.daimon_unbonded_ability,
            daimon_bonded_move_1                = daimon_unbonded.daimon_unbonded_move_1,
            daimon_bonded_move_2                = daimon_unbonded.daimon_unbonded_move_2,
            daimon_bonded_move_3                = daimon_unbonded.daimon_unbonded_move_3,
            daimon_bonded_move_4                = daimon_unbonded.daimon_unbonded_move_4,
            daimon_bonded_item                  = daimon_unbonded.daimon_unbonded_item,
            daimon_bonded_nickname              = daimon_unbonded.daimon_unbonded_species
        )

        # Add to PlayerDaimonInventory
        self.player_daimon_inventory.add_daimon_to_player_daimon_inventory(daimon_bonded)

        # If this is the first Daimon caught, make it the follower
        if daimon_bonded.daimon_bonded_id == 1:
            self.player_daimon_inventory.set_follower(daimon_bonded)

        # Remove DaimonUnbonded from daimon_unbonded_global
        if daimon_unbonded in daimon_unbonded_global:
            daimon_unbonded_global.remove(daimon_unbonded)

        print(f"🎉 {self.player_name} caught {daimon_bonded.daimon_bonded_species}!")
        return self
    
    def add_quest_side_to_player_quest_side_inventory(self, quest_side: "QuestSide") -> bool:
        """
        Adds a QuestSide to the player's side quest inventory if not already present.
        Removes the quest from the global quest_side_global list upon success.
        Returns True if successfully added, False otherwise.
        """

        # Add the quest to the player's side quest inventory
        quest_side.quest_side_id = len(self.player_quest_side_inventory.player_quest_side_inventory_storage) + 1
        self.player_quest_side_inventory.player_quest_side_inventory_storage.append(quest_side)
        print(f"🗺️ Added side quest '{quest_side.quest_side_name}' to {self.player_name}'s quest inventory.")

        # Remove it from the global quest pool if it exists there
        if quest_side in quest_side_global:
            quest_side_global.remove(quest_side)
            print(f"📦 Removed '{quest_side.quest_side_name}' from global quest pool.")

        return True
    
    def take_battle_turn(self, battle: "SystemDaimonBattle"):
        """
        Player turn handler.
        Prompts user for an action, then executes it.
        If no moves remain, the Daimon will automatically use Struggle.
        """
        active_team = battle.get_active_daimons_for_participant(self)
        opponents = battle.get_opponents_for_participant(self)

        if not active_team:
            print(f"⚠️ {self.player_name} has no active Daimons to take a turn!")
            return

        print(f"🎮 {self.player_name}'s turn: {len(active_team)} Daimons on field\n")

        for daimon in active_team:

            # Skip fainted Daimons
            if daimon.daimon_bonded_current_health <= 0:
                print(f"💀 {daimon.daimon_bonded_nickname} is fainted and cannot act.")
                continue

            print(f"➡️ {daimon.daimon_bonded_nickname}'s move!\n")

            print("""
                            ┌────────────────┐   ┌────────────────┐   ┌────────────────┐    ┌────────────────┐
                            │    1 Fight     │   │    2 Item      │   │   3 Switch     │    │     4 Run      │
                            └────────────────┘   └────────────────┘   └────────────────┘    └────────────────┘
            """)

            player_choice = input("Select an option: ").upper().strip()

            # ======================================================================
            # 🥊 FIGHT
            # ======================================================================
            if player_choice == "1" or player_choice == "FIGHT":
                print(f"⚔️ You chose to fight with {daimon.daimon_bonded_nickname}!\n")

                # ---- Get moves ----
                move_slots = [
                    getattr(daimon, "daimon_bonded_move_1", None),
                    getattr(daimon, "daimon_bonded_move_2", None),
                    getattr(daimon, "daimon_bonded_move_3", None),
                    getattr(daimon, "daimon_bonded_move_4", None),
                ]

                # ---- Build move display strings ----
                slot_strings = []
                for idx, move in enumerate(move_slots, start=1):
                    if move is None:
                        name = "—"
                        pp = ""
                    else:
                        name = move.daimon_move_name
                        pp = f"{move.daimon_move_points_current}/{move.daimon_move_points_max}"
                    slot_strings.append(f"{idx} {name} ({pp})".ljust(20))

                # ---- Print move UI ----
                print(f"""
                        ┌────────────────────┐   ┌────────────────────┐   ┌────────────────────┐   ┌────────────────────┐
                        │ {slot_strings[0]}  │   │ {slot_strings[1]}  │   │ {slot_strings[2]}  │   │ {slot_strings[3]}  │
                        └────────────────────┘   └────────────────────┘   └────────────────────┘   └────────────────────┘
                """)

                # Filter out None move slots and those with no current points left
                moves_with_current_points = [m for m in move_slots if m and m.daimon_move_points_current > 0]

                # Choose a move
                if not moves_with_current_points:
                    # Struggle if there are no move options
                    move = get_daimon_move_by_id(8)  # Struggle
                    print(f"💢 {daimon.daimon_bonded_nickname} has no moves left! It used {move.daimon_move_name}!\n")
                else:
                    move = None
                    while move is None:
                        choice = input("Choose a move (1–4): ").strip()
                        try:
                            idx = int(choice) - 1
                            if idx < 0 or idx >= len(move_slots):
                                raise ValueError
                            player_move_choice = move_slots[idx]
                            if player_move_choice is None:
                                raise ValueError
                            if player_move_choice.daimon_move_points_current <= 0:
                                print(f"❌ {player_move_choice.daimon_move_name} has no PP left! Choose another move.")
                                continue
                            # Valid player_move_choice
                            move = player_move_choice
                            move.daimon_move_points_current -= 1  # reduce PP
                        except ValueError:
                            print("❌ Invalid selection. Please choose a move number between 1 and 4 that has PP left.")

                # ==================================================================
                # 🎯 Target selection (Player chooses)
                # ==================================================================
                if opponents:
                    print("\nChoose a target:")
                    for i, o in enumerate(opponents, 1):
                        name = getattr(o, "daimon_bonded_nickname",
                                getattr(o, "daimon_unbonded_species", "Unknown"))
                        print(f"  {i}. {name}")

                    target_choice = input("Target: ").strip()
                    try:
                        target = opponents[int(target_choice) - 1]
                    except:
                        target = opponents[0]
                        print("⚠️ Invalid target. Defaulting to the first opponent.")
                else:
                    print("⚠️ No opponents available to target.")
                    return

                # ---- Execute the attack ----
                battle.execute_move(daimon, target, move)

            # ======================================================================
            # 🎁 ITEM (not implemented)
            # ======================================================================
            elif player_choice == "2" or player_choice == "ITEM":
                print("🎁 You chose to use an item (not yet implemented).")

            # ======================================================================
            # 🔁 SWITCH (not implemented)
            # ======================================================================
            elif player_choice == "3" or player_choice == "SWITCH":
                print("🔁 You chose to switch Daimons (not yet implemented).")

            # ======================================================================
            # 🏃 RUN (not implemented)
            # ======================================================================
            elif player_choice == "4" or player_choice == "RUN":
                print("🏃 You attempt to run. (not yet implemented).")

            else:
                print("❌ Invalid choice, skipping turn.")

    def _choose_move_action(self, battle: "SystemDaimonBattle", daimon: "DaimonBonded"):
        """Handle the player's choice to use a move."""
        moves = [
            getattr(daimon, f"daimon_bonded_move_{i}", None)
            for i in range(1, 5)
            if getattr(daimon, f"daimon_bonded_move_{i}", None)
        ]
        if not moves:
            print(f"⚠️ {daimon.daimon_bonded_nickname} has no moves!")
            return

        print("\nAvailable moves:")
        for i, move in enumerate(moves, 1):
            print(f"  {i}. {move.daimon_move_name}")

        choice = input("Choose a move: ").strip()
        try:
            index = int(choice) - 1
            if index < 0 or index >= len(moves):
                raise ValueError
            selected_move = moves[index]
        except ValueError:
            print("❌ Invalid move choice.")
            return

        opponents = battle.get_opponents_for_participant(self)
        if not opponents:
            print("⚠️ No opponents available.")
            return

        print("\nAvailable targets:")
        for i, opponent in enumerate(opponents, 1):
            print(f"  {i}. {opponent.daimon_bonded_nickname if hasattr(opponent, 'daimon_bonded_nickname') else opponent.daimon_unbonded_name}")

        target_choice = input("Choose a target: ").strip()
        try:
            target_index = int(target_choice) - 1
            if target_index < 0 or target_index >= len(opponents):
                raise ValueError
            target = opponents[target_index]
        except ValueError:
            print("❌ Invalid target choice.")
            return

        print(f"⚔️ {daimon.daimon_bonded_nickname} uses {selected_move.daimon_move_name} on {getattr(target, 'daimon_bonded_nickname', getattr(target, 'daimon_unbonded_name'))}!")
        battle.execute_move(daimon, target, selected_move)

    def _choose_item_action(self, battle: "SystemDaimonBattle", daimon: "DaimonBonded"):
        """Handle using an item during battle."""
        inventory = self.player_item_inventory_storage_unique + self.player_item_inventory_storage_generic
        if not inventory:
            print("🎒 You have no items!")
            return

        print("\nYour items:")
        for i, item in enumerate(inventory, 1):
            print(f"  {i}. {item.item_name} (x{item.item_quantity})")

        choice = input("Choose an item: ").strip()
        try:
            index = int(choice) - 1
            if index < 0 or index >= len(inventory):
                raise ValueError
            selected_item = inventory[index]
        except ValueError:
            print("❌ Invalid item choice.")
            return

        # Use item on a daimon (ally or self)
        allies = battle.get_active_daimons_for_participant(self)
        print("\nChoose a target:")
        for i, ally in enumerate(allies, 1):
            print(f"  {i}. {ally.daimon_bonded_nickname}")

        target_choice = input("Target: ").strip()
        try:
            target_index = int(target_choice) - 1
            if target_index < 0 or target_index >= len(allies):
                raise ValueError
            target = allies[target_index]
        except ValueError:
            print("❌ Invalid target choice.")
            return

        print(f"🎒 {self.player_name} uses {selected_item.item_name} on {target.daimon_bonded_nickname}!")
        battle.execute_item(self, selected_item, target)

    def _choose_switch_action(self, battle: "SystemDaimonBattle", current_daimon: "DaimonBonded"):
        """Handle switching Daimons."""
        team = self.player_daimon_inventory.player_daimon_inventory_team
        bench = [d for d in team if d not in battle.get_active_daimons_for_participant(self)]

        if not bench:
            print("⚠️ No Daimons available to switch in!")
            return

        print("\nAvailable Daimons to switch to:")
        for i, daimon in enumerate(bench, 1):
            print(f"  {i}. {daimon.daimon_bonded_nickname}")

        choice = input("Choose a Daimon to switch in: ").strip()
        try:
            index = int(choice) - 1
            if index < 0 or index >= len(bench):
                raise ValueError
            new_daimon = bench[index]
        except ValueError:
            print("❌ Invalid Daimon choice.")
            return

        print(f"🔄 Switching {current_daimon.daimon_bonded_nickname} → {new_daimon.daimon_bonded_nickname}!")
        battle.switch_daimon(self, current_daimon, new_daimon)

@dataclass(kw_only=True)
class SystemDaimonBattle:
    """Represents a SystemDaimonBattle and its attributes."""

    system_daimon_battle_id: int
    system_daimon_battle_side_a: List[Union["DaimonUnbonded", "NPC", "Player"]]
    system_daimon_battle_side_b: List[Union["DaimonUnbonded", "NPC", "Player"]]
    system_daimon_battle_side_a_daimon: List[Union["DaimonBonded", "DaimonUnbonded"]] = field(default_factory=list)
    system_daimon_battle_side_b_daimon: List[Union["DaimonBonded", "DaimonUnbonded"]] = field(default_factory=list)
    system_daimon_turn_order: List[Union["DaimonBonded", "DaimonUnbonded"]] = field(default_factory=list)
    system_daimon_current_turn: int = 0
    battle_log: List[str] = field(default_factory=list)

    # --------------------------------------------------
    # Initialization & Stat Stage Injection
    # --------------------------------------------------
    def initialize_battle(self):
        for participant, side_daimons in [
            (self.system_daimon_battle_side_a, self.system_daimon_battle_side_a_daimon),
            (self.system_daimon_battle_side_b, self.system_daimon_battle_side_b_daimon)
        ]:
            for p in participant:
                side_daimons.extend(self._extract_daimons(p))

        # Inject stat stages (battle-only)
        for d in self.system_daimon_battle_side_a_daimon + self.system_daimon_battle_side_b_daimon:
            d.battle_stat_stages = {
                "physical_attack": 0,
                "physical_defense": 0,
                "special_attack": 0,
                "special_defense": 0,
                "speed": 0
            }

        self.update_turn_order()

    # -------------------------
    # Helper Methods
    # -------------------------
    def _get_attr(self, daimon, attr):
        return getattr(daimon, attr)

    def _set_attr(self, daimon, attr, value):
        setattr(daimon, attr, value)

    def _get_daimon_name(self, daimon) -> str:
        if isinstance(daimon, DaimonBonded):
            return getattr(daimon, "daimon_bonded_nickname")
        elif isinstance(daimon, DaimonUnbonded):
            return getattr(daimon, "daimon_unbonded_species")
        return "Unknown"

    def is_daimon_alive(self, daimon) -> bool:
        if isinstance(daimon, DaimonBonded):
            current_health = getattr(daimon, "daimon_bonded_current_health")
        elif isinstance(daimon, DaimonUnbonded):
            current_health = getattr(daimon, "daimon_unbonded_current_health")
        else:
            return False
        return current_health > 0

    def _extract_daimons(self, participant):
        if isinstance(participant, Player):
            return participant.player_daimon_inventory.player_daimon_inventory_team[:6]
        elif isinstance(participant, NPC):
            return participant.npc_daimon_inventory.npc_daimon_inventory_team[:6]
        elif isinstance(participant, DaimonUnbonded):
            return [participant]
        return []
    

    def get_active_daimons_for_participant(self, participant) -> List[Union["DaimonBonded", "DaimonUnbonded"]]:
        """
        Returns the currently active Daimons for the given participant.
        - Players and NPCs return their current active battle Daimons.
        - Unbonded Daimons return themselves as a list.
        """
        if participant in self.system_daimon_battle_side_a:
            return self.system_daimon_battle_side_a_daimon
        elif participant in self.system_daimon_battle_side_b:
            return self.system_daimon_battle_side_b_daimon
        elif isinstance(participant, DaimonUnbonded):
            return [participant]
        return []

    def get_participant_for_daimon(self, daimon):
        for participant in self.system_daimon_battle_side_a + self.system_daimon_battle_side_b:
            if daimon in self._extract_daimons(participant):
                return participant
        return None

    def get_opponents_for_participant(self, participant):
        if participant in self.system_daimon_battle_side_a:
            return [d for d in self.system_daimon_battle_side_b_daimon if self.is_daimon_alive(d)]
        elif participant in self.system_daimon_battle_side_b:
            return [d for d in self.system_daimon_battle_side_a_daimon if self.is_daimon_alive(d)]
        return []

    # --------------------------------------------------
    # Turn Order
    # --------------------------------------------------
    def update_turn_order(self):
        all_daimons = self.system_daimon_battle_side_a_daimon + self.system_daimon_battle_side_b_daimon

        def speed_value(d):
            if isinstance(d, DaimonBonded):
                daimon_base_speed = getattr(d, "daimon_bonded_stat_speed")
            elif isinstance(d, DaimonUnbonded):
                daimon_base_speed = getattr(d, "daimon_unbonded_stat_speed")
            stage = d.battle_stat_stages.get("speed", 0)
            return daimon_base_speed * self._calculate_stage_multiplier(stage)

        self.system_daimon_turn_order = sorted(all_daimons, key=speed_value, reverse=True)

    # --------------------------------------------------
    # Stage Multipliers
    # --------------------------------------------------
    def _calculate_stage_multiplier(self, stage: int) -> float:
        stage = max(-6, min(6, stage))
        if stage > 0:
            return 1.0 + (stage * 0.5)  # +1 stage = 1.5x
        elif stage < 0:
            return (6 + stage) / 6      # -1 stage = 5/6x
        else:
            return 1.0

    # --------------------------------------------------
    # Move Execution
    # --------------------------------------------------
    def execute_move(self, attacker, target, move):
        """Execute a move between DaimonBonded/DaimonUnbonded and DaimonBonded/DaimonUnbonded."""

        attacker_name = self._get_daimon_name(attacker)
        target_name = self._get_daimon_name(target)

        # Accuracy check
        move_accuracy = getattr(move, "daimon_move_accuracy")
        move_name = getattr(move, "daimon_move_name")
        if random.random() > move_accuracy:
            print(f"❌ {attacker_name}'s {move_name} missed {target_name}!")
            return

        # -------------------------
        # Damage
        # -------------------------
        damage = 0
        if getattr(move, "daimon_move_power") > 0:
            damage = self._calculate_damage(attacker, target, move)
            self._apply_damage(target, damage)

        print(f"💥 {attacker_name} used {move_name} on {target_name}! Damage: {damage}")

        # -------------------------
        # Status Effects
        # -------------------------
        if getattr(move, "daimon_move_effect_status", None):
            self._apply_status_effects(attacker, target, move)

        # -------------------------
        # Stat Changes
        # -------------------------
        if getattr(move, "daimon_move_effect_stat_change", None):
            self._apply_stat_changes(attacker, target, move)

    # --------------------------------------------------
    # Apply Damage
    # --------------------------------------------------
    def _apply_damage(self, target, damage):
        hp_attr = "daimon_bonded_current_health" if isinstance(target, DaimonBonded) else "daimon_unbonded_current_health"
        current_hp = getattr(target, hp_attr)
        new_hp = max(0, current_hp - damage)
        setattr(target, hp_attr, new_hp)

        if new_hp == 0:
            print(f"💀 {self._get_daimon_name(target)} fainted!")

    # --------------------------------------------------
    # Status Effects
    # --------------------------------------------------
    def _apply_status_effects(self, attacker, target, move):
        for daimon_status in move.daimon_move_effect_status:
            ######print(f'\nDAIMON STATUS {daimon_status}')
            weight = daimon_status.get("daimon_move_status_weight", 1.0)
            if random.random() > weight:
                continue
            status_obj = daimon_status.get("daimon_move_status")
            ######print(f'\nSTATUS OBJ {status_obj}')
            status_target = daimon_status.get("daimon_effect_status_target", "Target")
            if status_target == "User":
                daimon = attacker
            elif status_target == "Target":
                daimon = target

            if isinstance(daimon, DaimonBonded):
                daimon.daimon_bonded_status = daimon_status
            elif isinstance(daimon, DaimonUnbonded):
                daimon.daimon_unbonded_status = daimon_status

            print(f"✨ {self._get_daimon_name(daimon)} is now {status_obj.daimon_status_name}!")

    # --------------------------------------------------
    # Stat Changes
    # --------------------------------------------------
    def _apply_stat_changes(self, attacker, target, move):
        for effect in move.daimon_move_effect_stat_change:
            stat = effect.get("daimon_effect_stat_change_type")
            value = effect.get("daimon_effect_stat_change_value")
            weight = effect.get("daimon_effect_stat_change_weight")
            stat_target = effect.get("daimon_effect_stat_change_target")

            if random.random() > weight:
                continue
            
            if stat_target == "User":
                daimon = attacker
            elif stat_target == "Target":
                daimon = target

            mapping = {
                "Physical Attack": "physical_attack",
                "Special Attack": "special_attack",
                "Physical Defense": "physical_defense",
                "Special Defense": "special_defense",
                "Speed": "speed",
            }

            key = mapping.get(stat)
            if key:
                current = daimon.battle_stat_stages[key]
                new_stage = max(-6, min(6, current + value))
                daimon.battle_stat_stages[key] = new_stage
                print(f"⚡ {self._get_daimon_name(daimon)}'s {stat} changed from {current} to {new_stage}!")

    # --------------------------------------------------
    # Damage Calculation
    # --------------------------------------------------
    def _calculate_damage(self, attacker, target, move):
        category = move.daimon_move_category

        # Attack stat
        if isinstance(attacker, DaimonBonded):
            atk_attr = "daimon_bonded_stat_physical_attack" if category == "Physical" else "daimon_bonded_stat_special_attack"
        else:
            atk_attr = "daimon_unbonded_stat_physical_attack" if category == "Physical" else "daimon_unbonded_stat_special_attack"

        atk_base = self._get_attr(attacker, atk_attr)
        atk_stage_key = "physical_attack" if category == "Physical" else "special_attack"
        atk_stage = attacker.battle_stat_stages.get(atk_stage_key, 0)
        atk_value = atk_base * self._calculate_stage_multiplier(atk_stage)

        # Defense stat
        if isinstance(target, DaimonBonded):
            def_attr = "daimon_bonded_stat_physical_defense" if category == "Physical" else "daimon_bonded_stat_special_defense"
        else:
            def_attr = "daimon_unbonded_stat_physical_defense" if category == "Physical" else "daimon_unbonded_stat_special_defense"

        def_base = self._get_attr(target, def_attr)
        def_stage_key = "physical_defense" if category == "Physical" else "special_defense"
        def_stage = target.battle_stat_stages.get(def_stage_key, 0)
        def_value = def_base * self._calculate_stage_multiplier(def_stage)

        damage = max(1, int((atk_value / max(1, def_value)) * move.daimon_move_power))
        return damage

    # --------------------------------------------------
    # Turn Handling
    # --------------------------------------------------
    def next_turn(self):
        if not self.system_daimon_turn_order:
            print("⚠️ No turn order set! Initialize battle first.")
            return

        current_daimon = self.system_daimon_turn_order[self.system_daimon_current_turn]
        participant = self.get_participant_for_daimon(current_daimon)

        if not participant:
            print(f"⚠️ Could not identify participant for {self._get_daimon_name(current_daimon)}.")
            self.system_daimon_current_turn = (self.system_daimon_current_turn + 1) % len(self.system_daimon_turn_order)
            return

        # Delegate turn: bonded/unbonded Daimons handle themselves
        if isinstance(participant, Player) or isinstance(participant, NPC):
            participant.take_battle_turn(self)
        elif isinstance(current_daimon, DaimonUnbonded):
            # The wild Daimon executes its AI-defined turn
            current_daimon.take_battle_turn(self)
        else:
            print(f"⚠️ Unrecognized participant type: {type(participant)}")

        # Handle fainted Daimons and check victory
        self._remove_fainted_daimons()
        self._check_victory_conditions()

        # Move to next turn in order
        self.system_daimon_current_turn = (self.system_daimon_current_turn + 1) % len(self.system_daimon_turn_order)

    # --------------------------------------------------
    # Fainting & Replacements
    # --------------------------------------------------
    def _remove_fainted_daimons(self):
        for participants, daimon_list in [
            (self.system_daimon_battle_side_a, self.system_daimon_battle_side_a_daimon),
            (self.system_daimon_battle_side_b, self.system_daimon_battle_side_b_daimon)
        ]:
            for d in daimon_list[:]:
                if not self.is_daimon_alive(d):
                    print(f"💀 {self._get_daimon_name(d)} fainted!")
                    daimon_list.remove(d)
                    # Send in a replacement from bench if available
                    bench = [
                        x for x in sum([self._extract_daimons(p) for p in participants], [])
                        if self.is_daimon_alive(x) and x not in daimon_list
                    ]
                    if bench:
                        daimon_list.append(bench[0])
                        print(f"🔁 {self._get_daimon_name(bench[0])} sent to the field!")

    # --------------------------------------------------
    # Victory Conditions
    # --------------------------------------------------
    def _check_victory_conditions(self):
        if not self.system_daimon_battle_side_a_daimon:
            print("🏁 Side B wins!")
            return True
        elif not self.system_daimon_battle_side_b_daimon:
            print("🏁 Side A wins!")
            return True
        return False

    # --------------------------------------------------
    # Switching Daimons
    # --------------------------------------------------
    def switch_daimon(self, participant, current_daimon, new_daimon):
        if participant in self.system_daimon_battle_side_a:
            active_list = self.system_daimon_battle_side_a_daimon
        elif participant in self.system_daimon_battle_side_b:
            active_list = self.system_daimon_battle_side_b_daimon
        else:
            return

        if current_daimon in active_list:
            active_list.remove(current_daimon)
            active_list.append(new_daimon)
            print(f"🔁 {getattr(participant, 'player_name', getattr(participant, 'npc_name', str(participant)))} switched "
                  f"{self._get_daimon_name(current_daimon)} for {self._get_daimon_name(new_daimon)}!")

    # --------------------------------------------------
    # Item Usage
    # --------------------------------------------------
    def execute_item(self, user, item, target):
        user_name = getattr(user, 'player_name', getattr(user, 'npc_name', 'Unknown'))
        print(f"🎁 {user_name} used {item.item_name} on {self._get_daimon_name(target)}!")
        if item.item_id == 18:  # Example: Heal 50 HP
            healed = min(
                self._get_attr(target, 'daimon_bonded_max_health' if isinstance(target, DaimonBonded) else 'daimon_unbonded_max_health') -
                self._get_attr(target, 'daimon_bonded_current_health' if isinstance(target, DaimonBonded) else 'daimon_unbonded_current_health'),
                50
            )
            self._set_attr(target,
                           'daimon_bonded_current_health' if isinstance(target, DaimonBonded) else 'daimon_unbonded_current_health',
                           self._get_attr(target, 'daimon_bonded_current_health' if isinstance(target, DaimonBonded) else 'daimon_unbonded_current_health') + healed)
            print(f"💖 {self._get_daimon_name(target)} healed for {healed} HP!")

    # --------------------------------------------------
    # Run Full Battle
    # --------------------------------------------------
    def run_full_battle(self):
        round_count = 1
        while True:
            print(f"\n============================\n🕓 ROUND {round_count}\n============================")
            for _ in range(len(self.system_daimon_turn_order)):
                self.next_turn()
                time.sleep(0.5)

            if self._check_victory_conditions():
                print(f"\n⏹️ Battle finished after {round_count} rounds.")
                break

            round_count += 1
    
# ----------------------------------------------------------------------------------------------------
# UPDATED Item Template - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_item_template():
    global item_template_global
    if ITEM_TEMPLATE_DATA_FILE.exists():
        with open(ITEM_TEMPLATE_DATA_FILE, "r", encoding="utf-8") as f:
            item_template_data = json.load(f)
            item_template_global = [ItemTemplate.from_dict(d) for d in item_template_data]
            print(f"Loaded {len(item_template_global)} Item Template")
    else:
        raise FileNotFoundError(f"{ITEM_TEMPLATE_DATA_FILE} not found")

def get_item_template_by_id(item_template_id: int) -> Optional[ItemTemplate]:
    for item_template in item_template_global:
        if item_template.item_template_id == item_template_id:
            return item_template
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Item - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_item():
    global item_global
    if ITEM_DATA_FILE.exists():
        with open(ITEM_DATA_FILE, "r", encoding="utf-8") as f:
            item_data = json.load(f)
            item_global = [Item.from_dict(d) for d in item_data]
            print(f"Loaded {len(item_global)} Item")
    else:
        raise FileNotFoundError(f"{ITEM_DATA_FILE} not found")
    
def save_all_item():
    with open(ITEM_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([item.to_dict() for item in item_global], f, indent=4)
        print(f"Saved {len(item_global)} Item")

def get_item_by_id(item_id: int) -> Optional[Item]:
    for item in item_global:
        if item.item_id == item_id:
            return item
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Weather Template - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_weather_template():
    global weather_template_global
    if WEATHER_TEMPLATE_DATA_FILE.exists():
        with open(WEATHER_TEMPLATE_DATA_FILE, "r", encoding="utf-8") as f:
            weather_template_data = json.load(f)
            weather_template_global = [WeatherTemplate.from_dict(d) for d in weather_template_data]
            print(f"Loaded {len(weather_template_global)} Weather Template")
    else:
        raise FileNotFoundError(f"{WEATHER_TEMPLATE_DATA_FILE} not found")

def get_weather_template_by_id(weather_template_id: int) -> Optional[WeatherTemplate]:
    for weather_template in weather_template_global:
        if weather_template.weather_template_id == weather_template_id:
            return weather_template
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Weather - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_weather():
    global weather_global
    if WEATHER_DATA_FILE.exists():
        with open(WEATHER_DATA_FILE, "r", encoding="utf-8") as f:
            weather_data = json.load(f)
            weather_global = [Weather.from_dict(d) for d in weather_data]
            print(f"Loaded {len(weather_global)} Weather")
    else:
        raise FileNotFoundError(f"{WEATHER_DATA_FILE} not found")

def get_weather_by_id(weather_id: int) -> Optional[Weather]:
    for weather in weather_global:
        if weather.weather_id == weather_id:
            return weather
    return None

# ----------------------------------------------------------------------------------------------------
# Biome - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_biome():
    global biome_global
    if BIOME_DATA_FILE.exists():
        with open(BIOME_DATA_FILE, "r", encoding="utf-8") as f:
            biome_data = json.load(f)
            biome_global = [Biome.from_dict(d) for d in biome_data]
            print(f"Loaded {len(biome_global)} Biome")
    else:
        raise FileNotFoundError(f"{BIOME_DATA_FILE} not found")

def get_biome_by_id(biome_id: int) -> Optional[Biome]:
    for biome in biome_global:
        if biome.biome_id == biome_id:
            return biome
    return None
    
# ----------------------------------------------------------------------------------------------------
# UPDATED Location - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_location():
    global location_global
    if LOCATION_DATA_FILE.exists():
        with open(LOCATION_DATA_FILE, "r", encoding="utf-8") as f:
            location_data = json.load(f)
            location_global = [Location.from_dict(d) for d in location_data]
            print(f"Loaded {len(location_global)} Location")
    else:
        raise FileNotFoundError(f"{LOCATION_DATA_FILE} not found")
    
def save_all_location():
    with open(LOCATION_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([location.to_dict() for location in location_global], f, indent=4)
        print(f"Saved {len(location_global)} Location")

def get_location_by_id(location_id: int) -> Optional[Location]:
    for location in location_global:
        if location.location_id == location_id:
            return location
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Interactible - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_interactible():
    global interactible_global
    if INTERACTIBLE_DATA_FILE.exists():
        with open(INTERACTIBLE_DATA_FILE, "r", encoding="utf-8") as f:
            interactible_data = json.load(f)
            interactible_global = [Interactible.from_dict(d) for d in interactible_data]
            print(f"Loaded {len(interactible_global)} Interactible")
    else:
        raise FileNotFoundError(f"{INTERACTIBLE_DATA_FILE} not found")
    
def save_all_interactible():
    with open(INTERACTIBLE_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([interactible.to_dict() for interactible in interactible_global], f, indent=4)
        print(f"Saved {len(interactible_global)} Interactible")

def get_interactible_by_id(interactible_id: int) -> Optional[Interactible]:
    for interactible in interactible_global:
        if interactible.interactible_id == interactible_id:
            return interactible
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Daimon Status Template - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_daimon_status_template():
    global daimon_status_template_global
    if DAIMON_STATUS_TEMPLATE_DATA_FILE.exists():
        with open(DAIMON_STATUS_TEMPLATE_DATA_FILE, "r", encoding="utf-8") as f:
            daimon_status_template_data = json.load(f)
            daimon_status_template_global = [DaimonStatusTemplate.from_dict(d) for d in daimon_status_template_data]
            print(f"Loaded {len(daimon_status_template_global)} Daimon Status Template")
    else:
        raise FileNotFoundError(f"{DAIMON_STATUS_TEMPLATE_DATA_FILE} not found")

def get_daimon_status_template_by_id(daimon_status_template_id: int) -> Optional[DaimonStatusTemplate]:
    for daimon_status_template in daimon_status_template_global:
        if daimon_status_template.daimon_status_template_id == daimon_status_template_id:
            return daimon_status_template
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Daimon Status - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_daimon_status():
    global daimon_status_global
    if DAIMON_STATUS_DATA_FILE.exists():
        with open(DAIMON_STATUS_DATA_FILE, "r", encoding="utf-8") as f:
            daimon_status_data = json.load(f)
            daimon_status_global = [DaimonStatus.from_dict(d) for d in daimon_status_data]
            print(f"Loaded {len(daimon_status_global)} Daimon Status")
    else:
        raise FileNotFoundError(f"{DAIMON_STATUS_DATA_FILE} not found")

def save_all_daimon_status():
    with open(DAIMON_STATUS_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([daimon_status.to_dict() for daimon_status in daimon_status_global], f, indent=4)
        print(f"Saved {len(daimon_status_global)} Daimon Status")

def get_daimon_status_by_id(daimon_status_id: int) -> Optional[DaimonStatus]:
    for daimon_status in daimon_status_global:
        if daimon_status.daimon_status_id == daimon_status_id:
            return daimon_status
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Daimon Type - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_daimon_type():
    global daimon_type_global
    if DAIMON_TYPE_DATA_FILE.exists():
        with open(DAIMON_TYPE_DATA_FILE, "r", encoding="utf-8") as f:
            daimon_type_data = json.load(f)
            daimon_type_global = [DaimonType.from_dict(d) for d in daimon_type_data]
            print(f"Loaded {len(daimon_type_global)} Daimon Type")
    else:
        raise FileNotFoundError(f"{DAIMON_TYPE_DATA_FILE} not found")

def get_daimon_type_by_id(daimon_type_id: int) -> Optional[DaimonType]:
    for daimon_type in daimon_type_global:
        if daimon_type.daimon_type_id == daimon_type_id:
            return daimon_type
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Daimon Ability - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_daimon_ability():
    global daimon_ability_global
    if DAIMON_ABILITY_DATA_FILE.exists():
        with open(DAIMON_ABILITY_DATA_FILE, "r", encoding="utf-8") as f:
            daimon_ability_data = json.load(f)
            daimon_ability_global = [DaimonAbility.from_dict(d) for d in daimon_ability_data]
            print(f"Loaded {len(daimon_ability_global)} Daimon Ability")
    else:
        raise FileNotFoundError(f"{DAIMON_ABILITY_DATA_FILE} not found")

def get_daimon_ability_by_id(daimon_ability_id: int) -> Optional[DaimonAbility]:
    for daimon_ability in daimon_ability_global:
        if daimon_ability.daimon_ability_id == daimon_ability_id:
            return daimon_ability
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Daimon Move Template - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_daimon_move_template():
    global daimon_move_template_global
    if DAIMON_MOVE_TEMPLATE_DATA_FILE.exists():
        with open(DAIMON_MOVE_TEMPLATE_DATA_FILE, "r", encoding="utf-8") as f:
            daimon_move_template_data = json.load(f)
            daimon_move_template_global = [DaimonMoveTemplate.from_dict(d) for d in daimon_move_template_data]
            print(f"Loaded {len(daimon_move_template_global)} Daimon Move Template")
    else:
        raise FileNotFoundError(f"{DAIMON_MOVE_TEMPLATE_DATA_FILE} not found")

def get_daimon_move_template_by_id(daimon_move_template_id: int) -> Optional[DaimonMoveTemplate]:
    for daimon_move_template in daimon_move_template_global:
        if daimon_move_template.daimon_move_template_id == daimon_move_template_id:
            return daimon_move_template
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Daimon Move - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_daimon_move():
    global daimon_move_global
    if DAIMON_MOVE_DATA_FILE.exists():
        with open(DAIMON_MOVE_DATA_FILE, "r", encoding="utf-8") as f:
            daimon_move_data = json.load(f)
            daimon_move_global = [DaimonMove.from_dict(d) for d in daimon_move_data]
            print(f"Loaded {len(daimon_move_global)} Daimon Move")
    else:
        raise FileNotFoundError(f"{DAIMON_MOVE_DATA_FILE} not found")
   
def save_all_daimon_move():
    with open(DAIMON_MOVE_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([daimon_move.to_dict() for daimon_move in daimon_move_global], f, indent=4)
        print(f"Saved {len(daimon_move_global)} Daimon Move")

def get_daimon_move_by_id(daimon_move_id: int) -> Optional[DaimonMove]:
    for daimon_move in daimon_move_global:
        if daimon_move.daimon_move_id == daimon_move_id:
            return daimon_move
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Daimon Template - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_daimon_template():
    global daimon_template_global
    if DAIMON_TEMPLATE_DATA_FILE.exists():
        with open(DAIMON_TEMPLATE_DATA_FILE, "r", encoding="utf-8") as f:
            daimon_template_data = json.load(f)
            daimon_template_global = [DaimonTemplate.from_dict(d) for d in daimon_template_data]
            print(f"Loaded {len(daimon_template_global)} Daimon Template")
    else:
        raise FileNotFoundError(f"{DAIMON_TEMPLATE_DATA_FILE} not found")

def get_daimon_template_by_id(daimon_template_id: int) -> Optional[DaimonTemplate]:
    for daimon_template in daimon_template_global:
        if daimon_template.daimon_template_id == daimon_template_id:
            return daimon_template
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Daimon Unbonded - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_daimon_unbonded():
    global daimon_unbonded_global
    if DAIMON_UNBONDED_DATA_FILE.exists():
        with open(DAIMON_UNBONDED_DATA_FILE, "r", encoding="utf-8") as f:
            daimon_unbonded_data = json.load(f)
            daimon_unbonded_global = [DaimonUnbonded.from_dict(d) for d in daimon_unbonded_data]
            print(f"Loaded {len(daimon_unbonded_global)} Daimon Unbonded")
    else:
        raise FileNotFoundError(f"{DAIMON_UNBONDED_DATA_FILE} not found")
    
def save_all_daimon_unbonded():
    with open(DAIMON_UNBONDED_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([daimon_unbonded.to_dict() for daimon_unbonded in daimon_unbonded_global], f, indent=4)
        print(f"Saved {len(daimon_unbonded_global)} Daimon Unbonded")

def get_daimon_unbonded_by_id(daimon_unbonded_id: int) -> Optional[DaimonUnbonded]:
    for daimon_unbonded in daimon_unbonded_global:
        if daimon_unbonded.daimon_unbonded_id == daimon_unbonded_id:
            return daimon_unbonded
    return None

# ----------------------------------------------------------------------------------------------------
# UPDATED Daimon Bonded - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_daimon_bonded():
    global daimon_bonded_global
    if DAIMON_BONDED_DATA_FILE.exists():
        with open(DAIMON_BONDED_DATA_FILE, "r", encoding="utf-8") as f:
            daimon_bonded_data = json.load(f)
            daimon_bonded_global = [DaimonBonded.from_dict(d) for d in daimon_bonded_data]
            print(f"Loaded {len(daimon_bonded_global)} Daimon Bonded")
    else:
        raise FileNotFoundError(f"{DAIMON_BONDED_DATA_FILE} not found")
    
def save_all_daimon_bonded():
    with open(DAIMON_BONDED_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([daimon_bonded.to_dict() for daimon_bonded in daimon_bonded_global], f, indent=4)
        print(f"Saved {len(daimon_bonded_global)} Daimon Bonded")

def get_daimon_bonded_by_id(daimon_bonded_id: int) -> Optional[DaimonBonded]:
    for daimon_bonded in daimon_bonded_global:
        if daimon_bonded.daimon_bonded_id == daimon_bonded_id:
            return daimon_bonded
    return None



# ----------------------------------------------------------------------------------------------------
# NPC Item Inventory - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_npc_item_inventory():
    global npc_item_inventory_global
    if NPC_ITEM_INVENTORY_DATA_FILE.exists():
        with open(NPC_ITEM_INVENTORY_DATA_FILE, "r", encoding="utf-8") as f:
            npc_item_inventory_data = json.load(f)
            npc_item_inventory_global = [NPCItemInventory.from_dict(d) for d in npc_item_inventory_data]
            print(f"Loaded {len(npc_item_inventory_global)} NPC Item Inventory")
    else:
        raise FileNotFoundError(f"{NPC_ITEM_INVENTORY_DATA_FILE} not found")
    
def save_all_npc_item_inventory():
    with open(NPC_ITEM_INVENTORY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([npc_item_inventory.to_dict() for npc_item_inventory in npc_item_inventory_global], f, indent=4)
        print(f"Saved {len(npc_item_inventory_global)} NPC Item Inventory")

def get_npc_item_inventory_by_id(npc_item_inventory_id: int) -> Optional[NPCItemInventory]:
    for npc_item_inventory in npc_item_inventory_global:
        if npc_item_inventory.npc_item_inventory_id == npc_item_inventory_id:
            return npc_item_inventory
    return None

# ----------------------------------------------------------------------------------------------------
# NPC Daimon Dex Entry - Nonstatic data, need to save back to file. 
# ----------------------------------------------------------------------------------------------------
def load_all_npc_daimon_dex_entry():
    global npc_daimon_dex_entry_global
    if NPC_DAIMON_DEX_ENTRY_DATA_FILE.exists():
        with open(NPC_DAIMON_DEX_ENTRY_DATA_FILE, "r", encoding="utf-8") as f:
            npc_daimon_dex_entry_data = json.load(f)
            npc_daimon_dex_entry_global = [NPCDaimonDexEntry.from_dict(d) for d in npc_daimon_dex_entry_data]
            print(f"Loaded {len(npc_daimon_dex_entry_global)} NPC Daimon Dex Entry")
    else:
        raise FileNotFoundError(f"{NPC_DAIMON_DEX_ENTRY_DATA_FILE} not found")
    
def save_all_npc_daimon_dex_entry():
    with open(NPC_DAIMON_DEX_ENTRY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([npc_daimon_dex_entry.to_dict() for npc_daimon_dex_entry in npc_daimon_dex_entry_global], f, indent=4)
        print(f"Saved {len(npc_daimon_dex_entry_global)} NPC Daimon Dex Entry")

def get_npc_daimon_dex_entry_by_id(npc_daimon_dex_entry_id: int) -> Optional[NPCDaimonDexEntry]:
    for npc_daimon_dex_entry in npc_daimon_dex_entry_global:
        if npc_daimon_dex_entry.npc_daimon_dex_entry_id == npc_daimon_dex_entry_id:
            return npc_daimon_dex_entry
    return None

# ----------------------------------------------------------------------------------------------------
# NPC Daimon Dex - Nonstatic data, need to save back to file. 
# ----------------------------------------------------------------------------------------------------
def load_all_npc_daimon_dex():
    global npc_daimon_dex_global
    if NPC_DAIMON_DEX_DATA_FILE.exists():
        with open(NPC_DAIMON_DEX_DATA_FILE, "r", encoding="utf-8") as f:
            npc_daimon_dex_data = json.load(f)
            npc_daimon_dex_global = [NPCDaimonDex.from_dict(d) for d in npc_daimon_dex_data]
            print(f"Loaded {len(npc_daimon_dex_global)} NPC Daimon Dex")
    else:
        raise FileNotFoundError(f"{NPC_DAIMON_DEX_DATA_FILE} not found")
    
def save_all_npc_daimon_dex():
    with open(NPC_DAIMON_DEX_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([npc_daimon_dex.to_dict() for npc_daimon_dex in npc_daimon_dex_global], f, indent=4)
        print(f"Saved {len(npc_daimon_dex_global)} NPC Daimon Dex")

def get_npc_daimon_dex_by_id(npc_daimon_dex_id: int) -> Optional[NPCDaimonDex]:
    for npc_daimon_dex in npc_daimon_dex_global:
        if npc_daimon_dex.npc_daimon_dex_id == npc_daimon_dex_id:
            return npc_daimon_dex
    return None

# ----------------------------------------------------------------------------------------------------
# NPC Daimon Inventory - Nonstatic data, need to save back to file. 
# ----------------------------------------------------------------------------------------------------
def load_all_npc_daimon_inventory():
    global npc_daimon_inventory_global
    if NPC_DAIMON_INVENTORY_DATA_FILE.exists():
        with open(NPC_DAIMON_INVENTORY_DATA_FILE, "r", encoding="utf-8") as f:
            npc_daimon_inventory_data = json.load(f)
            npc_daimon_inventory_global = [NPCDaimonInventory.from_dict(d) for d in npc_daimon_inventory_data]
            print(f"Loaded {len(npc_daimon_inventory_global)} NPC Daimon Inventory")
    else:
        raise FileNotFoundError(f"{NPC_DAIMON_INVENTORY_DATA_FILE} not found")
    
def save_all_npc_daimon_inventory():
    with open(NPC_DAIMON_INVENTORY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([npc_daimon_inventory.to_dict() for npc_daimon_inventory in npc_daimon_inventory_global], f, indent=4)
        print(f"Saved {len(npc_daimon_inventory_global)} NPC Daimon Inventory")

def get_npc_daimon_inventory_by_id(npc_daimon_inventory_id: int) -> Optional[NPCDaimonInventory]:
    for npc_daimon_inventory in npc_daimon_inventory_global:
        if npc_daimon_inventory.npc_daimon_inventory_id == npc_daimon_inventory_id:
            return npc_daimon_inventory
    return None

# ----------------------------------------------------------------------------------------------------
# NPC Main Quest Inventory - Nonstatic data, need to save back to file. 
# ----------------------------------------------------------------------------------------------------
def load_all_npc_quest_main_inventory():
    global npc_quest_main_inventory_global
    if NPC_QUEST_MAIN_INVENTORY_DATA_FILE.exists():
        with open(NPC_QUEST_MAIN_INVENTORY_DATA_FILE, "r", encoding="utf-8") as f:
            npc_quest_main_inventory_data = json.load(f)
            npc_quest_main_inventory_global = [NPCQuestMainInventory.from_dict(d) for d in npc_quest_main_inventory_data]
            print(f"Loaded {len(npc_quest_main_inventory_global)} NPC Quest Main Inventory")
    else:
        raise FileNotFoundError(f"{NPC_QUEST_MAIN_INVENTORY_DATA_FILE} not found")
    
def save_all_npc_quest_main_inventory():
    with open(NPC_QUEST_MAIN_INVENTORY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([npc_quest_main_inventory.to_dict() for npc_quest_main_inventory in npc_quest_main_inventory_global], f, indent=4)
        print(f"Saved {len(npc_quest_main_inventory_global)} NPC Quest Main Inventory")

def get_npc_quest_main_inventory_by_id(npc_quest_main_inventory_id: int) -> Optional[NPCQuestMainInventory]:
    for npc_quest_main_inventory in npc_quest_main_inventory_global:
        if npc_quest_main_inventory.npc_quest_main_inventory_id == npc_quest_main_inventory_id:
            return npc_quest_main_inventory
    return None

# ----------------------------------------------------------------------------------------------------
# NPC Side Quest Inventory - Nonstatic data, need to save back to file. 
# ----------------------------------------------------------------------------------------------------
def load_all_npc_quest_side_inventory():
    global npc_quest_side_inventory_global
    if NPC_QUEST_SIDE_INVENTORY_DATA_FILE.exists():
        with open(NPC_QUEST_SIDE_INVENTORY_DATA_FILE, "r", encoding="utf-8") as f:
            npc_quest_side_inventory_data = json.load(f)
            npc_quest_side_inventory_global = [NPCQuestSideInventory.from_dict(d) for d in npc_quest_side_inventory_data]
            print(f"Loaded {len(npc_quest_side_inventory_global)} NPC Quest Side Inventory")
    else:
        raise FileNotFoundError(f"{NPC_QUEST_SIDE_INVENTORY_DATA_FILE} not found")
    
def save_all_npc_quest_side_inventory():
    with open(NPC_QUEST_SIDE_INVENTORY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([npc_quest_side_inventory.to_dict() for npc_quest_side_inventory in npc_quest_side_inventory_global], f, indent=4)
        print(f"Saved {len(npc_quest_side_inventory_global)} NPC Quest Side Inventory")
        
def get_npc_quest_side_inventory_by_id(npc_quest_side_inventory_id: int) -> Optional[NPCQuestSideInventory]:
    for npc_quest_side_inventory in npc_quest_side_inventory_global:
        if npc_quest_side_inventory.npc_quest_side_inventory_id == npc_quest_side_inventory_id:
            return npc_quest_side_inventory
    return None

# ----------------------------------------------------------------------------------------------------
# NPC - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_npc():
    global npc_global
    if NPC_DATA_FILE.exists():
        with open(NPC_DATA_FILE, "r", encoding="utf-8") as f:
            npc_data = json.load(f)
            npc_global = [NPC.from_dict(d) for d in npc_data]
            print(f"Loaded {len(npc_global)} NPC")
    else:
        raise FileNotFoundError(f"{NPC_DATA_FILE} not found")
    
def save_all_npc():
    with open(NPC_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([npc.to_dict() for npc in npc_global], f, indent=4)
        print(f"Saved {len(npc_global)} NPC")

def get_npc_by_id(npc_id: int) -> Optional[NPC]:
    for npc in npc_global:
        if npc.npc_id == npc_id:
            return npc
    return None



# ----------------------------------------------------------------------------------------------------
# Player Item Inventory - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_player_item_inventory():
    global player_item_inventory_global
    if PLAYER_ITEM_INVENTORY_DATA_FILE.exists():
        with open(PLAYER_ITEM_INVENTORY_DATA_FILE, "r", encoding="utf-8") as f:
            player_item_inventory_data = json.load(f)
            player_item_inventory_global = [PlayerItemInventory.from_dict(d) for d in player_item_inventory_data]
            print(f"Loaded {len(player_item_inventory_global)} Player Item Inventory")
    else:
        raise FileNotFoundError(f"{PLAYER_ITEM_INVENTORY_DATA_FILE} not found")
    
def save_all_player_item_inventory():
    with open(PLAYER_ITEM_INVENTORY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([player_item_inventory.to_dict() for player_item_inventory in player_item_inventory_global], f, indent=4)
        print(f"Saved {len(player_item_inventory_global)} Player Item Inventory")

def get_player_item_inventory_by_id(player_item_inventory_id: int) -> Optional[PlayerItemInventory]:
    for player_item_inventory in player_item_inventory_global:
        if player_item_inventory.player_item_inventory_id == player_item_inventory_id:
            return player_item_inventory
    return None

# ----------------------------------------------------------------------------------------------------
# Player Daimon Dex Entry - Nonstatic data, need to save back to file. 
# ----------------------------------------------------------------------------------------------------
def load_all_player_daimon_dex_entry():
    global player_daimon_dex_entry_global
    if PLAYER_DAIMON_DEX_ENTRY_DATA_FILE.exists():
        with open(PLAYER_DAIMON_DEX_ENTRY_DATA_FILE, "r", encoding="utf-8") as f:
            player_daimon_dex_entry_data = json.load(f)
            player_daimon_dex_entry_global = [PlayerDaimonDexEntry.from_dict(d) for d in player_daimon_dex_entry_data]
            print(f"Loaded {len(player_daimon_dex_entry_global)} Player Daimon Dex Entry")
    else:
        raise FileNotFoundError(f"{PLAYER_DAIMON_DEX_ENTRY_DATA_FILE} not found")
    
def save_all_player_daimon_dex_entry():
    with open(PLAYER_DAIMON_DEX_ENTRY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([player_daimon_dex_entry.to_dict() for player_daimon_dex_entry in player_daimon_dex_entry_global], f, indent=4)
        print(f"Saved {len(player_daimon_dex_entry_global)} Player Daimon Dex Entry")

def get_player_daimon_dex_entry_by_id(player_daimon_dex_entry_id: int) -> Optional[PlayerDaimonDexEntry]:
    for player_daimon_dex_entry in player_daimon_dex_entry_global:
        if player_daimon_dex_entry.player_daimon_dex_entry_id == player_daimon_dex_entry_id:
            return player_daimon_dex_entry
    return None

# ----------------------------------------------------------------------------------------------------
# Player Daimon Dex - Nonstatic data, need to save back to file. 
# ----------------------------------------------------------------------------------------------------
def load_all_player_daimon_dex():
    global player_daimon_dex_global
    if PLAYER_DAIMON_DEX_DATA_FILE.exists():
        with open(PLAYER_DAIMON_DEX_DATA_FILE, "r", encoding="utf-8") as f:
            player_daimon_dex_data = json.load(f)
            player_daimon_dex_global = [PlayerDaimonDex.from_dict(d) for d in player_daimon_dex_data]
            print(f"Loaded {len(player_daimon_dex_global)} Player Daimon Dex")
    else:
        raise FileNotFoundError(f"{PLAYER_DAIMON_DEX_DATA_FILE} not found")
    
def save_all_player_daimon_dex():
    with open(PLAYER_DAIMON_DEX_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([player_daimon_dex.to_dict() for player_daimon_dex in player_daimon_dex_global], f, indent=4)
        print(f"Saved {len(player_daimon_dex_global)} Player Daimon Dex")

def get_player_daimon_dex_by_id(player_daimon_dex_id: int) -> Optional[PlayerDaimonDex]:
    for player_daimon_dex in player_daimon_dex_global:
        if player_daimon_dex.player_daimon_dex_id == player_daimon_dex_id:
            return player_daimon_dex
    return None

# ----------------------------------------------------------------------------------------------------
# Player Daimon Inventory - Nonstatic data, need to save back to file. 
# ----------------------------------------------------------------------------------------------------
def load_all_player_daimon_inventory():
    global player_daimon_inventory_global
    if PLAYER_DAIMON_INVENTORY_DATA_FILE.exists():
        with open(PLAYER_DAIMON_INVENTORY_DATA_FILE, "r", encoding="utf-8") as f:
            player_daimon_inventory_data = json.load(f)
            player_daimon_inventory_global = [PlayerDaimonInventory.from_dict(d) for d in player_daimon_inventory_data]
            print(f"Loaded {len(player_daimon_inventory_global)} Player Daimon Inventory")
    else:
        raise FileNotFoundError(f"{PLAYER_DAIMON_INVENTORY_DATA_FILE} not found")
    
def save_all_player_daimon_inventory():
    with open(PLAYER_DAIMON_INVENTORY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([player_daimon_inventory.to_dict() for player_daimon_inventory in player_daimon_inventory_global], f, indent=4)
        print(f"Saved {len(player_daimon_inventory_global)} Player Daimon Inventory")
        
def get_player_daimon_inventory_by_id(player_daimon_inventory_id: int) -> Optional[PlayerDaimonInventory]:
    for player_daimon_inventory in player_daimon_inventory_global:
        if player_daimon_inventory.player_daimon_inventory_id == player_daimon_inventory_id:
            return player_daimon_inventory
    return None

# ----------------------------------------------------------------------------------------------------
# Player Quest Main Inventory - Nonstatic data, need to save back to file. 
# ----------------------------------------------------------------------------------------------------
def load_all_player_quest_main_inventory():
    global player_quest_main_inventory_global
    if PLAYER_QUEST_MAIN_INVENTORY_DATA_FILE.exists():
        with open(PLAYER_QUEST_MAIN_INVENTORY_DATA_FILE, "r", encoding="utf-8") as f:
            player_quest_main_inventory_data = json.load(f)
            player_quest_main_inventory_global = [PlayerQuestMainInventory.from_dict(d) for d in player_quest_main_inventory_data]
            print(f"Loaded {len(player_quest_main_inventory_global)} Player Quest Main Inventory")
    else:
        raise FileNotFoundError(f"{PLAYER_QUEST_MAIN_INVENTORY_DATA_FILE} not found")
    
def save_all_player_quest_main_inventory():
    with open(PLAYER_QUEST_MAIN_INVENTORY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([player_quest_main_inventory.to_dict() for player_quest_main_inventory in player_quest_main_inventory_global], f, indent=4)
        print(f"Saved {len(player_quest_main_inventory_global)} Player Quest Main Inventory")
        
def get_player_quest_main_inventory_by_id(player_quest_main_inventory_id: int) -> Optional[PlayerQuestMainInventory]:
    for player_quest_main_inventory in player_quest_main_inventory_global:
        if player_quest_main_inventory.player_quest_main_inventory_id == player_quest_main_inventory_id:
            return player_quest_main_inventory
    return None

# ----------------------------------------------------------------------------------------------------
# Player Side Quest Inventory - Nonstatic data, need to save back to file. 
# ----------------------------------------------------------------------------------------------------
def load_all_player_quest_side_inventory():
    global player_quest_side_inventory_global
    if PLAYER_QUEST_SIDE_INVENTORY_DATA_FILE.exists():
        with open(PLAYER_QUEST_SIDE_INVENTORY_DATA_FILE, "r", encoding="utf-8") as f:
            player_quest_side_inventory_data = json.load(f)
            player_quest_side_inventory_global = [PlayerQuestSideInventory.from_dict(d) for d in player_quest_side_inventory_data]
            print(f"Loaded {len(player_quest_side_inventory_global)} Player Quest Side Inventory")
    else:
        raise FileNotFoundError(f"{PLAYER_QUEST_SIDE_INVENTORY_DATA_FILE} not found")
    
def save_all_player_quest_side_inventory():
    with open(PLAYER_QUEST_SIDE_INVENTORY_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([player_quest_side_inventory.to_dict() for player_quest_side_inventory in player_quest_side_inventory_global], f, indent=4)
        (f"Saved {len(player_quest_side_inventory_global)} Player Quest Side Inventory")

def get_player_quest_side_inventory_by_id(player_quest_side_inventory_id: int) -> Optional[PlayerQuestSideInventory]:
    for player_quest_side_inventory in player_quest_side_inventory_global:
        if player_quest_side_inventory.player_quest_side_inventory_id == player_quest_side_inventory_id:
            return player_quest_side_inventory
    return None

# ----------------------------------------------------------------------------------------------------
# Player - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_player():
    global player_global
    if PLAYER_DATA_FILE.exists():
        with open(PLAYER_DATA_FILE, "r", encoding="utf-8") as f:
            player_data = json.load(f)
            player_global = [Player.from_dict(d) for d in player_data]
            print(f"Loaded {len(player_global)} Player")
    else:
        raise FileNotFoundError(f"{PLAYER_DATA_FILE} not found")
    
def save_all_player():
    with open(PLAYER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([player.to_dict() for player in player_global], f, indent=4)
        print(f"Saved {len(player_global)} Player")

def get_player_by_id(player_id: int) -> Optional[Player]:
    for player in player_global:
        if player.player_id == player_id:
            return player
    return None

# ----------------------------------------------------------------------------------------------------
# Quest Step Template - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_quest_step_template():
    global quest_step_template_global
    if QUEST_STEP_TEMPLATE_DATA_FILE.exists():
        with open(QUEST_STEP_TEMPLATE_DATA_FILE, "r", encoding="utf-8") as f:
            quest_step_template_data = json.load(f)
            quest_step_template_global = [QuestStepTemplate.from_dict(d) for d in quest_step_template_data]
            print(f"Loaded {len(quest_step_template_global)} Quest Step Template")
    else:
        quest_step_template_global = []

def get_quest_step_template_by_id(quest_step_template_id: int) -> Optional[QuestStepTemplate]:
    for quest_step_template in quest_step_template_global:
        if quest_step_template.quest_step_template_id == quest_step_template_id:
            return quest_step_template
    return None

# ----------------------------------------------------------------------------------------------------
# Quest Step - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_quest_step():
    global quest_step_global
    if QUEST_STEP_DATA_FILE.exists():
        with open(QUEST_STEP_DATA_FILE, "r", encoding="utf-8") as f:
            quest_step_data = json.load(f)
            quest_step_global = [QuestStep.from_dict(d) for d in quest_step_data]
            print(f"Loaded {len(quest_step_global)} Quest Step")
    else:
        quest_step_global = []

def save_all_quest_step():
    with open(QUEST_STEP_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([quest_step.to_dict() for quest_step in quest_step_global], f, indent=4)

def get_quest_step_by_id(quest_step_id: int) -> Optional[QuestStep]:
    for quest_step in quest_step_global:
        if quest_step.quest_step_id == quest_step_id:
            return quest_step
    return None

# ----------------------------------------------------------------------------------------------------
# Quest Type - Static data, no need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_quest_type():
    global quest_type_global
    if QUEST_TYPE_DATA_FILE.exists():
        with open(QUEST_TYPE_DATA_FILE, "r", encoding="utf-8") as f:
            quest_type_data = json.load(f)
            quest_type_global = [QuestType.from_dict(d) for d in quest_type_data]
            print(f"Loaded {len(quest_type_global)} Quest Type")
    else:
        quest_type_global = []

def get_quest_type_by_id(quest_type_id: int) -> Optional[QuestType]:
    for quest_type in quest_type_global:
        if quest_type.quest_type_id == quest_type_id:
            return quest_type
    return None

# ----------------------------------------------------------------------------------------------------
# Quest Main - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_quest_main():
    global quest_main_global
    if QUEST_MAIN_DATA_FILE.exists():
        with open(QUEST_MAIN_DATA_FILE, "r", encoding="utf-8") as f:
            quest_main_data = json.load(f)
            quest_main_global = [QuestMain.from_dict(d) for d in quest_main_data]
            print(f"Loaded {len(quest_main_global)} Quest Side")
    else:
        quest_main_global = []

def save_all_quest_main():
    with open(QUEST_MAIN_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([quest_main.to_dict() for quest_main in quest_main_global], f, indent=4)
        print(f"Saved {len(quest_main_global)} Quest Main")

def get_quest_main_by_id(quest_main_id: int) -> Optional[QuestMain]:
    for quest_main in quest_main_global:
        if quest_main.quest_main_id == quest_main_id:
            return quest_main
    return None

# ----------------------------------------------------------------------------------------------------
# Quest Side - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_quest_side():
    global quest_side_global
    if QUEST_SIDE_DATA_FILE.exists():
        with open(QUEST_SIDE_DATA_FILE, "r", encoding="utf-8") as f:
            quest_side_data = json.load(f)
            quest_side_global = [QuestSide.from_dict(d) for d in quest_side_data]
            print(f"Loaded {len(quest_side_global)} Quest Side")
    else:
        quest_side_global = []

def save_all_quest_side():
    with open(QUEST_SIDE_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([quest_side.to_dict() for quest_side in quest_side_global], f, indent=4)

def get_quest_side_by_id(quest_side_id: int) -> Optional[QuestSide]:
    for quest_side in quest_side_global:
        if quest_side.quest_side_id == quest_side_id:
            return quest_side
    return None

# ----------------------------------------------------------------------------------------------------
# Daimon Battle - Nonstatic data, need to save back to file.
# ----------------------------------------------------------------------------------------------------
def load_all_system_daimon_battle():
    global daimon_battle_global
    if SYSTEM_DAIMON_BATTLE_DATA_FILE.exists():
        with open(SYSTEM_DAIMON_BATTLE_DATA_FILE, "r", encoding="utf-8") as f:
            daimon_battle_data = json.load(f)
            daimon_battle_global = [SystemDaimonBattle.from_dict(d) for d in daimon_battle_data]
    else:
        daimon_battle_global = []

def save_all_system_daimon_battle():
    with open(SYSTEM_DAIMON_BATTLE_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([daimon_battle.to_dict() for daimon_battle in daimon_battle_global], f, indent=4)

def get_system_daimon_battle_by_id(daimon_battle_id: int) -> Optional[SystemDaimonBattle]:
    for daimon_battle in daimon_battle_global:
        if daimon_battle.daimon_battle_id == daimon_battle_id:
            return daimon_battle
    return None


def generate_random_item_generic(player: "Player") -> Optional[Item]:
    """
    Generates a generic (stackable) Item object.
    Hex codes come from the template, 1–10.
    """
    location = player.player_location
    spawn_roll = random.random()
    print(f"EL SPAWN ROLL {spawn_roll} & LOCATION SPAWN RATE {location.location_item_base_spawn_rate}")   #DELETE
    if spawn_roll > location.location_item_base_spawn_rate:
        print("Shouldn't have spawned something") #DELETE
        return None

    spawn_candidates = [
        (item_template, spawn_weight)
        for entry in location.location_item_base_spawn_pool
        for spawn_weight, item_template in entry.items()
        if item_template and spawn_weight > 0 and item_template.item_template_category in ITEM_CATEGORY_GENERIC
    ]
    if not spawn_candidates:
        print("No spawn candidates.")
        return None

    templates, weights = zip(*spawn_candidates)
    random_item_template = random.choices(templates, weights=weights, k=1)[0]

    item_quantity = 1 if random_item_template.item_template_category == "Clothing" else random.randint(1, 10)

    new_item = Item(
        item_id          = len(item_global) + 1,
        item_name        = random_item_template.item_template_name,
        item_description = random_item_template.item_template_description,
        item_category    = random_item_template.item_template_category,
        item_actions     = random_item_template.item_template_actions,
        item_base_value  = random_item_template.item_template_base_value,
        item_hex_code_1  = random_item_template.item_template_base_hex_code_1,
        item_hex_code_2  = random_item_template.item_template_base_hex_code_2,
        item_hex_code_3  = random_item_template.item_template_base_hex_code_3,
        item_hex_code_4  = random_item_template.item_template_base_hex_code_4,
        item_hex_code_5  = random_item_template.item_template_base_hex_code_5,
        item_hex_code_6  = random_item_template.item_template_base_hex_code_6,
        item_hex_code_7  = random_item_template.item_template_base_hex_code_7,
        item_hex_code_8  = random_item_template.item_template_base_hex_code_8,
        item_hex_code_9  = random_item_template.item_template_base_hex_code_9,
        item_hex_code_10 = random_item_template.item_template_base_hex_code_10,
        item_quantity    = item_quantity,
    )

    print(f"Created new item {new_item}!")

    item_global.append(new_item)
    return new_item

def generate_random_item_unique(player: "Player") -> Optional[Item]:
    """
    Generates a unique (non-stackable) Item object.
    Randomizes 10 hex codes.
    """
    location = player.player_location
    spawn_roll = random.random()
    if spawn_roll > location.location_item_base_spawn_rate:
        return None

    spawn_candidates = [
        (item_template, spawn_weight)
        for entry in location.location_item_base_spawn_pool
        for spawn_weight, item_template in entry.items()
        if item_template and spawn_weight > 0 and item_template.item_template_category in ITEM_CATEGORY_UNIQUE
    ]
    if not spawn_candidates:
        return None

    templates, weights = zip(*spawn_candidates)
    random_item_template = random.choices(templates, weights=weights, k=1)[0]

    item_quantity = 1 if random_item_template.item_template_category == "Clothing" else random.randint(1, 10)

    # Generate 10 random hex codes
    hex_codes = ["#" + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in range(10)]

    new_item = Item(
        item_id          = len(item_global) + 1,
        item_name        = random_item_template.item_template_name,
        item_description = random_item_template.item_template_description,
        item_category    = random_item_template.item_template_category,
        item_actions     = random_item_template.item_template_actions,
        item_base_value  = random_item_template.item_template_base_value,
        item_hex_code_1  = hex_codes[0],
        item_hex_code_2  = hex_codes[1],
        item_hex_code_3  = hex_codes[2],
        item_hex_code_4  = hex_codes[3],
        item_hex_code_5  = hex_codes[4],
        item_hex_code_6  = hex_codes[5],
        item_hex_code_7  = hex_codes[6],
        item_hex_code_8  = hex_codes[7],
        item_hex_code_9  = hex_codes[8],
        item_hex_code_10 = hex_codes[9],
        item_quantity    = item_quantity,
    )

    item_global.append(new_item)
    return new_item

def generate_random_daimon_unbonded(location: "Location") -> Optional[DaimonUnbonded]:
    """
    Generates a DaimonUnbonded object based on the given Location.
    Uses the location's spawn rate and per-Daimon spawn chances.
    Returns None if no Daimon spawns.
    """

    # 1️⃣ Location spawn rate check
    spawn_roll = random.random()
    if spawn_roll > location.location_daimon_base_spawn_rate:
        print(f"No Daimon spawned at {location.location_name} (roll={spawn_roll:.2f}, rate={location.location_daimon_base_spawn_rate}).")
        return None

    # 2️⃣ Flatten spawn list
    spawn_candidates = []
    for entry in location.location_daimon_base_spawn_pool:
        for spawn_weight, daimon_template in entry.items():
            if daimon_template is not None and spawn_weight > 0:
                spawn_candidates.append((daimon_template, spawn_weight))

    if not spawn_candidates:
        print(f"No valid Daimon Templates to spawn at {location.location_name}.")
        return None

    # 3️⃣ Weighted choice
    templates = [template for template, _ in spawn_candidates]
    weights = [weight for _, weight in spawn_candidates]
    random_daimon_template = random.choices(templates, weights=weights, k=1)[0]

    print(f"Selected Daimon Template: {random_daimon_template.daimon_template_species}")

    # 4️⃣ Determine level
    # Flatten all evolution stages into one ordered list
    evolution_stages = []
    for evo_field in [random_daimon_template.daimon_template_evolution_1,
                    random_daimon_template.daimon_template_evolution_2,
                    random_daimon_template.daimon_template_evolution_3]:
        if isinstance(evo_field, list) and evo_field and evo_field[0]:  # skip empty dicts
            evolution_stages.extend(evo_field)

    # Find the stage that matches the Daimon's current template ID
    current_stage = next(
        (stage for stage in evolution_stages if stage["daimon_template_evolution_id"] == random_daimon_template.daimon_template_id),
        None
    )

    if current_stage is None:
        raise ValueError(f"No evolution stage found for template ID {random_daimon_template.daimon_template_id}")

    min_level = current_stage["daimon_template_evolution_level"]

    # Find the next evolution stage (with a higher level than the current one)
    next_stage = next(
        (stage for stage in evolution_stages if stage["daimon_template_evolution_level"] > min_level),
        None
    )

    max_level = next_stage["daimon_template_evolution_level"] - 1 if next_stage else 100

    # Randomize level and progress
    daimon_level = random.randint(min_level, max_level)
    daimon_level_progress = round(random.random(), 2)

    print(f"Min: {min_level}, Max: {max_level}, Level: {daimon_level}, Progress: {daimon_level_progress}")

    # 11️⃣ Calculate level-based stats
    daimon_stat_health = round(random_daimon_template.daimon_template_stat_base_health * daimon_level, 2)
    daimon_stat_physical_attack = round(random_daimon_template.daimon_template_stat_base_physical_attack * daimon_level, 2)
    daimon_stat_special_attack = round(random_daimon_template.daimon_template_stat_base_special_attack * daimon_level, 2)
    daimon_stat_physical_defense = round(random_daimon_template.daimon_template_stat_base_physical_defense * daimon_level, 2)
    daimon_stat_special_defense = round(random_daimon_template.daimon_template_stat_base_special_defense * daimon_level, 2)
    daimon_stat_speed = round(random_daimon_template.daimon_template_stat_base_speed * daimon_level, 2)

    # 5️⃣ Gender
    gender_options = list(random_daimon_template.daimon_template_gender_distribution.keys())
    gender_weights = list(random_daimon_template.daimon_template_gender_distribution.values())
    daimon_gender = random.choices(gender_options, weights=gender_weights, k=1)[0]

    # 6️⃣ Height & Weight
    height_mean = random_daimon_template.daimon_template_height_distribution.get("daimon_template_height_mean", 1)
    height_range = random_daimon_template.daimon_template_height_distribution.get("daimon_template_height_range", 0)
    daimon_height = round(random.uniform(height_mean - height_range, height_mean + height_range), 2)

    weight_mean = random_daimon_template.daimon_template_weight_distribution.get("daimon_template_weight_mean", 1)
    weight_range = random_daimon_template.daimon_template_weight_distribution.get("daimon_template_weight_range", 0)
    daimon_weight = round(random.uniform(weight_mean - weight_range, weight_mean + weight_range), 2)

    # Max Health, Current Health & Current Status
    daimon_max_health = daimon_stat_health * 2 + daimon_level
    daimon_current_health = daimon_max_health

    daimon_status_template = get_daimon_status_template_by_id(1)
    daimon_status = DaimonStatus.from_dict({
        "daimon_status_id"               : daimon_status_template.daimon_status_template_id,
        "daimon_status_name"             : daimon_status_template.daimon_status_template_name,
        "daimon_status_description"      : daimon_status_template.daimon_status_template_description,
        "daimon_status_effect"           : daimon_status_template.daimon_status_template_effect,
        "daimon_status_duration_max"     : daimon_status_template.daimon_status_template_duration_max,
        "daimon_status_duration_current" : daimon_status_template.daimon_status_template_duration_max
        }
    )

    # 7️⃣ Types
    daimon_type_1 = random_daimon_template.daimon_template_type_1
    daimon_type_2 = random_daimon_template.daimon_template_type_2

    # Abilities
    daimon_ability_pool = [
        option for option in random_daimon_template.daimon_template_ability_pool
        if option.get("daimon_ability") is not None
    ]

    if daimon_ability_pool:
        daimon_ability_options = [option["daimon_ability"] for option in daimon_ability_pool]
        daimon_ability_weights = [option["daimon_ability_weight"] for option in daimon_ability_pool]

        daimon_ability = random.choices(daimon_ability_options, daimon_ability_weights, k=1)[0]

    # 8️⃣ Moves
    available_daimon_move_templates = [
        move_entry["daimon_template_move_template"]
        for move_entry in random_daimon_template.daimon_template_move_template_pool
        if move_entry["daimon_template_move_template_level_requirement"] <= daimon_level
    ]

    # Convert each template into a DaimonMove object
    available_moves: List[Optional[DaimonMove]] = [
        DaimonMove.from_dict({
            "daimon_move_id"                 : daimon_move_template.daimon_move_template_id,
            "daimon_move_name"               : daimon_move_template.daimon_move_template_name,
            "daimon_move_type"               : daimon_move_template.daimon_move_template_type,
            "daimon_move_description"        : daimon_move_template.daimon_move_template_description,
            "daimon_move_category"           : daimon_move_template.daimon_move_template_category,
            "daimon_move_power"              : daimon_move_template.daimon_move_template_power,
            "daimon_move_accuracy"           : daimon_move_template.daimon_move_template_accuracy,
            "daimon_move_points_max"         : daimon_move_template.daimon_move_template_points_max,
            "daimon_move_points_base"        : daimon_move_template.daimon_move_template_points_base,
            "daimon_move_points_current"     : daimon_move_template.daimon_move_template_points_base,
            "daimon_move_effect_status": [
                {
                    "daimon_move_status": DaimonStatus.from_dict({
                        "daimon_status_id"               : daimon_move_template_effect_status.get("daimon_move_template_status").daimon_status_template_id,
                        "daimon_status_name"             : daimon_move_template_effect_status.get("daimon_move_template_status").daimon_status_template_name,
                        "daimon_status_description"      : daimon_move_template_effect_status.get("daimon_move_template_status").daimon_status_template_description,
                        "daimon_status_effect"           : daimon_move_template_effect_status.get("daimon_move_template_status").daimon_status_template_effect,
                        "daimon_status_duration_max"     : daimon_move_template_effect_status.get("daimon_move_template_status").daimon_status_template_duration_max,
                        "daimon_status_duration_current" : daimon_move_template_effect_status.get("daimon_move_template_status").daimon_status_template_duration_max,
                    }
                    ),
                    "daimon_move_status_weight": daimon_move_template_effect_status.get("daimon_move_template_status_weight"),
                    "daimon_effect_status_target": daimon_move_template_effect_status.get("daimon_move_template_status_target")
                }
                for daimon_move_template_effect_status in daimon_move_template.daimon_move_template_effect_status
            ],
            "daimon_move_effect_stat_change" : daimon_move_template.daimon_move_template_effect_stat_change
        })
        for daimon_move_template in available_daimon_move_templates
    ]

    random.shuffle(available_moves)

    # Ensure the Daimon has 4 move slots
    while len(available_moves) < 4:
        available_moves.append(None)

    daimon_move_1, daimon_move_2, daimon_move_3, daimon_move_4 = available_moves[:4]

    # 9️⃣ Held item (simplified)
    item_template_entries = [
        entry for entry in random_daimon_template.daimon_template_item_template_pool
        if entry.get("item_template") is not None
    ]

    if item_template_entries:
        item_template_options = [entry["item_template"] for entry in item_template_entries]
        item_template_weights = [entry["item_template_weight"] for entry in item_template_entries]

        selected_template = random.choices(item_template_options, item_template_weights, k=1)[0]

        # Generate hex codes depending on category
        if selected_template.item_template_category in ITEM_CATEGORY_GENERIC:
            # Use template hex codes directly
            hex_codes = [
                selected_template.item_template_base_hex_code_1,
                selected_template.item_template_base_hex_code_2,
                selected_template.item_template_base_hex_code_3,
                selected_template.item_template_base_hex_code_4,
                selected_template.item_template_base_hex_code_5,
                selected_template.item_template_base_hex_code_6,
                selected_template.item_template_base_hex_code_7,
                selected_template.item_template_base_hex_code_8,
                selected_template.item_template_base_hex_code_9,
                selected_template.item_template_base_hex_code_10,
            ]
        if selected_template.item_template_category in ITEM_CATEGORY_UNIQUE:
            # Randomize 10 hex codes ("#RRGGBB")
            hex_codes = [
                "#{:06x}".format(random.randint(0, 0xFFFFFF))
                for _ in range(10)
            ]

        daimon_item = Item(
            item_id          = selected_template.item_template_id,
            item_name        = selected_template.item_template_name,
            item_description = selected_template.item_template_description,
            item_category    = selected_template.item_template_category,
            item_actions     = selected_template.item_template_actions,
            item_base_value  = selected_template.item_template_base_value,
            item_hex_code_1  = hex_codes[0],
            item_hex_code_2  = hex_codes[1],
            item_hex_code_3  = hex_codes[2],
            item_hex_code_4  = hex_codes[3],
            item_hex_code_5  = hex_codes[4],
            item_hex_code_6  = hex_codes[5],
            item_hex_code_7  = hex_codes[6],
            item_hex_code_8  = hex_codes[7],
            item_hex_code_9  = hex_codes[8],
            item_hex_code_10 = hex_codes[9],
            item_quantity    = 1
        )
    else:
        daimon_item = None

    # 🔟 Construct DaimonUnbonded
    daimon_unbonded = DaimonUnbonded(
        daimon_unbonded_id                    = len(daimon_unbonded_global) + 1,
        daimon_unbonded_daimon_template_id    = random_daimon_template.daimon_template_id,
        daimon_unbonded_species               = random_daimon_template.daimon_template_species,
        daimon_unbonded_level                 = daimon_level,
        daimon_unbonded_level_progress        = daimon_level_progress,
        daimon_unbonded_gender                = daimon_gender,
        daimon_unbonded_height                = daimon_height,
        daimon_unbonded_weight                = daimon_weight,
        daimon_unbonded_max_health            = daimon_max_health,
        daimon_unbonded_current_health        = daimon_current_health,
        daimon_unbonded_status                = daimon_status,
        daimon_unbonded_stat_health           = daimon_stat_health,
        daimon_unbonded_stat_physical_attack  = daimon_stat_physical_attack,
        daimon_unbonded_stat_special_attack   = daimon_stat_special_attack,
        daimon_unbonded_stat_physical_defense = daimon_stat_physical_defense,
        daimon_unbonded_stat_special_defense  = daimon_stat_special_defense,
        daimon_unbonded_stat_speed            = daimon_stat_speed,
        daimon_unbonded_type_1                = daimon_type_1,
        daimon_unbonded_type_2                = daimon_type_2,
        daimon_unbonded_ability               = daimon_ability,
        daimon_unbonded_move_1                = daimon_move_1,
        daimon_unbonded_move_2                = daimon_move_2,
        daimon_unbonded_move_3                = daimon_move_3,
        daimon_unbonded_move_4                = daimon_move_4,
        daimon_unbonded_item                  = daimon_item
    )

    daimon_unbonded_global.append(daimon_unbonded)

    print(f"✅ Spawned Daimon: Lv.{daimon_unbonded.daimon_unbonded_level} {daimon_unbonded.daimon_unbonded_species}") 
    
    return daimon_unbonded

def generate_random_daimon_unbonded_team() -> Optional[List[DaimonUnbonded]]:
    """
    Generates a random team of 1-6 DaimonUnbonded.
    """

    # 1️⃣ Determine random team size
    team_size = random.randint(1, 6)

    # 2️⃣ Generate DaimonUnbonded, convert to DaimonBonded, and assign positions
    daimon_team = []
    for i in range(1, team_size + 1):
        daimon_unbonded = generate_random_daimon_unbonded()
        daimon_team.append(daimon_unbonded)

def generate_random_quest_side() -> "QuestSide":
    # 1️⃣ Choose a random QuestType
    quest_type = random.choice(quest_type_global)

    # Define guaranteed main QuestStep IDs per type
    REQUIRED_STEP_BY_TYPE = {
        "Defeat": 5,
        "Deliver": 6,
        "Disband": 7,
        "Discover": 8
    }

    # 2️⃣ Pick start and end templates
    start_template = random.choice(quest_type.quest_type_quest_step_template_starts)
    end_template = random.choice(quest_type.quest_type_quest_step_template_ends)

    # 3️⃣ Prepare middle templates
    middle_templates = quest_type.quest_type_quest_step_template_steps

    # Always include the required step if applicable
    required_step_id = REQUIRED_STEP_BY_TYPE.get(quest_type.quest_type_name)
    required_template = None
    if required_step_id is not None:
        # Find the template object matching the required ID
        required_template = next(
            (t for t in middle_templates if t.quest_step_template_id == required_step_id),
            None
        )

    # Randomly sample remaining steps (excluding required one)
    optional_middle_templates = [
        t for t in middle_templates if t is not required_template
    ]

    sampled_templates = random.sample(
        optional_middle_templates,
        k=random.randint(0, len(optional_middle_templates))
    )

    # Combine them, ensuring required_template is always present
    all_middle = []
    if required_template:
        all_middle.append(required_template)
    all_middle.extend(sampled_templates)

    # Shuffle middle templates to add variation (so the required one isn’t always first)
    random.shuffle(all_middle)

    all_templates = [start_template] + all_middle + [end_template]
    quest_steps: List[QuestStep] = []

    # 4️⃣ Generate step starts
    step_starts = [random.choice(all_templates[0].quest_step_template_start_pool)]
    for template in all_templates[1:]:
        step_starts.append(random.choice(template.quest_step_template_start_pool))

    # 5️⃣ Generate last step end
    last_end = random.choice(all_templates[-1].quest_step_template_end_pool)

    # 6️⃣ Construct QuestStep objects with chaining
    for idx, template in enumerate(all_templates):
        step_start = step_starts[idx]
        step_end = step_starts[idx + 1] if idx < len(all_templates) - 1 else last_end

        step_start_type = type(step_start).__name__
        step_end_type = type(step_end).__name__

        reward_money = random.randint(*template.quest_step_template_reward_money_range)

        # Weighted item rewards
        reward_item = None
        pool = template.quest_step_template_reward_item_template_pool
        if pool:
            items = [e["item_template"] for e in pool]
            weights = [e["item_template_weight"] for e in pool]
            chosen_template = random.choices(items, weights=weights, k=1)[0]
            reward_item = Item(
                item_id=chosen_template.item_template_id,
                item_name=chosen_template.item_template_name,
                item_description=chosen_template.item_template_description,
                item_category=chosen_template.item_template_category,
                item_actions=chosen_template.item_template_actions,
                item_base_value=chosen_template.item_template_base_value,
                item_hex_code_1=chosen_template.item_template_base_hex_code_1,
                item_hex_code_2=chosen_template.item_template_base_hex_code_2,
                item_hex_code_3=chosen_template.item_template_base_hex_code_3,
                item_hex_code_4=chosen_template.item_template_base_hex_code_4,
                item_hex_code_5=chosen_template.item_template_base_hex_code_5,
                item_hex_code_6=chosen_template.item_template_base_hex_code_6,
                item_hex_code_7=chosen_template.item_template_base_hex_code_7,
                item_hex_code_8=chosen_template.item_template_base_hex_code_8,
                item_hex_code_9=chosen_template.item_template_base_hex_code_9,
                item_hex_code_10=chosen_template.item_template_base_hex_code_10,
                item_quantity=random.randint(1, 3)
            )

        quest_steps.append(QuestStep(
            quest_step_id=len(quest_steps) + 1,
            quest_step_name=f"{template.quest_step_template_name} Step",
            quest_step_description=template.quest_step_template_description,
            quest_step_start_type=step_start_type,
            quest_step_start=step_start,
            quest_step_end_type=step_end_type,
            quest_step_end=step_end,
            quest_step_reward_money=reward_money,
            quest_step_reward_item=reward_item,
            quest_step_status="Not Started"
        ))

    # 7️⃣ Aggregate QuestSide info
    total_reward_money = sum(step.quest_step_reward_money for step in quest_steps)
    total_reward_items = [
        step.quest_step_reward_item
        for step in quest_steps
        if step.quest_step_reward_item is not None
    ]

    quest_side_start = quest_steps[0].quest_step_start
    quest_side_end = quest_steps[-1].quest_step_end

    quest_side = QuestSide(
        quest_side_id=len(quest_side_global) + 1,
        quest_side_name=f"{quest_type.quest_type_name} Quest Side",
        quest_side_description=quest_type.quest_type_description,
        quest_side_type=quest_type.quest_type_name,
        quest_side_steps=quest_steps,
        quest_side_start_type=type(quest_side_start).__name__,
        quest_side_start=quest_side_start,
        quest_side_end_type=type(quest_side_end).__name__,
        quest_side_end=quest_side_end,
        quest_side_reward_money=total_reward_money,
        quest_side_reward_item=total_reward_items,
        quest_side_status="Not Started"
    )

    quest_side_global.append(quest_side)
    return quest_side

def load_all_data():
    print('Loading All Data')

    load_all_item_template()
    load_all_item()

    load_all_daimon_type()
    DaimonType.resolve_daimon_type_relationships()
    for d in daimon_type_global:
        adv_names = [t.daimon_type_name for t in d.daimon_type_advantages]
        dis_names = [t.daimon_type_name for t in d.daimon_type_disadvantages]
        imm_names = [t.daimon_type_name for t in d.daimon_type_immunities]
        #print(f"  {d.daimon_type_name} -> Advantages: {adv_names}, Disadvantages: {dis_names}, Immunities: {imm_names}")
    load_all_daimon_status_template()
    load_all_daimon_status()
    load_all_daimon_ability()
    load_all_daimon_move_template()
    load_all_daimon_move()
    load_all_daimon_template()
    load_all_daimon_unbonded()
    load_all_daimon_bonded()

    load_all_weather_template()
    load_all_weather()
    load_all_biome()
    load_all_location()

    load_all_interactible()

    load_all_npc_item_inventory()
    load_all_npc_daimon_dex_entry()
    load_all_npc_daimon_dex()
    load_all_npc_daimon_inventory()
    load_all_npc_quest_main_inventory()
    load_all_npc_quest_side_inventory()
    load_all_npc()

    load_all_player_item_inventory()
    load_all_player_daimon_dex_entry()
    load_all_player_daimon_dex()
    load_all_player_daimon_inventory()
    load_all_player_quest_main_inventory()
    load_all_player_quest_side_inventory()
    load_all_player()

    load_all_quest_step_template()
    load_all_quest_step()
    load_all_quest_type()
    load_all_quest_side()
    load_all_quest_main()

    print('All Data Loaded\n')

def save_all_data():

    print('\nSaving All Data')

    #save_all_item_template()
    save_all_item()

    #save_all_daimon_type()
    #save_all_daimon_status_template()
    save_all_daimon_status()
    #save_all_daimon_ability()
    #save_all_daimon_move_template()
    save_all_daimon_move()
    #save_all_daimon_template()
    save_all_daimon_unbonded()
    save_all_daimon_bonded()

    #save_all_weather_template()
    #save_all_weather()
    #save_all_biome()
    save_all_location()

    save_all_interactible()

    save_all_npc_item_inventory()
    save_all_npc_daimon_dex_entry()
    save_all_npc_daimon_dex()
    save_all_npc_daimon_inventory()
    save_all_npc_quest_main_inventory()
    save_all_npc_quest_side_inventory()
    save_all_npc()

    save_all_player_item_inventory()
    save_all_player_daimon_dex_entry()
    save_all_player_daimon_dex()
    save_all_player_daimon_inventory()
    save_all_player_quest_main_inventory()
    save_all_player_quest_side_inventory()
    save_all_player()

    save_all_quest_step()
    save_all_quest_side()
    save_all_quest_main()

    print('All Data Saved')

if __name__ == "__main__":
    load_all_data()

    player = get_player_by_id(1)
    print(f'Player: {player.player_name}')
    location = get_location_by_id(player.player_location.location_id)
    print(f'Location: {location.location_name}')
    generate_random_daimon_unbonded(location)

    #test_full_inventory_and_daimon_operations()

    #test_player_daimon_catch()
    #print(f'DaimonBonded {player.player_daimon_inventory.player_daimon_inventory_team[0].daimon_bonded_move_1.daimon_move_effect_status}')
    #player = get_player_by_id(1)
    #location = get_location_by_id(8)
    #daimon = player.player_daimon_inventory.player_daimon_inventory_team[0]
    #daimon = generate_random_daimon_unbonded(location)
    #print(daimon.daimon_unbonded_move_1.daimon_move_effect_status)

    #test_player_vs_wild_daimon_battle()

    #test_npc_daimon_catch()

    #test_player_vs_npc_battle()

    save_all_data()