import sys

from ..concourse import concourse_method



@concourse_method(required_source=('db',), required_params=('ident_hash',))
def main(input_, environ):
    ident_hash = input_['params']['ident_hash']

    # Start extracting stuff here
    print(" *** 3xTr4cT0r ***", file=sys.stderr)

    output = {'version': 'smoo'}
    return output
