import shlex

test = shlex.split('move folder "my projects" "test/my projects"')
print(test)