from actions.screen import observe_screen


screen = observe_screen()

print("=" * 60)
print("GRISHA SCREEN OBSERVATION")
print("=" * 60)

print(f"\nDetected {len(screen['elements'])} text elements:\n")

for element in screen["elements"]:

    print(
        f'Text: "{element["text"]}"'
    )

    print(
        f'Position: '
        f'({element["x"]}, {element["y"]})'
    )

    print(
        f'Size: '
        f'{element["width"]} x {element["height"]}'
    )

    print(
        f'Confidence: '
        f'{element["confidence"]:.1f}'
    )

    print("-" * 40)