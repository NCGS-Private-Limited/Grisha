from core.parser import command_split
from core.dispatcher import dispatch


class Assistant:
    def start(self):
        print("====== Grisha Here ======")
        print('Type "exit" to Stop')

        while True:
            user_input = input("> ")
            user_input = user_input.strip().lower()

            if user_input == "exit":
                print("Grisha> Goodbye!")
                break

            command, args = command_split(user_input)

            dispatch_output = dispatch(command, args)

            print(f"Grisha> {dispatch_output}")