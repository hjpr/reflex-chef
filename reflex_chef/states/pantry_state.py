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
from typing import Callable, Iterable

load_dotenv()
jwt_key = os.getenv("jwt_key")
api_url = os.getenv("api_url")
api_key = os.getenv("api_key")


class PantryState(BaseState):
    """
    State for managing the pantry items.
    """
    modified_at: str = ""
    quantity_unit_switch_dry: bool = True

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

    # Vars for manually adding items to the pantry.
    add_name: str = ""
    add_uuid: str = ""
    add_quantity_amount: str = ""
    add_quantity_unit: str = ""
    add_category: str = ""
    add_purchase_date: str = ""
    add_expiration_date: str = ""
    add_price: str = ""
    add_nutrition_serving_size: str = "" 
    add_nutrition_serving_unit: str = ""
    add_nutrition_calories: str = ""
    add_nutrition_carbs: str = ""
    add_nutrition_protein: str = ""
    add_nutrition_fat: str = ""
    add_nutrition_fiber: str = ""

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
            for item in pantry.get("meat_seafood", []):
                self.meat_seafood.append(GroceryItem.load(item))
            for item in pantry.get("fresh_produce", []):
                self.fresh_produce.append(GroceryItem.load(item))
            for item in pantry.get("milk_cheese_and_eggs", []):
                self.milk_cheese_and_eggs.append(GroceryItem.load(item))
            for item in pantry.get("bread_rice_and_flour", []):
                self.bread_rice_and_flour.append(GroceryItem.load(item))
            for item in pantry.get("spices_and_seasonings", []):
                self.spices_and_seasonings.append(GroceryItem.load(item))
            for item in pantry.get("oils_and_vinegars", []):
                self.oils_and_vinegars.append(GroceryItem.load(item))
            for item in pantry.get("snacks_and_sweets", []):
                self.snacks_and_sweets.append(GroceryItem.load(item))
            for item in pantry.get("beverages", []):
                self.beverages.append(GroceryItem.load(item))
            for item in pantry.get("frozen_foods", []):
                self.frozen_foods.append(GroceryItem.load(item))
            for item in pantry.get("condiments_and_sauces", []):
                self.condiments_and_sauces.append(GroceryItem.load(item))
            for item in pantry.get("nuts_seeds_and_dried_fruits", []):
                self.nuts_seeds_and_dried_fruits.append(GroceryItem.load(item))
            for item in pantry.get("dry_baking_goods", []):
                self.dry_baking_goods.append(GroceryItem.load(item))
            for item in pantry.get("canned_goods", []):
                self.canned_goods.append(GroceryItem.load(item))
            for item in pantry.get("jarred_goods", []):
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
            data = {
                "user_id": self.user_claims_id,
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
                "modified_at": str(datetime.now(timezone.utc).isoformat(timespec="seconds")),
            }
            create_pantry.insert_to_table(
                "pantry",
                data
            )

    def add_to_pantry(self) -> Iterable[Callable]:
        """
        Add item to pantry.
        """
        try:
            if not self.add_name:
                raise ValueError("Name is required.")
            if not self.add_quantity_amount:
                raise ValueError("Quantity amount is required.")
            if not self.add_quantity_unit:
                raise ValueError("Quantity unit is required.")
            if not self.add_category:
                raise ValueError("Category is required.")
            if not self.add_purchase_date:
                raise ValueError("Purchase date is required.")
            if not self.add_price:
                raise ValueError("Price is required.")

            # Create a new grocery item.
            grocery_dict = {
                "name": self.add_name,
                "quantity": {
                    "amount": float(self.add_quantity_amount),
                    "unit": self.add_quantity_unit,
                },
                "category": self.add_category,
                "expiration": self.add_expiration_date,
                "purchase_date": self.add_purchase_date,
                "price": float(self.add_price),
                "nutrition": {
                    "serving_size": {
                        "size": float(self.add_nutrition_serving_size) if self.add_nutrition_serving_size else 0.0,
                        "unit": self.add_nutrition_serving_unit,
                    },
                    "carbs": int(self.add_nutrition_carbs) if self.add_nutrition_carbs else 0,
                    "protein": int(self.add_nutrition_protein) if self.add_nutrition_protein else 0,
                    "fat": int(self.add_nutrition_fat) if self.add_nutrition_fat else 0,
                    "fiber": int(self.add_nutrition_fiber) if self.add_nutrition_fiber else 0,
                },
            }

            # Convert user readable category name to database category name.
            category_map = {
                "Meat & Seafood": "meat_seafood",
                "Fresh Produce": "fresh_produce",
                "Milk, Cheese & Eggs": "milk_cheese_and_eggs",
                "Bread, Rice & Flour": "bread_rice_and_flour",
                "Spices & Seasonings": "spices_and_seasonings",
                "Oils & Vinegars": "oils_and_vinegars",
                "Snacks & Sweets": "snacks_and_sweets",
                "Beverages": "beverages",
                "Frozen Foods": "frozen_foods",
                "Condiments & Sauces": "condiments_and_sauces",
                "Nuts, Seeds & Dried Fruits": "nuts_seeds_and_dried_fruits",
                "Dry Baking Goods": "dry_baking_goods",
                "Canned Goods": "canned_goods",
                "Jarred Goods": "jarred_goods"
            }
            # Map the category to the database category.
            grocery_dict["category"] = category_map.get(grocery_dict["category"])

            # Instantiate a GroceryItem object.
            grocery_item = GroceryItem.load(grocery_dict)

            # Add item to the appropriate category list.
            getattr(self, grocery_item.category).append(grocery_item)

            # Upload the updated pantry to Supabase.
            pantry = SupabaseRequest(
                api_url,
                api_key,
                self.access_token,
            )
            data = {
                f"{grocery_item.category}": [item.to_dict() for item in getattr(self, grocery_item.category)],
                "modified_at": str(datetime.now(timezone.utc).isoformat(timespec="seconds")),
            }
            pantry.update_table(
                self.user_claims_id,
                "pantry",
                data,
            )
            self.modified_at = data["modified_at"]
            yield rx.toast.success("Item added successfully.")
            self.reset_add_to_pantry()

        except Exception as e:
            return rx.toast.error("Error adding item to pantry: " + str(e))
        
    def reset_add_to_pantry(self) -> None:
        """
        Reset the add to pantry form.
        """
        self.add_name = ""
        self.add_quantity_amount = ""
        self.add_quantity_unit = ""
        self.add_category = ""
        self.add_purchase_date = ""
        self.add_expiration_date = ""
        self.add_price = ""
        self.add_nutrition_serving_size = "" 
        self.add_nutrition_serving_unit = ""
        self.add_nutrition_calories = ""
        self.add_nutrition_carbs = ""
        self.add_nutrition_protein = ""
        self.add_nutrition_fat = ""
        self.add_nutrition_fiber = ""
        self.quantity_unit_switch_dry = True

    def remove_from_pantry(self, item: GroceryItem) -> Iterable[Callable]:
        """
        Remove item from pantry.
        """
        try:
            # Remove item from the appropriate category list.
            logger.info("Removing item from pantry...")
            logger.info(self.meat_seafood.copy())
            setattr(self, item.category, [i for i in getattr(self, item.category) if i.uuid != item.uuid])
            logger.info("Item removed from pantry.")
            logger.info(self.meat_seafood.copy())

            # Upload the updated pantry to Supabase.
            pantry = SupabaseRequest(
                api_url,
                api_key,
                self.access_token,
            )
            data = {
                f"{item.category}": [i.to_dict() for i in getattr(self, item.category)],
                "modified_at": str(datetime.now(timezone.utc).isoformat(timespec="seconds")),
            }
            logger.info("Data to be uploaded:")
            rich.inspect(data)
            pantry.update_table(
                self.user_claims_id,
                "pantry",
                data,
            )
            self.modified_at = data["modified_at"]
            yield rx.toast.success("Item removed successfully.")

        except Exception as e:
            return rx.toast.error("Error removing item from pantry: " + str(e))