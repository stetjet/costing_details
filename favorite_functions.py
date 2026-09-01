import inspect
import re


def debug_print(*args):
    """Print each argument's source name, type, and value, prefixed with the calling line number."""

    frame = inspect.currentframe().f_back
    line_number = frame.f_lineno
    context = inspect.getframeinfo(frame).code_context
    call_line = context[0] if context else ''

    match = re.search(r'debug_print\s*\((.*)\)', call_line)
    arg_names = [a.strip() for a in match.group(1).split(',')] if match else []

    for i, value in enumerate(args):
        name = arg_names[i] if i < len(arg_names) else f'arg{i}'
        print(f'Line [{line_number}]: {type(value)}: {name} = {value!r}')

def flip_bool(boolean:bool):
    if boolean == True:
        return False
    if boolean == False:
        return True

if __name__ == '__main__':
    time = "6 O'clock"
    later = "7 O'clock"
    change = 1
    debug_print(time, later, change)