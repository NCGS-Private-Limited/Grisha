class Assistant:
    def start(self):
        command = ""
        Grisha_start =""
        print("======Grisha Here======")
        print("Type to \"exit\" to Stop")
        command = input("> ")
        command = command.lower()
        command = command.strip()
        print(f"Grisha> {command}")
        if command == "exit":
            exit()