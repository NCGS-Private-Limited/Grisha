instant_memory = {}

def instmemory_set(key, value):
    instant_memory[key] = value

def instmemory_get(key):
    return instant_memory.get(key)

def instmemory_del(key):
    if key in instant_memory:
        del instant_memory[key]

def instmemory_clear():
    instant_memory.clear()