from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from randovania.game.game_enum import RandovaniaGame
from randovania.games.cave_story.layout.cs_configuration import CSConfiguration
from randovania.layout.preset_describer import (
    GamePresetDescriber,
    fill_template_strings_from_tree,
    message_for_required_mains,
)

if TYPE_CHECKING:
    from randovania.game.gui import ProgressiveItemTuples
    from randovania.layout.base.base_configuration import BaseConfiguration


class CSPresetDescriber(GamePresetDescriber):
    def format_params(self, configuration: BaseConfiguration) -> dict[str, list[str]]:
        assert isinstance(configuration, CSConfiguration)

        template_strings = defaultdict(list)
        template_strings["Objective"].append(configuration.objective.long_name)
        template_strings.update(super().format_params(configuration))

        extra_message_tree = {
            "Item Placement": [
                {
                    "Puppies anywhere": configuration.puppies_anywhere,
                    "Puppies in Sand Zone only": not configuration.puppies_anywhere,
                }
            ],
            "Game Changes": [
                message_for_required_mains(
                    configuration.ammo_pickup_configuration, {"Missiles need main Launcher": "Missile Expansion"}
                ),
                {"No falling blocks in B2": configuration.no_blocks},
            ],
            "Difficulty": [{f"Starting HP: {configuration.starting_hp}": configuration.starting_hp != 3}],
        }
        fill_template_strings_from_tree(template_strings, extra_message_tree)

        return template_strings

    def progressive_items(self) -> ProgressiveItemTuples:
        from randovania.games.cave_story.layout import progressive_items

        return progressive_items.tuples()


hash_items = {
    1: "Arthur's Key",
    2: "Map System",
    3: "Santa's Key",
    4: "Silver Locket",
    5: "Beast Fang",
    6: "Life Capsule",
    7: "ID Card",
    8: "Jellyfish Juice",
    9: "Rusty Key",
    10: "Gum Key",
    11: "Gum Base",
    12: "Charcoal",
    13: "Explosive",
    14: "Puppy",
    15: "Life Pot",
    16: "Cure-All",
    17: "Clinic Key",
    18: "Booster 0.8",
    19: "Arms Barrier",
    20: "Turbocharge",
    21: "Curly's Air Tank",
    22: "Nikumaru Counter",
    23: "Booster 2.0",
    24: "Mimiga Mask",
    25: "Teleporter Room Key",
    26: "Sue's Letter",
    27: "Controller",
    28: "Broken Sprinkler",
    29: "Sprinkler",
    30: "Tow Rope",
    31: "Clay Figure Medal",
    32: "Little Man",
    33: "Mushroom Badge",
    34: "Ma Pignon",
    35: "Curly's Panties",
    36: "Alien Medal",
    37: "Chaco's Lipstick",
    38: "Whimsical Star",
    39: "Iron Bond",
}


def get_ingame_hash_str(hash_bytes: bytes) -> str:
    ids = get_ingame_hash(hash_bytes)

    def get_str(x: int) -> str:
        name = hash_items[x]
        path = str(RandovaniaGame.CAVE_STORY.data_path.joinpath("assets", "icon", f"{name}.png"))
        return f"""<img src="{path}" alt="{name}" width="32" height="16">"""

    return "".join([get_str(i) for i in ids])


def get_ingame_hash(hash_bytes: bytes) -> list[int]:
    NUM_HASH_ITEMS = 39

    num = int.from_bytes(hash_bytes, "big", signed=False)
    num %= NUM_HASH_ITEMS**5

    out = []
    for i in range(5):
        out.append((num % NUM_HASH_ITEMS) + 1)
        num //= NUM_HASH_ITEMS
    return out
