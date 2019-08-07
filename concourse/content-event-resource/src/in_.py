import json
import sys


def in_(dest_path, in_stream):
    input = json.load(in_stream)

    return input


def main():
    dest_path = sys.argv[1]
    print(f"Output dir {dest_path}", file=sys.stderr)
    version = in_(dest_path, sys.stdin)
    print(f"Version is {version}", file=sys.stderr)


if __name__ == '__main__':
    main()
