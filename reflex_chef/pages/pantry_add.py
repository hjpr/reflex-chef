import reflex as rx

from ..components.classes import GroceryItem
from ..components.components import navbar
from ..components.decorators import login_protected
from ..states.pantry_state import PantryState

@login_protected
@rx.page(route="/pantry/add", title="Add item to Pantry")
def pantry_add() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        class_name="flex-col items-center w-full min-h-screen"
    )

def content() -> rx.Component:
    return rx.flex(
        add_item(),
        class_name="flex-col items-center space-y-4 w-full"
    )

def add_item() -> rx.Component:
    return rx.flex(
        grocery_item(),
        class_name="flex-col items-center space-y-4 p-4 md:py-16 md:px-0 w-full"
    )

def grocery_item() -> rx.Component:
    return rx.flex(
        # Required entries.
        rx.flex(
            rx.flex(
                rx.text("Name", class_name="text-xs uppercase"),
                rx.input(
                    name="add_name",
                    value=PantryState.add_name,
                    placeholder="Enter name",
                    on_change=PantryState.setvar("add_name"),
                ),
                class_name="flex-col px-4 pt-4 pb-2 space-y-2 w-full"
            ),
            rx.flex(
                rx.flex(
                    rx.text("Amount", class_name="text-xs uppercase"),
                    rx.input(
                        name="add_quantity_amount",
                        type="number",
                        value=PantryState.add_quantity_amount,
                        placeholder="Enter quantity",
                        on_change=PantryState.setvar("add_quantity_amount"),
                    ),
                    class_name="flex-col space-y-2 w-full"
                ),
                rx.flex(
                    rx.flex(
                        rx.text("Unit", class_name="text-xs uppercase"),
                        rx.spacer(),
                        rx.flex(
                            rx.text("Wet", class_name="text-xs uppercase"),
                            rx.switch(
                                checked=PantryState.quantity_unit_switch_dry,
                                size="1",
                                on_change=[
                                    PantryState.setvar("quantity_unit_switch_dry", ~PantryState.quantity_unit_switch_dry),
                                    PantryState.setvar("add_quantity_unit", "")
                                ]
                            ),
                            rx.text("Dry", class_name="text-xs uppercase"),
                            class_name="flex-row space-x-2"
                        ),
                        class_name="flex-row w-full"
                    ),
                    rx.cond(
                        PantryState.quantity_unit_switch_dry,
                        rx.select(
                            ["oz", "lb", "g", "kg", "piece", "container"],
                            name="add_quantity_unit",
                            value=PantryState.add_quantity_unit,
                            placeholder="Select dry unit",
                            position="item-aligned",
                            on_change=PantryState.setvar("add_quantity_unit"),
                        ),
                        rx.select(
                            ["fl oz", "pint", "quart", "gallon", "ml", "l"],
                            name="add_quantity_unit",
                            value=PantryState.add_quantity_unit,
                            placeholder="Select wet unit",
                            position="item-aligned",
                            on_change=PantryState.setvar("add_quantity_unit")
                        ),
                    ),
                    class_name="flex-col space-y-2 w-full"
                ),
                class_name="flex-row gap-4 px-4 py-2 w-full"
            ),
            rx.flex(
                rx.text("Category", class_name="text-xs uppercase"),
                rx.select(
                    [
                        "Meat & Seafood",
                        "Fresh Produce",
                        "Milk, Cheese & Eggs",
                        "Bread, Rice & Flour",
                        "Spices & Seasonings",
                        "Oils & Vinegars",
                        "Snacks & Sweets",
                        "Beverages",
                        "Frozen Foods",
                        "Condiments & Sauces",
                        "Nuts, Seeds & Dried Fruits",
                        "Dry Baking Goods",
                        "Canned Goods",
                        "Jarred Goods"
                    ],
                    name="add_category",
                    default_value="",
                    value=PantryState.add_category,
                    placeholder="Select category",
                    position="item-aligned",
                    on_change=PantryState.setvar("add_category"),
                ),
                class_name="flex-col px-4 py-2 space-y-2 w-full"
            ),
            rx.flex(
                rx.text("Purchase Date", class_name="text-xs uppercase"),
                rx.input(
                    name="add_purchase_date",
                    value=PantryState.add_purchase_date,
                    type="date",
                    placeholder="Enter purchase date",
                    on_change=PantryState.setvar("add_purchase_date"),
                ),
                class_name="flex-col px-4 pt-2 py-2 space-y-2 w-full"
            ),
            rx.flex(
                rx.text("Price - $", class_name="text-xs uppercase"),
                rx.input(
                    name="add_price",
                    value=PantryState.add_price,
                    placeholder="Enter item price",
                    type="number",
                    on_change=PantryState.setvar("add_price"),
                ),
                class_name="flex-col px-4 pt-2 pb-4 space-y-2 w-full"
            ),
            class_name="flex-col items-center w-full" 
        ),
        # Optional entries.
        rx.flex(
            rx.flex(
                rx.button(
                    rx.flex(
                        rx.icon("brain", class_name="h-4 w-4"),
                        rx.text("Best guess", class_name="text-sm uppercase mt-0.5"),
                        class_name="flex items-center justify-center space-x-2"
                    ),
                    size="2",
                    variant="surface"
                ),
                class_name="flex items-center justify-center space-x-4 pt-4  w-full"
            ),
            rx.flex(
                rx.text("Expiration Date", class_name="text-xs uppercase"),
                rx.input(
                    name="add_expiration_date",
                    type="date",
                    value=PantryState.add_expiration_date,
                    placeholder="Enter expiration date",
                    on_change=PantryState.setvar("add_expiration_date"),
                ),
                class_name="flex-col px-4 pt-4 pb-2 space-y-2 w-full"
            ),
            rx.flex(
                rx.flex(
                    rx.text("Serving Size", class_name="text-xs uppercase"),
                    rx.input(
                        name="add_nutrition_serving_size",
                        value=PantryState.add_nutrition_serving_size,
                        type="number",
                        placeholder="Enter serving size",
                        on_change=PantryState.setvar("add_nutrition_serving_size"),
                    ),
                    class_name="flex-col space-y-2 w-full"
                ),
                rx.flex(
                    rx.text("Units", class_name="text-xs uppercase"),
                    rx.cond(
                        PantryState.quantity_unit_switch_dry,
                        rx.select(
                            ["oz", "cup", "g", "tbsp", "piece"],
                            name="add_nutrition_serving_unit",
                            value=PantryState.add_nutrition_serving_unit,
                            placeholder="Select dry unit",
                            position="item-aligned",
                            on_change=PantryState.setvar("add_nutrition_serving_unit"),
                        ),
                        rx.select(
                            ["fl oz", "ml", "tbsp", "cup"],
                            name="add_nutrition_serving_unit",
                            value=PantryState.add_nutrition_serving_unit,
                            placeholder="Select wet unit",
                            position="item-aligned",
                            on_change=PantryState.setvar("add_nutrition_serving_unit")
                        ),
                    ),
                    class_name="flex-col space-y-2 w-full"
                ),
                class_name="flex-row gap-4 px-4 py-2 w-full"
            ),
            rx.flex(
                rx.flex(
                    rx.text("Carbs", class_name="text-xs uppercase"),
                    rx.input(
                        name="add_nutrition_carbs",
                        value=PantryState.add_nutrition_carbs,
                        type="number",
                        placeholder="kcal",
                        on_change=PantryState.setvar("add_nutrition_carbs"),
                    ),
                    class_name="flex-col space-y-2 w-full"
                ),
                rx.flex(
                    rx.text("Protein", class_name="text-xs uppercase"),
                    rx.input(
                        name="add_nutrition_protein",
                        value=PantryState.add_nutrition_protein,
                        type="number",
                        placeholder="kcal",
                        on_change=PantryState.setvar("add_nutrition_protein"),
                    ),
                    class_name="flex-col space-y-2 w-full"
                ),
                rx.flex(
                    rx.text("Fat", class_name="text-xs uppercase"),
                    rx.input(
                        name="add_nutrition_fat",
                        value=PantryState.add_nutrition_fat,
                        type="number",
                        placeholder="kcal",
                        on_change=PantryState.setvar("add_nutrition_fat"),
                    ),
                    class_name="flex-col space-y-2 w-full"
                ),
                rx.flex(
                    rx.text("Fiber", class_name="text-xs uppercase"),
                    rx.input(
                        name="add_nutrition_fiber",
                        value=PantryState.add_nutrition_fiber,
                        type="number",
                        placeholder="kcal",
                        on_change=PantryState.setvar("add_nutrition_fiber"),
                    ),
                    class_name="flex-col space-y-2 w-full"
                ),
                class_name="flex-row gap-4 px-4 pt-2 pb-4 w-full"
            ),
            class_name="flex-col items-center w-full"
        ),
        rx.flex(
            rx.button(
                rx.text("Add item", class_name="text-sm uppercase"),
                on_click=PantryState.add_to_pantry,
                class_name="w-full"
            ),
            class_name="flex p-4 w-full"
        ),
        class_name="flex-col border rounded-lg items-center divide-y w-full max-w-md"
    )
