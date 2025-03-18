import reflex as rx

from ..components.components import navbar
from ..states.base_state import BaseState

@rx.page(route="/", title="Chef Dilly")
def index() -> rx.Component:
    return rx.flex(
        navbar(),
        content(),
        class_name="flex-col items-center w-full min-h-screen"
    )

def content() -> rx.Component:
    return rx.flex(
        rx.cond(
            BaseState.user_claims_authenticated,
            rx.flex(
                choices(),
                class_name="flex-col space-y-4 w-full max-w-xl"
            ),
            rx.flex(
                login(),
                class_name="flex items-center justify-center w-full"
            )
        ),
        class_name="flex-col items-center justify-center space-y-4 p-4 md:py-24 w-full"
    )

def login() -> rx.Component:
    return rx.flex(
        rx.image(src="/chefhatcat.png", class_name="w-[384] h-[216]"),
        rx.form(
            rx.flex(
                rx.flex(
                    rx.text("Email", class_name="text-sm"),
                    rx.input(
                        placeholder="Enter e-mail",
                        name="email",
                        type="email",
                    ),
                    class_name="flex-col p-4 w-full"
                ),
                rx.flex(
                    rx.text("Password", class_name="text-sm"),
                    rx.input(
                        placeholder="Enter password",
                        name="password",
                        type="password",
                    ),
                    class_name="flex-col p-4 w-full"
                ),
                class_name="flex-col w-full"
            ),
            rx.flex(
                rx.button(
                    "Login",
                    type="submit",
                    loading=BaseState.user_is_loading,
                    class_name="w-full cursor-pointer"),
                class_name="flex justify-center p-4 w-full"
            ),
            on_submit=BaseState.user_login,
            reset_on_submit=False,
            class_name="flex-col space-y-4 divide-y w-full"
        ),
        class_name="flex-col border rounded-lg w-full max-w-sm"
    )

def choices() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.flex(
                rx.text("PANTRY", class_name="text-sm"),
                on_click=rx.redirect("/pantry"),
                class_name="flex items-center justify-center border rounded w-full h-48 cursor-pointer active:bg-zinc-700 transition-colors duration-75"
            ),
            rx.flex(
                rx.text("RECIPES", class_name="text-sm"),
                on_click=rx.redirect("/recipes"),
                class_name="flex items-center justify-center border rounded w-full h-48 cursor-pointer active:bg-zinc-700 transition-colors duration-75"
            ),
            class_name="flex-col md:flex-row gap-4 w-full"
        ),
        rx.flex(
            rx.flex(
                rx.text("CALENDAR", class_name="text-sm"),
                on_click=rx.redirect("/calendar"),
                class_name="flex items-center justify-center border rounded w-full h-48 cursor-pointer active:bg-zinc-700 transition-colors duration-75"
            ),
            rx.flex(
                rx.text("MEAL PLANNING", class_name="text-sm"),
                on_click=rx.redirect("/planning"),
                class_name="flex items-center justify-center border rounded w-full h-48 cursor-pointer active:bg-zinc-700 transition-colors duration-75"
            ),
            class_name="flex-col md:flex-row gap-4 w-full"
        ),
        class_name="flex-col gap-4 w-full"
    )