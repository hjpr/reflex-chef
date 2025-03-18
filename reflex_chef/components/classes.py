import httpx
import json

from datetime import datetime, timezone
from loguru import logger
from reflex.base import Base

class GroceryItem(Base):
    name: str = ""
    quantity: dict = {}
    category: str = ""
    expiration: str = ""
    purchase_date: str = ""
    price: float = 0.0
    nutrition: dict = {}
    allergens: list = []

    def load(self, data: dict) -> None:
        self.name = data.get("name", "")
        self.quantity = data.get("quantity", {})
        self.category = data.get("category", "")
        self.expiration = data.get("expiration", "")
        self.purchase_date = data.get("purchase_date", "")
        self.price = data.get("price", 0.0)
        self.nutrition = data.get("nutrition", {})
        self.allergens = data.get("allergens", [])

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "quantity": self.quantity,
            "category": self.category,
            "expiration": self.expiration,
            "purchase_date": self.purchase_date,
            "price": self.price,
            "nutrition": self.nutrition,
            "allergens": self.allergens
            }
        
class SupabaseRequest(Base):
    api_url: str = ""
    api_key: str = ""
    access_token: str = ""

    def __init__(self, api_url: str, api_key: str, access_token: str) -> None:
        super().__init__()
        self.api_url = api_url
        self.api_key = api_key
        self.access_token = access_token

    def get_all_from_table(self, table: str, last_modified: str) -> dict | None:
        logger.info(f"Requesting data from table '{table}'...")
        url= f"{self.api_url}/rest/v1/{table}?&select=modified_at"
        headers={
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        if not (
            self.api_url or
            self.api_key or
            self.access_token or
            table
        ):
            raise ValueError("Missing required parameters.")
        
        # Check if pantry has been modified first.
        response = httpx.get(
            url=url,
            headers=headers
        )
        if response.is_success:
            logger.info(f"Data from table '{table}' received.")
            content = dict(json.loads(response.content)[0])

            # Check if last_modified in database is different from the one in the state.
            if content.get("modified_at", "") != last_modified:
                logger.info(f"Pantry is outdated. Refreshing with current data...")
                url = f"{self.api_url}/rest/v1/{table}?select=*"
                response = httpx.get(
                    url=url,
                    headers=headers
                )
                if response.is_success:
                    return dict(json.loads(response.content)[0])
                else:
                    raise httpx.RequestError(f"Error: {response.status_code} - {response.text}")
            else:
                logger.info(f"Pantry is up to date.")
        else:
            raise httpx.RequestError(f"Error: {response.status_code} - {response.text}")
        
    def insert_to_table(self, table: str, data: dict) -> None:
        """ 
        Specify the table name and data to insert.
        """
        logger.info(f"Creating entry in table '{table}'...")
        url = f"{self.api_url}/rest/v1/{table}"
        headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        if not (
            self.api_url or
            self.api_key or
            self.access_token or
            table or
            data
        ):
            raise ValueError("Missing required parameters.")
        response = httpx.post(
            url=url,
            headers=headers,
            data=json.dumps(data)
        )
        if response.is_success:
            logger.info(f"Entry created in table '{table}'.")
        else:
            raise httpx.RequestError(f"Error: {response.status_code} - {response.text}")
        
    
