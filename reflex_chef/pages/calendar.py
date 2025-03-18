import reflex as rx


@rx.page(route="/calendar", title="Calendar")
def calendar() -> rx.Component:
    return rx.flex()