from core.parser import command_split


class Assistant:
    def start(self):
        print("======Grisha Here======")
        print("Type to \"exit\" to Stop")
        command = ""

        while True:
            command = input("> ")
            command = command.strip().lower()

            if command == "exit":
                print("Grisha> Goodbye!")
                break

            result = command_split(command)
            print(f"Grisha> {result}")