import sys


def msg(msg, *args, **kwargs):
    print(msg.format(*args, **kwargs), file=sys.stderr)
