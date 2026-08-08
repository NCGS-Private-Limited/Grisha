from core.parser import command_split
from core.dispatcher import dispatch

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
            dispatch_output = dispatch(result[0],result[1:])
            print(f"Grisha> {dispatch_output}")