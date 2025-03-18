import reflex as rx

def navbar() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.icon("cat"),
            rx.text("Chef Dilly", class_name="text-2xl font-bold"),
            class_name="flex-row items-center space-x-2 p-4"
        ),
        rx.spacer(),
        rx.flex(
            rx.icon("menu"),
            class_name="p-4 cursor-pointer"
        ),
        class_name="flex-row items-center shadow-lg backdrop-blur-lg sticky top-0 w-full p-4 h-12"
    )

def footer() -> rx.Component:
    return rx.flex(
        class_name="flex-row border w-full h-14"
    )