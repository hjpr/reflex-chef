import reflex as rx

@rx.page(route="/planning", title="Meal Planning")
def planning() -> rx.Component:
    return rx.flex()