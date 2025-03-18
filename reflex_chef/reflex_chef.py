import reflex as rx

from .pages import *
from rxconfig import config

app = rx.App(
    theme=rx.theme(
        accent_color="teal",
        appearance="light"
    )
)
