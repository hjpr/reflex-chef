import functools
import reflex as rx

from ..states.base_state import BaseState

def login_protected(page) -> rx.Component:
    @functools.wraps(page)
    def _wrapper() -> rx.Component:
        return rx.cond(BaseState.user_claims_authenticated, page(), rx.box("Please login to access..."))