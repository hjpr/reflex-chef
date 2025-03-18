import dotenv
import datetime
import json
import os
import reflex as rx
import rich

from ..components.classes import GroceryItem, SupabaseRequest
from ..states.base_state import BaseState
from datetime import datetime, timezone
from dotenv import load_dotenv
from loguru import logger

load_dotenv()
jwt_key = os.getenv("jwt_key")
api_url = os.getenv("api_url")
api_key = os.getenv("api_key")


class PantryState(BaseState):
    """
    State for managing the pantry items.
    """
    modified_at: str = ""
    meat_seafood: list[GroceryItem] = []
    fresh_produce: list[GroceryItem] = []
    milk_cheese_and_eggs: list[GroceryItem] = []
    bread_rice_and_flour: list[GroceryItem] = []
    spices_and_seasonings: list[GroceryItem] = []
    oils_and_vinegars: list[GroceryItem] = []
    snacks_and_sweets: list[GroceryItem] = []
    beverages: list[GroceryItem] = []
    frozen_foods: list[GroceryItem] = []
    condiments_and_sauces: list[GroceryItem] = []
    nuts_seeds_and_dried_fruits: list[GroceryItem] = []
    dry_baking_goods: list[GroceryItem] = []
    canned_goods: list[GroceryItem] = []
    jarred_goods: list[GroceryItem] = []

    def on_load(self) -> None:
        # Get pantry from Supabase.
        pantry = SupabaseRequest(
            api_url,
            api_key,
            self.access_token,
        )
        pantry = pantry.get_all_from_table("pantry", self.modified_at)

        # If user has a pantry, load it into state.
        if pantry:
            logger.info("Loading pantry content into state...")
            self.modified_at = pantry.get("modified_at", "")
            for item in pantry.get("contents", {}).get("meat_seafood", []):
                self.meat_seafood.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("fresh_produce", []):
                self.fresh_produce.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("milk_cheese_and_eggs", []):
                self.milk_cheese_and_eggs.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("bread_rice_and_flour", []):
                self.bread_rice_and_flour.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("spices_and_seasonings", []):
                self.spices_and_seasonings.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("oils_and_vinegars", []):
                self.oils_and_vinegars.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("snacks_and_sweets", []):
                self.snacks_and_sweets.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("beverages", []):
                self.beverages.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("frozen_foods", []):
                self.frozen_foods.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("condiments_and_sauces", []):
                self.condiments_and_sauces.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("nuts_seeds_and_dried_fruits", []):
                self.nuts_seeds_and_dried_fruits.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("dry_baking_goods", []):
                self.dry_baking_goods.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("canned_goods", []):
                self.canned_goods.append(GroceryItem.load(item))
            for item in pantry.get("contents", {}).get("jarred_goods", []):
                self.jarred_goods.append(GroceryItem.load(item))
            logger.info("Pantry content loaded into state.")  

        # If modified_at is empty, create a new pantry in the database.
        elif not self.modified_at:
            logger.info("No pantry items found in database.")
            create_pantry = SupabaseRequest(
                api_url,
                api_key,
                self.access_token,
            )
            create_pantry.insert_to_table(
                "pantry",
                {
                    "user_id": self.user_claims_id,
                    "contents": {
                        "meat_seafood": [],
                        "fresh_produce": [],
                        "milk_cheese_and_eggs": [],
                        "bread_rice_and_flour": [],
                        "spices_and_seasonings": [],
                        "oils_and_vinegars": [],
                        "snacks_and_sweets": [],
                        "beverages": [],
                        "frozen_foods": [],
                        "condiments_and_sauces": [],
                        "nuts_seeds_and_dried_fruits": [],
                        "dry_baking_goods": [],
                        "canned_goods": [],
                        "jarred_goods": [],
                    },
                    "modified_at": str(datetime.now(timezone.utc).isoformat(timespec="seconds")),
                }
            )