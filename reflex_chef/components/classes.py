import httpx
import json
import rich

from datetime import datetime, timezone
from loguru import logger
from reflex.base import Base
from uuid import uuid4

class GroceryItem(Base):
    """
    Data structure for a grocery item.
    """
    name: str = ""
    uuid: str = ""
    quantity: dict = {"amount": 0, "unit": ""}
    category: str = ""
    expiration_date: str = ""
    purchase_date: str = ""
    price: float = 0.0
    nutrition: dict = {
        "serving_size": {
            "quantity": 0.0,
            "unit": "",
        },
        "calories": 0,
        "carbs": 0,
        "protein": 0,
        "fat": 0,
        "fiber": 0,
    }

    def __init__(
            self,
            name="",
            uuid="",
            quantity=None,
            category="",
            expiration_date="",
            purchase_date="",
            price=0.0,
            nutrition=None
        ):
        super().__init__()
        self.name = name
        self.uuid = str(uuid4()) if not uuid else uuid
        self.quantity = quantity or {"amount": 0, "unit": ""}
        self.category = category
        self.expiration_date = expiration_date
        self.purchase_date = purchase_date
        self.price = price
        self.nutrition = nutrition or {
            "serving_size": {"quantity": 0.0, "unit": ""},
            "calories": 0,
            "carbs": 0,
            "protein": 0,
            "fat": 0,
            "fiber": 0,
        }

    @classmethod
    def load(cls, data: dict):
        return cls(
            name=data.get("name", ""),
            uuid=data.get("uuid", str(uuid4())),
            quantity=data.get("quantity", {"amount": 0, "unit": ""}),
            category=data.get("category", ""),
            expiration_date=data.get("expiration_date", ""),
            purchase_date=data.get("purchase_date", ""),
            price=data.get("price", 0.0),
            nutrition=data.get("nutrition", {
                "serving_size": {"quantity": 0.0, "unit": ""},
                "calories": 0,
                "carbs": 0,
                "protein": 0,
                "fat": 0,
                "fiber": 0,
            }),
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "uuid": self.uuid,
            "quantity": self.quantity,
            "category": self.category,
            "expiration_date": self.expiration_date,
            "purchase_date": self.purchase_date,
            "price": self.price,
            "nutrition": self.nutrition,
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
        
        # First request is to get the last modified date.
        response = httpx.get(
            url=url,
            headers=headers
        )
        if response.is_success:
            logger.info(f"Data from table '{table}' received.")
            content = json.loads(response.content)
            if content:
                content = content[0]
            else:
                logger.info(f"Pantry is empty.")
                return None

            # If last_modified is equal, we don't need to update the pantry.
            if content.get("modified_at", "") != last_modified:
                logger.info(f"Pantry is outdated. Refreshing with current data...")
                url = f"{self.api_url}/rest/v1/{table}?select=*"

                # Second request is to get the actual data.
                response = httpx.get(
                    url=url,
                    headers=headers
                )
                if response.is_success:
                    content = json.loads(response.content)[0]
                    return content
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
        
    def update_table(self, user_id: str, table: str, data: dict) -> None:
        """
        Specify the table name and data to update.
        """
        logger.info(f"Updating entry in table '{table}'...")
        url = f"{self.api_url}/rest/v1/{table}?user_id=eq.{user_id}"
        headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        logger.debug(self.access_token)
        if not (
            self.api_url or
            self.api_key or
            self.access_token or
            table or
            data
        ):
            raise ValueError("Missing required parameters.")
        
        response = httpx.patch(
            url=url,
            headers=headers,
            data=json.dumps(data)
        )
        if response.is_success:
            logger.info(f"Entry updated in table '{table}'.")
        else:
            raise httpx.RequestError(f"Error: {response.status_code} - {response.text}")
        
    
