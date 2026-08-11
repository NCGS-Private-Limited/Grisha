def memory_extract(user_input):
    if user_input.startswith("remember for now that"):
        print("Instant memory request")
        prefix_text = "remember for now that"

        memory_text = user_input[len("remember for now that"):].strip()
        print(memory_text)