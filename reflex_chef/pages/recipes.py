import reflex as rx

@rx.page(route="/recipes", title="Recipes")
def recipes() -> rx.Component:
    return rx.flex()