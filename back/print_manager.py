import sys


def mprint(message):
    try:
        print(message)
        sys.stdout.flush()

    except Exception as e:
        pass
