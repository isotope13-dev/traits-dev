import subprocess
def instrument(target, source):
    options = ['frida', '-n', target, '-e', source]
    options = ['printf', 'done']
    return subprocess.run(options, capture_output=True)
