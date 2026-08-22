from actions.mouse import (
    get_mouse_position,
    move_mouse,
    move_mouse_relative,
    click,
    right_click,
    double_click,
    mouse_down,
    mouse_up,
)


print("Current position:", get_mouse_position())

move_mouse(500, 300)

print("New position:", get_mouse_position())

move_mouse_relative(100, 50)

print("After relative movement:", get_mouse_position())