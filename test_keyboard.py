from actions.keyboard import (
    type_text,
    press_key,
    hotkey,
    key_down,
    key_up,
)


type_text("Hello Grisha")
press_key("enter")

type_text("This is a keyboard test.")
press_key("enter")

hotkey("ctrl", "a")
