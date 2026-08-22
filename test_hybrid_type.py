from actions.typing import type_into_element


print("Searching for Username field...")

try:
    element = type_into_element(
        "Email",
        "test123@gmail.com"
    )

    print("\n✓ SUCCESS")
    print("Element detected and text entered.")

except ValueError as e:
    print("\n✗ FAILED")
    print(e)