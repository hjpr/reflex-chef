import reflex as rx

from ..components.classes import GroceryItem
from ..components.components import navbar
from ..components.decorators import login_protected
from ..states.pantry_state import PantryState

@login_protected
@rx.page(route="/pantry/upload", title="Upload receipt to Pantry", on_load=PantryState.on_load)
def pantry_upload() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        class_name="flex-col items-center w-full min-h-screen"
    )

def content() -> rx.Component:
    return rx.flex(
        class_name="flex-col items-center space-y-4 w-full"
    )
