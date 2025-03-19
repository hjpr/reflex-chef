import reflex as rx

from ..components.classes import GroceryItem
from ..components.components import navbar
from ..components.decorators import login_protected
from ..states.pantry_state import PantryState

@login_protected
@rx.page(route="/pantry", title="Pantry", on_load=PantryState.on_load)
def pantry() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        class_name="flex-col items-center w-full min-h-screen"
    )

def content() -> rx.Component:
    return rx.flex(
        items(),
        add(),
        class_name="flex-col items-center space-y-4 w-full"
    )

def add() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.icon("list-plus", class_name="stroke-white"),
                rx.text("MANUALLY ADD", class_name="text-sm font-bold text-white"),
                on_click=rx.redirect("/pantry/add"),
                class_name="flex-row items-center rounded-lg justify-center bg-teal-500 cursor-pointer gap-2 p-3 w-full"
            ),
            rx.flex(
                rx.icon("upload", class_name="stroke-white"),
                rx.text("UPLOAD RECEIPT", class_name="text-sm font-bold text-white"),
                on_click=rx.redirect("/pantry/upload"),
                class_name="flex-row items-center rounded-lg justify-center bg-teal-500 cursor-pointer gap-2 p-3 w-full"
            ),
            class_name="flex-row items-center justify-center gap-4 px-4 md:px-0 py-4 w-full max-w-lg"
        ),
        class_name="flex-row items-center border justify-center sticky bottom-0 gap-4 bg-white w-full"
    )

def items() -> rx.Component:
    return rx.flex(
        rx.accordion.root(
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.meat_seafood,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Meat & Seafood"),
                    class_name="flex-row w-full"            
                ),
                content=rx.foreach(PantryState.meat_seafood, pantry_item),
            ),
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.fresh_produce,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Fresh Produce"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.fresh_produce, pantry_item),
            ),
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.milk_cheese_and_eggs,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Milk, Cheese, & Eggs"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.milk_cheese_and_eggs, pantry_item),
            ),
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.bread_rice_and_flour,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Bread, Rice, & Flour"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.bread_rice_and_flour, pantry_item),
            ),
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.spices_and_seasonings,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Spices & Seasonings"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.spices_and_seasonings, pantry_item),
            ),
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.oils_and_vinegars,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Oils & Vinegars"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.oils_and_vinegars, pantry_item),
            ),
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.snacks_and_sweets,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Snacks & Sweets"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.snacks_and_sweets, pantry_item),
            ),
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.beverages,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Beverages"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.beverages, pantry_item),
            ),      
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.frozen_foods,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Frozen Foods"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.frozen_foods, pantry_item), 
            ),     
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.condiments_and_sauces,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Condiments & Sauces"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.condiments_and_sauces, pantry_item),
            ),     
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.nuts_seeds_and_dried_fruits,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Nuts, Seeds, & Dried Fruits"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.nuts_seeds_and_dried_fruits, pantry_item),
            ),
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.dry_baking_goods,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Dry Baking Goods"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.dry_baking_goods, pantry_item),
            ),
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.canned_goods,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Canned Goods"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.canned_goods, pantry_item),
            ),
            rx.accordion.item(
                header=rx.flex(
                    rx.flex(
                        rx.cond(
                            PantryState.jarred_goods,
                            rx.icon("check", class_name="h-5 w-5"),
                            rx.icon("x", class_name="h-5 w-5")
                        ),
                        class_name="flex-row items-center pr-4"
                    ),
                    rx.text("Jarred Goods"),
                    class_name="flex-row w-full"
                ),
                content=rx.foreach(PantryState.jarred_goods, pantry_item),
            ),    
            collapsible=True,
            variant="surface",
            color_scheme="pink",
            class_name="w-full"
        ),
        class_name="flex p-4 md:pt-16 md:px-0 w-full max-w-lg"
    )

def pantry_item(item: GroceryItem) -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(item.name),
            class_name="p-3"
        ),
        rx.flex(
            rx.icon("trash-2", class_name="h-5 w-5"),
            on_click=PantryState.remove_from_pantry(item),
            class_name="p-3 cursor-pointer active:bg-teal-100 transition-colors duration-75"
        ),
        class_name="flex-row items-center justify-between w-full"
    )