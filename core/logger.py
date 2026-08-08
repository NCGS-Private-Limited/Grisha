import datetime
from os import mkdir
from pathlib import Path


def logger(user_input, dispatch_output, status_output):
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = user_input
    output = dispatch_output

    try:
        mkdir("logs")
    except FileExistsError:
        pass

    file = Path("logs/logs.txt")

    with file.open("a") as f:
        f.write(f"[{date}] "
                f"command : {message}, "
                f"action : {output}, "
                f"status : {status_output}\n")  # we need to add the status of the command like success or failed
