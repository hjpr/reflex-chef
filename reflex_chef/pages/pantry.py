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
        add(),
        items(),
        class_name="flex-col items-center justify-center space-y-4 py-4 md:py-24 p-4 w-full max-w-lg"
    )

def add() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("list-plus", class_name="stroke-white"),
            rx.text("MANUALLY ADD", class_name="text-sm font-bold text-white"),
            class_name="flex-row items-center rounded-lg justify-center bg-teal-500 cursor-pointer gap-2 p-2 w-full"
        ),
        rx.flex(
            rx.icon("wand-sparkles", class_name="stroke-white"),
            rx.text("UPLOAD RECEIPT", class_name="text-sm font-bold text-white"),
            class_name="flex-row items-center rounded-lg justify-center bg-teal-500 cursor-pointer gap-2 p-2 w-full"
        ),
        class_name="flex-row items-center justify-center gap-4 w-full max-w-xl"
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
                disabled=~PantryState.meat_seafood
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
                disabled=~PantryState.fresh_produce
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
                disabled=~PantryState.milk_cheese_and_eggs
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
                disabled=~PantryState.bread_rice_and_flour
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
                disabled=~PantryState.spices_and_seasonings  
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
                disabled=~PantryState.oils_and_vinegars
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
                disabled=~PantryState.snacks_and_sweets 
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
                disabled=~PantryState.beverages
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
                disabled=~PantryState.frozen_foods   
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
                disabled=~PantryState.condiments_and_sauces
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
                disabled=~PantryState.nuts_seeds_and_dried_fruits 
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
                disabled=~PantryState.dry_baking_goods
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
                disabled=~PantryState.canned_goods
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
                disabled=~PantryState.jarred_goods
            ),    
            collapsible=True,
            variant="surface",
            class_name="w-full"
        ),
        class_name="flex w-full max-w-xl"
    )

def pantry_item(item: GroceryItem) -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.text(item.name),
            class_name="p-3"
        ),
        rx.flex(
            rx.icon("trash-2", class_name="h-5 w-5"),
            class_name="p-3 cursor-pointer active:bg-teal-100 transition-colors duration-75"
        ),
        class_name="flex-row items-center justify-between w-full"
    )