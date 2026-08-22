from actions.screen import observe_screen


screen = observe_screen()

print("=" * 60)
print("GRISHA OCR TEST")
print("=" * 60)

for element in screen["elements"]:

    print(
        f'"{element["text"]}" '
        f'-> '
        f'({element["x"]}, {element["y"]}) '
        f'{element["width"]}x{element["height"]} '
        f'confidence={element["confidence"]:.1f} '
        f'source={element["source"]}'
    )