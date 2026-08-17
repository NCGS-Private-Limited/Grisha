from core.parser import command_split
from core.dispatcher import dispatch
from core.logger import logger
from core.config import config
from file_operations.test import test_file


class Assistant:
    def start(self):
        configuration = config()
        print(f"====== {configuration['assistant_name']} Here ======")
        print('Type "exit" to Stop')

        while True:
            user_input = input("> ")
            user_input = user_input.strip().lower()

            command, args = command_split(user_input)
            dispatch_output, status_output = dispatch(command, args)
            print(f"{configuration['assistant_name']}> {dispatch_output}")
            test_file()

            if user_input == "exit":
                logger(user_input, "GoodBye!",status_output)
                break
            else:
                logger(user_input, dispatch_output,status_output)
