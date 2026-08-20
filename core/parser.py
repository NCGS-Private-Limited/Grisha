import shlex

def command_split(command):
    raw_input = shlex.split(command)

    command = raw_input[0]
    args = raw_input[1:]

    return command, args