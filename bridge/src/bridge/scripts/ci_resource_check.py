import sys
from datetime import datetime


def main():
    print(f'[{{"timestamp": "{datetime.now().timestamp()}"}}]')
    sys.exit(0)
